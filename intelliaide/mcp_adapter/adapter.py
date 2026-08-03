"""Main MCP bridging adapter for IntelliAide.

Orchestrates: parse path -> select MCP tool -> call -> write to cache.
Handles wildcards via enumerate-then-fetch, resource list pagination,
and events format adaptation.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

from .parser import ParsedPath, PathKind, parse_path
from .plural_map import resolve_api_version, resolve_kind
from .mcp_client import MCPClient, MCPClientError


_UNSUPPORTED_KINDS = frozenset({
    PathKind.HOST_SERVICE_LOG,
    PathKind.AUDIT_LOG,
    PathKind.NETWORK_LOG,
    PathKind.STATIC_POD,
    PathKind.UNSUPPORTED,
})


class FetchResult:
    """Result of fetching a single path."""

    __slots__ = ("path", "status", "cache_path", "error")

    def __init__(self, path: str, status: str, cache_path: str = "", error: str = ""):
        self.path = path
        self.status = status  # "fetched", "skipped", "failed"
        self.cache_path = cache_path
        self.error = error

    def to_dict(self) -> Dict:
        d = {"path": self.path, "status": self.status}
        if self.cache_path:
            d["cache_path"] = self.cache_path
        if self.error:
            d["error"] = self.error
        return d


class MCPMustGatherAdapter:
    """Bridges IntelliAide file paths to MCP tool calls.

    Fetches must-gather data via MCP and writes it to a local cache
    directory so DataAnalyzer can read it as if it were mounted locally.
    """

    def __init__(self, mcp_url: str, cache_dir: str = "/tmp/must-gather-cache"):
        self._client = MCPClient(mcp_url)
        self._cache_dir = cache_dir
        Path(self._cache_dir).mkdir(parents=True, exist_ok=True)

    def fetch(self, raw_path: str) -> FetchResult:
        """Fetch a single must-gather path via MCP and write to cache."""
        parsed = parse_path(raw_path)

        if parsed.kind in _UNSUPPORTED_KINDS:
            return FetchResult(raw_path, "skipped", error=f"unsupported path type: {parsed.kind.name}")

        if parsed.has_wildcard and parsed.kind == PathKind.POD_LOG:
            return self._fetch_wildcard_pod_logs(parsed)

        try:
            content = self._dispatch(parsed)
        except MCPClientError as e:
            return FetchResult(raw_path, "failed", error=str(e))
        except Exception as e:
            return FetchResult(raw_path, "failed", error=f"unexpected error: {e}")

        if content is None:
            return FetchResult(raw_path, "failed", error="no content returned")

        cache_path = self._write_to_cache(raw_path, content)
        return FetchResult(raw_path, "fetched", cache_path=cache_path)

    def fetch_batch(self, paths: List[str]) -> Dict[str, List]:
        """Fetch multiple paths, returning a structured report.

        Returns:
            {"fetched": [...], "skipped_no_tool": [...], "failed": [...]}
        """
        report = {"fetched": [], "skipped_no_tool": [], "failed": []}

        for raw_path in paths:
            result = self.fetch(raw_path)
            if result.status == "fetched":
                report["fetched"].append(result.to_dict())
            elif result.status == "skipped":
                report["skipped_no_tool"].append(result.to_dict())
            else:
                report["failed"].append(result.to_dict())

        self._log(
            f"Fetch complete: {len(report['fetched'])} fetched, "
            f"{len(report['skipped_no_tool'])} skipped, "
            f"{len(report['failed'])} failed"
        )
        return report

    def close(self):
        """Close the underlying MCP client."""
        self._client.close()

    def _dispatch(self, parsed: ParsedPath) -> Optional[str]:
        """Route a parsed path to the correct MCP tool call."""
        if parsed.kind == PathKind.POD_LOG:
            return self._fetch_pod_log(parsed)
        elif parsed.kind == PathKind.EVENTS:
            return self._fetch_events(parsed)
        elif parsed.kind == PathKind.ETCD_INFO:
            return self._fetch_etcd(parsed)
        elif parsed.kind == PathKind.NODE_DIAG:
            return self._fetch_node_diag(parsed)
        elif parsed.kind in (PathKind.RESOURCE_LIST, PathKind.RESOURCE_GET):
            return self._fetch_resource(parsed)
        return None

    def _fetch_pod_log(self, parsed: ParsedPath) -> str:
        args = {"namespace": parsed.namespace or "", "pod": parsed.pod or ""}
        if parsed.container:
            args["container"] = parsed.container
        if parsed.previous:
            args["previous"] = True
        return self._client.call_tool("mustgather_pod_logs_get", args)

    def _fetch_events(self, parsed: ParsedPath) -> str:
        args = {}
        if parsed.namespace:
            args["namespace"] = parsed.namespace
        content = self._client.call_tool("mustgather_events_list", args)
        return self._reconstruct_events_yaml(content)

    # Matches a digest header line like:
    #   [Warning] 2026-07-28T11:25:17Z Pod/some-name (ns: some-namespace)
    _EVENT_HEADER_RE = re.compile(
        r"^\[(?P<type>\w+)\]\s+(?P<time>\S+)\s+(?P<kind>[\w.]+)/(?P<name>\S+)"
        r"(?:\s+\(ns:\s*(?P<namespace>[\w-]+)\))?$"
    )

    @classmethod
    def _reconstruct_events_yaml(cls, content: str) -> str:
        """Rebuild a Kubernetes-style Event List YAML from mustgather_events_list's
        human-readable digest so DataAnalyzer can extract per-event critical fields
        (metadata.namespace, type, reason, message, involvedObject.*).

        mustgather_events_list returns formatted text, not the raw events.yaml
        list from the must-gather archive:

            Found N events:

            [Warning] 2026-07-28T11:25:17Z Pod/some-name (ns: some-namespace)
              Reason: FailedScheduling
              Message: 0/6 nodes are available...

        Without this reconstruction, DataAnalyzer's YAML critical-field
        extractor sees only free text and reports "No critical fields
        extracted" for every events.yaml file, which is one of the
        contributors to perform_rca.py producing 0 chunks.
        """
        if not content:
            return content

        lines = content.splitlines()
        events = []
        current = None
        pending_field = None  # "Message" can wrap onto continuation lines

        for line in lines:
            header_match = cls._EVENT_HEADER_RE.match(line.strip())
            if header_match:
                if current:
                    events.append(current)
                gd = header_match.groupdict()
                current = {
                    "type": gd["type"],
                    "lastTimestamp": gd["time"],
                    "involvedObject": {"kind": gd["kind"], "name": gd["name"]},
                    "metadata": {"namespace": gd.get("namespace") or ""},
                    "reason": "",
                    "message": "",
                    "count": 1,
                }
                pending_field = None
                continue

            stripped = line.strip()
            if current is None:
                continue

            if stripped.startswith("Reason:"):
                current["reason"] = stripped[len("Reason:"):].strip()
                pending_field = "reason"
            elif stripped.startswith("Message:"):
                current["message"] = stripped[len("Message:"):].strip()
                pending_field = "message"
            elif stripped.startswith("Count:"):
                try:
                    current["count"] = int(stripped[len("Count:"):].strip())
                except ValueError:
                    pass
                pending_field = None
            elif stripped and pending_field:
                # Continuation of a wrapped Message/Reason line.
                current[pending_field] = (current[pending_field] + " " + stripped).strip()

        if current:
            events.append(current)

        if not events:
            # No parseable events (e.g. "No events found matching the
            # criteria") — return the original text so it's still cached
            # and visible, just not force-fed through the YAML parser.
            return content

        yaml_lines = ["apiVersion: v1", "kind: List", "items:"]
        for ev in events:
            yaml_lines.append("- apiVersion: v1")
            yaml_lines.append("  kind: Event")
            yaml_lines.append("  type: " + cls._yaml_quote(ev["type"]))
            yaml_lines.append("  reason: " + cls._yaml_quote(ev["reason"]))
            yaml_lines.append("  message: " + cls._yaml_quote(ev["message"]))
            yaml_lines.append("  count: " + str(ev["count"]))
            yaml_lines.append("  lastTimestamp: " + cls._yaml_quote(ev["lastTimestamp"]))
            yaml_lines.append("  metadata:")
            yaml_lines.append("    namespace: " + cls._yaml_quote(ev["metadata"]["namespace"]))
            yaml_lines.append("  involvedObject:")
            yaml_lines.append("    kind: " + cls._yaml_quote(ev["involvedObject"]["kind"]))
            yaml_lines.append("    name: " + cls._yaml_quote(ev["involvedObject"]["name"]))
        return "\n".join(yaml_lines) + "\n"

    @staticmethod
    def _yaml_quote(value: str) -> str:
        """Double-quote a scalar for safe embedding in hand-built YAML."""
        escaped = (value or "").replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'

    def _fetch_etcd(self, parsed: ParsedPath) -> str:
        subtype = parsed.etcd_subtype or ""
        if "health" in subtype or "endpoint_health" in subtype:
            return self._client.call_tool("mustgather_etcd_health", {})
        elif "object_count" in subtype or "member" in subtype:
            return self._client.call_tool("mustgather_etcd_object_count", {})
        # Default: try health
        return self._client.call_tool("mustgather_etcd_health", {})

    def _fetch_node_diag(self, parsed: ParsedPath) -> str:
        if not parsed.node:
            return self._client.call_tool("mustgather_node_diagnostics_get", {})
        return self._client.call_tool("mustgather_node_diagnostics_get", {"node": parsed.node})

    def _fetch_resource(self, parsed: ParsedPath) -> str:
        """Fetch a Kubernetes resource via MCP.

        Handles the names-only response issue: if >5 resources are returned
        as just names, fetches each individually via resource URI.
        """
        kind_str, default_api_version = resolve_kind(parsed.resource_kind or "")
        api_version = resolve_api_version(parsed.api_group or "") if parsed.api_group else default_api_version

        args = {}
        if kind_str:
            args["kind"] = kind_str
        if parsed.namespace:
            args["namespace"] = parsed.namespace
        if api_version:
            args["apiVersion"] = api_version

        # For RESOURCE_GET with a specific name, try the resource URI first
        if parsed.kind == PathKind.RESOURCE_GET and parsed.resource_name:
            content = self._try_resource_uri(
                kind_str, api_version, parsed.namespace, parsed.resource_name
            )
            if content:
                return content
            # Fallback to list with filter
            args["name"] = parsed.resource_name

        content = self._client.call_tool("mustgather_resources_list", args)

        # Detect names-only response and fetch individually
        if parsed.kind == PathKind.RESOURCE_LIST and self._is_names_only(content):
            full_content = self._fetch_resources_individually(
                content, kind_str, api_version, parsed.namespace
            )
            if full_content:
                return full_content

        return content

    def _try_resource_uri(
        self, kind: str, api_version: str, namespace: Optional[str], name: str
    ) -> Optional[str]:
        """Attempt to fetch a single resource via MCP resource URI template.

        The MCP server's URI template is:
            must-gather://current/resources/{group}/{version}/{kind}/{namespace}/{name}
        It uses the literal placeholder "-" (hyphen) for an empty group
        (core API) or a cluster-scoped resource (no namespace) — see
        pkg/toolsets/mustgather/mcp_resources.go's resourceGet, which only
        treats "-" as empty, not "_" or "". Sending anything else (e.g. an
        underscore) is treated as a literal namespace/group name and the
        lookup fails with "resource <kind>/<name> not found".
        """
        group = "-"
        version = api_version
        if "/" in api_version:
            group, version = api_version.rsplit("/", 1)
            group = group or "-"

        ns = namespace if namespace else "-"
        uri = f"must-gather://current/resources/{group}/{version}/{kind}/{ns}/{name}"

        try:
            return self._client.read_resource(uri)
        except MCPClientError:
            return None

    def _is_names_only(self, content: str) -> bool:
        """Detect if MCP response is just resource names (not full YAML).

        mustgather_resources_list's names-only format looks like:
            Found 19 Pod resource(s):

            - openshift-etcd/etcd-cluster-...-master-2
            - openshift-etcd/etcd-guard-...-master-0

        Every line starts with "- ", so a naive "starts with -" check
        misclassifies this as YAML (YAML lists also use "- "). The
        distinguishing signal is that a *key: value* pair follows the
        dash in real YAML list items (e.g. "- apiVersion: v1" or
        "- metadata:"), whereas names-only entries are a single bare
        token (namespace/name or name) with no colon-delimited mapping.
        """
        if not content:
            return False
        lines = [l.strip() for l in content.strip().splitlines() if l.strip()]
        if len(lines) <= 5:
            return False
        yaml_indicators = 0
        for line in lines[:20]:
            if line.startswith("apiVersion") or line.startswith("kind:"):
                yaml_indicators += 1
            elif line.startswith("- "):
                # A dash-prefixed YAML list item has a mapping after the
                # dash ("- key: value"); a names-only entry does not.
                after_dash = line[2:].strip()
                if ":" in after_dash:
                    yaml_indicators += 1
            elif ":" in line:
                yaml_indicators += 1
        return yaml_indicators < len(lines[:20]) * 0.3

    def _fetch_resources_individually(
        self, names_content: str, kind: str, api_version: str, namespace: Optional[str]
    ) -> Optional[str]:
        """Fetch each named resource individually and combine into a YAML list."""
        names = self._extract_resource_names(names_content)

        if not names:
            return None

        yaml_parts = ["apiVersion: v1", "kind: List", "items:"]
        for name in names:
            content = self._try_resource_uri(kind, api_version, namespace, name)
            if content:
                # Indent content under items list
                for line in content.splitlines():
                    yaml_parts.append(f"  {line}")
                yaml_parts.append("")

        if len(yaml_parts) <= 3:
            return None
        return "\n".join(yaml_parts)

    def _fetch_wildcard_pod_logs(self, parsed: ParsedPath) -> FetchResult:
        """Handle wildcard pod log paths by enumerating pods first.

        Step A: list pods in namespace via mustgather_resources_list
        Step B: fetch logs for each pod individually
        """
        ns = parsed.namespace
        if not ns:
            return FetchResult(
                parsed.original_path, "failed",
                error="wildcard pod log path missing namespace"
            )

        # Step A: enumerate pods
        try:
            pods_response = self._client.call_tool(
                "mustgather_resources_list",
                {"kind": "Pod", "namespace": ns, "apiVersion": "v1"},
            )
        except MCPClientError as e:
            return FetchResult(
                parsed.original_path, "failed",
                error=f"failed to list pods in {ns}: {e}"
            )

        pod_names = self._extract_pod_names(pods_response)
        if not pod_names:
            return FetchResult(
                parsed.original_path, "failed",
                error=f"no pods found in namespace {ns}"
            )

        # Step B: fetch logs for each pod
        fetched_count = 0
        for pod_name in pod_names:
            args = {"namespace": ns, "pod": pod_name}
            if parsed.container:
                args["container"] = parsed.container
            if parsed.previous:
                args["previous"] = True

            try:
                content = self._client.call_tool("mustgather_pod_logs_get", args)
                # Build the expanded path for this specific pod
                expanded_path = parsed.original_path.replace("*", pod_name)
                self._write_to_cache(expanded_path, content)
                fetched_count += 1
            except MCPClientError:
                continue

        if fetched_count == 0:
            return FetchResult(
                parsed.original_path, "failed",
                error=f"failed to fetch logs for any pod in {ns}"
            )

        return FetchResult(
            parsed.original_path, "fetched",
            cache_path=f"{self._cache_dir}/... ({fetched_count} pods)"
        )

    def _extract_pod_names(self, response: str) -> List[str]:
        """Extract bare pod names from a mustgather_resources_list response."""
        return self._extract_resource_names(response)

    @staticmethod
    def _extract_resource_names(response: str) -> List[str]:
        """Extract bare resource names from a mustgather_resources_list
        names-only response.

        Entries are formatted as "- <name>" or "- <namespace>/<name>"
        (e.g. "- openshift-etcd/etcd-master-0"). Namespace-scoped entries
        carry the namespace as a prefix, which must be stripped since
        downstream tools (mustgather_pod_logs_get, resource URIs) take the
        namespace as a separate argument, not part of the name.
        """
        if not response:
            return []
        names = []
        for line in response.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("="):
                continue
            if not line.startswith("- "):
                # Skip header/summary lines like "Found 19 Pod resource(s):"
                continue
            entry = line[2:].strip()
            if not entry or ":" in entry or len(entry) >= 200:
                continue
            # Strip a leading "<namespace>/" prefix if present.
            name = entry.rsplit("/", 1)[-1] if "/" in entry else entry
            if name:
                names.append(name)
        return names

    def _write_to_cache(self, relative_path: str, content: str) -> str:
        """Write content to the local cache at the appropriate path."""
        # Strip variable prefixes
        clean_path = relative_path.strip().lstrip("/")
        for prefix in ("quay", "must-gather"):
            while clean_path.lower().startswith(prefix):
                idx = clean_path.find("/")
                if idx == -1:
                    break
                clean_path = clean_path[idx + 1:]

        full_path = os.path.join(self._cache_dir, clean_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return full_path

    @staticmethod
    def _log(msg: str) -> None:
        print(f"[mcp_adapter] {msg}", file=sys.stderr)
