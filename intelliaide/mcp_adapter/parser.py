"""Path parser for must-gather archive paths.

Parses must-gather relative paths into structured ParsedPath objects that
carry enough information to select the correct MCP tool and arguments.

"""

import re
from enum import Enum, auto
from typing import Optional


class PathKind(Enum):
    RESOURCE_LIST = auto()
    RESOURCE_GET = auto()
    POD_LOG = auto()
    EVENTS = auto()
    ETCD_INFO = auto()
    NODE_DIAG = auto()
    HOST_SERVICE_LOG = auto()
    AUDIT_LOG = auto()
    NETWORK_LOG = auto()
    STATIC_POD = auto()
    UNSUPPORTED = auto()


class ParsedPath:
    """Structured representation of a parsed must-gather path."""

    __slots__ = (
        "kind", "namespace", "pod", "container", "previous",
        "resource_kind", "resource_name", "api_group", "api_version",
        "node", "etcd_subtype", "original_path", "has_wildcard",
    )

    def __init__(self, kind: PathKind, original_path: str, **kwargs):
        self.kind = kind
        self.original_path = original_path
        self.namespace: Optional[str] = kwargs.get("namespace")
        self.pod: Optional[str] = kwargs.get("pod")
        self.container: Optional[str] = kwargs.get("container")
        self.previous: bool = kwargs.get("previous", False)
        self.resource_kind: Optional[str] = kwargs.get("resource_kind")
        self.resource_name: Optional[str] = kwargs.get("resource_name")
        self.api_group: Optional[str] = kwargs.get("api_group")
        self.api_version: Optional[str] = kwargs.get("api_version")
        self.node: Optional[str] = kwargs.get("node")
        self.etcd_subtype: Optional[str] = kwargs.get("etcd_subtype")
        self.has_wildcard: bool = kwargs.get("has_wildcard", False)

    def __repr__(self):
        attrs = ", ".join(
            f"{k}={getattr(self, k)!r}"
            for k in self.__slots__
            if getattr(self, k) is not None and getattr(self, k) is not False
        )
        return f"ParsedPath({attrs})"


_KNOWN_PREFIXES_TO_STRIP = [
    re.compile(r"^/?(quay[^/]*/|must-gather[^/]*/)+", re.IGNORECASE),
]


def _strip_prefix(path: str) -> str:
    """Remove variable must-gather wrapper prefixes."""
    path = path.strip().lstrip("/")
    for pattern in _KNOWN_PREFIXES_TO_STRIP:
        path = pattern.sub("", path)
    return path.lstrip("/")


def _has_wildcard(segment: str) -> bool:
    return "*" in segment or "?" in segment


def parse_path(raw_path: str) -> ParsedPath:
    """Parse a must-gather relative path into a structured ParsedPath.

    Supports patterns:
      - namespaces/<ns>/<group>/<resource>.yaml
      - namespaces/<ns>/pods/<pod>/<container>/<container>/logs/{current,previous}.log
      - cluster-scoped-resources/<group>/<resource>.yaml
      - cluster-scoped-resources/<group>/<resource>/<name>.yaml
      - namespaces/<ns>/core/events.yaml
      - etcd_info/{endpoint_health,endpoint_status,member_list}.json
      - host_service_logs/masters/<service>.log
      - audit_logs/**
      - network_logs/**
      - static-pods/**
    """
    path = _strip_prefix(raw_path)
    parts = path.split("/")
    wildcard = any(_has_wildcard(p) for p in parts)

    # --- Pod logs ---
    # namespaces/<ns>/pods/<pod>/<container>/<container>/logs/{current,previous}.log
    if "pods" in parts and "logs" in parts:
        return _parse_pod_log(parts, raw_path, wildcard)

    # --- Events ---
    # namespaces/<ns>/core/events.yaml  OR  namespaces/<ns>/<group>/events.yaml
    if parts[-1] == "events.yaml" and parts[0] == "namespaces":
        ns = parts[1] if len(parts) > 1 else None
        return ParsedPath(PathKind.EVENTS, raw_path, namespace=ns, has_wildcard=wildcard)

    # --- ETCD info ---
    if parts[0] == "etcd_info" or (len(parts) > 1 and parts[0] == "cluster-scoped-resources" and "etcd" in path.lower()):
        subtype = parts[1] if len(parts) > 1 else None
        if subtype and subtype.endswith(".json"):
            subtype = subtype.rsplit(".", 1)[0]
        return ParsedPath(PathKind.ETCD_INFO, raw_path, etcd_subtype=subtype, has_wildcard=wildcard)

    # --- Host service logs ---
    if parts[0] == "host_service_logs":
        return ParsedPath(PathKind.HOST_SERVICE_LOG, raw_path, has_wildcard=wildcard)

    # --- Audit logs ---
    if parts[0] == "audit_logs":
        return ParsedPath(PathKind.AUDIT_LOG, raw_path, has_wildcard=wildcard)

    # --- Network logs ---
    if parts[0] == "network_logs" or parts[0] == "pod_network_connectivity_check":
        return ParsedPath(PathKind.NETWORK_LOG, raw_path, has_wildcard=wildcard)

    # --- Static pods ---
    if parts[0] == "static-pods":
        return ParsedPath(PathKind.STATIC_POD, raw_path, has_wildcard=wildcard)

    # --- Cluster-scoped resources ---
    if parts[0] == "cluster-scoped-resources":
        return _parse_cluster_scoped(parts, raw_path, wildcard)

    # --- Namespaced resources ---
    if parts[0] == "namespaces":
        return _parse_namespaced(parts, raw_path, wildcard)

    # --- Node diagnostics (alternative layout) ---
    if parts[0] == "nodes" or (parts[0] == "cluster-scoped-resources" and len(parts) > 2 and parts[2] == "nodes"):
        node = parts[1] if len(parts) > 1 and not _has_wildcard(parts[1]) else None
        return ParsedPath(PathKind.NODE_DIAG, raw_path, node=node, has_wildcard=wildcard)

    return ParsedPath(PathKind.UNSUPPORTED, raw_path, has_wildcard=wildcard)


def _parse_pod_log(parts: list, raw_path: str, wildcard: bool) -> ParsedPath:
    """Parse pod log path: namespaces/<ns>/pods/<pod>/<ctr>/<ctr>/logs/{current,previous}.log"""
    ns = None
    pod = None
    container = None
    previous = False

    try:
        ns_idx = parts.index("namespaces")
        ns = parts[ns_idx + 1] if ns_idx + 1 < len(parts) else None
    except ValueError:
        pass

    try:
        pod_idx = parts.index("pods")
        pod = parts[pod_idx + 1] if pod_idx + 1 < len(parts) else None
        # Container is the next segment after pod name
        if pod_idx + 2 < len(parts) and parts[pod_idx + 2] != "logs":
            container = parts[pod_idx + 2]
    except ValueError:
        pass

    log_file = parts[-1] if parts else ""
    if "previous" in log_file:
        previous = True

    pod_wildcard = pod is not None and _has_wildcard(pod)

    return ParsedPath(
        PathKind.POD_LOG, raw_path,
        namespace=ns, pod=pod, container=container,
        previous=previous, has_wildcard=wildcard or pod_wildcard,
    )


def _parse_cluster_scoped(parts: list, raw_path: str, wildcard: bool) -> ParsedPath:
    """Parse cluster-scoped-resources/<group>/<resource>.yaml or .../<resource>/<name>.yaml"""
    # cluster-scoped-resources/<group>/<resource>.yaml
    # cluster-scoped-resources/<group>/<resource>/<name>.yaml
    api_group = parts[1] if len(parts) > 1 else None
    resource_kind = None
    resource_name = None

    if len(parts) == 3:
        # e.g. cluster-scoped-resources/config.openshift.io/clusteroperators.yaml
        filename = parts[2]
        resource_kind = filename.rsplit(".", 1)[0] if "." in filename else filename
    elif len(parts) >= 4:
        # e.g. cluster-scoped-resources/config.openshift.io/clusteroperators/authentication.yaml
        resource_kind = parts[2]
        filename = parts[3]
        resource_name = filename.rsplit(".", 1)[0] if "." in filename else filename

    kind = PathKind.RESOURCE_GET if resource_name else PathKind.RESOURCE_LIST
    return ParsedPath(
        kind, raw_path,
        api_group=api_group, resource_kind=resource_kind,
        resource_name=resource_name, has_wildcard=wildcard,
    )


def _parse_namespaced(parts: list, raw_path: str, wildcard: bool) -> ParsedPath:
    """Parse namespaces/<ns>/<group>/<resource>.yaml or .../<resource>/<name>.yaml"""
    # namespaces/<ns>/<group>/<resource>.yaml
    # namespaces/<ns>/<group>/<resource>/<name>.yaml
    ns = parts[1] if len(parts) > 1 else None
    api_group = parts[2] if len(parts) > 2 else None
    resource_kind = None
    resource_name = None

    if len(parts) == 4:
        # namespaces/openshift-etcd/core/pods.yaml
        filename = parts[3]
        resource_kind = filename.rsplit(".", 1)[0] if "." in filename else filename
    elif len(parts) >= 5:
        # namespaces/openshift-etcd/core/pods/etcd-master-0.yaml
        resource_kind = parts[3]
        filename = parts[4]
        resource_name = filename.rsplit(".", 1)[0] if "." in filename else filename

    kind = PathKind.RESOURCE_GET if resource_name else PathKind.RESOURCE_LIST
    return ParsedPath(
        kind, raw_path,
        namespace=ns, api_group=api_group, resource_kind=resource_kind,
        resource_name=resource_name, has_wildcard=wildcard,
    )
