#!/usr/bin/env python3
"""
extract_cluster.py — Step 1 of IntelliAide pure-skills pipeline (LLM-free).

Reads diagnostic data from a specified directory (default: /data/input) and
validates it. The data directory can be overridden via --data-dir to point to
wherever the must-gather output was collected (e.g. /tmp/must-gather-output
when the agent runs `oc adm must-gather` inside the sandbox).

The cluster_dir in state.json is the deepest directory that serves as the
logical root for downstream file resolution. Single-child wrapper directories
are unwrapped so cluster_dir lands as close to the real data as possible.
No assumptions are made about the internal layout — downstream
DataAnalyzer._resolve_path handles path expansion with glob wildcards for
any directory structure.

Usage:
    # With default data directory (/data/input):
    python /app/skills/intelliaide/extract_cluster.py --query "etcd pods not ready"

    # With custom data directory (e.g. after oc adm must-gather):
    python /app/skills/intelliaide/extract_cluster.py --query "etcd pods not ready" \\
        --data-dir /tmp/must-gather-output

    # Reuse an existing job dir (skips validation)
    python /app/skills/intelliaide/extract_cluster.py --query "..." --job-dir /tmp/intelliaide/abc123

Output (stdout JSON):
    {
      "job_id":      "<8-char id>",
      "job_dir":     "/tmp/intelliaide/<job_id>",
      "cluster_dir": "<data-dir>/...",
      "mode":        "must-gather",
      "success":     true,
      "return_code": 0
    }

On failure the script prints JSON with success=false and exits with code 1 so
the orchestrating agent stops immediately rather than proceeding with no data.
"""

import argparse
import json
import sys
import uuid
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent
for _p in (str(_SKILL_DIR),):
    if _p not in sys.path:
        sys.path.insert(0, _p)

_JOB_BASE  = "/tmp/intelliaide"

_DEFAULT_DATA_DIR = "/data/input"


def _mcp_configured() -> bool:
    """Return True when an MCP server is available to fetch data on demand.

    In MCP mode the data directory legitimately starts out empty/near-empty
    — files are fetched lazily by analyze_data.py's adapter in Step 3, not
    pre-populated on the PVC/filesystem. The local-file-count validation
    below only makes sense for the non-MCP (locally mounted must-gather)
    path, so it must be skipped here.
    """
    try:
        from mcp_adapter.mcp_client import get_mcp_url
        return bool(get_mcp_url())
    except Exception:
        return False


def _log_pod(msg: str) -> None:
    """Write a progress line directly to the container log stream (PID 1 stdout).

    Skill scripts run as subprocesses of the Claude Code CLI whose stdout is
    piped internally — it never reaches the pod log stream.  Opening PID 1's
    stdout directly is the only way to surface progress in `oc logs`.
    Falls back silently if the file is not accessible.
    """
    line = f"[intelliaide] {msg}\n"
    try:
        with open("/proc/1/fd/1", "a") as fh:
            fh.write(line)
    except Exception:
        sys.stderr.write(line)


_SKIP_DIRS = frozenset({"lost+found"})

_MIN_DATA_FILES = 3

_MAX_UNWRAP_DEPTH = 4


def _real_entries(parent: Path) -> "list[Path]":
    """List children of *parent*, skipping lost+found and hidden entries."""
    try:
        return sorted(
            p for p in parent.iterdir()
            if p.name not in _SKIP_DIRS and not p.name.startswith(".")
        )
    except OSError:
        return []


def _unwrap_single_child_dirs(raw_dir: Path) -> Path:
    """Walk single-child wrapper directories to reach the actual data root.

    Many diagnostic bundles wrap content in one or more levels of a single
    subdirectory (e.g. /data/input/bundle-abc123/cluster-dump/...).  This
    traverses down as long as a directory has exactly one real child that is
    itself a directory, stopping when the directory fans out or max depth is
    reached.
    """
    current = raw_dir
    for _ in range(_MAX_UNWRAP_DEPTH):
        children = _real_entries(current)
        dirs = [c for c in children if c.is_dir()]
        if len(dirs) == 1 and len(children) == 1:
            current = dirs[0]
        else:
            break
    return current


def _total_files(entries: "list[Path]") -> int:
    """Count files across all top-level entries (dirs and regular files)."""
    total = 0
    for entry in entries:
        if entry.is_file():
            total += 1
        elif entry.is_dir():
            total += sum(1 for _ in entry.rglob("*") if _.is_file())
    return total


def _check_data_source(data_input_dir: Path) -> "tuple[Path, bool, str]":
    """Validate the data input directory and return the data root for downstream resolution.

    Checks: mount exists, is readable, is non-empty, has enough files.
    Then unwraps single-child wrapper directories so cluster_dir is as close
    to the real data as possible.

    Returns (cluster_dir, success, error_message).
    """
    mcp_mode = _mcp_configured()

    # In MCP mode, the cache directory is expected to start out empty (or
    # only contain a handful of previously-fetched files) — data is pulled
    # on demand in Step 3. Skip the pre-population checks below entirely
    # and use the data dir itself as cluster_dir, so a near-empty directory
    # doesn't get mistaken for a "single-child wrapper" and doesn't need to
    # be artificially seeded just to pass validation here.
    if mcp_mode:
        data_input_dir.mkdir(parents=True, exist_ok=True)
        return data_input_dir, True, ""

    if not data_input_dir.exists():
        return data_input_dir, False, (
            f"No data source found at {data_input_dir}. "
            "Ensure the data directory exists and contains diagnostic data."
        )

    try:
        list(data_input_dir.iterdir())
    except OSError as exc:
        return data_input_dir, False, (
            f"Cannot read {data_input_dir}: {exc}. "
            "Check directory permissions and content."
        )

    real = _real_entries(data_input_dir)
    if not real:
        return data_input_dir, False, (
            f"Data source at {data_input_dir} is empty (only lost+found). "
            "Ensure the directory contains diagnostic data."
        )

    total_files = _total_files(real)
    if total_files < _MIN_DATA_FILES:
        return data_input_dir, False, (
            f"Data source at {data_input_dir} has too few files ({total_files}). "
            "Ensure the directory contains a complete diagnostic bundle."
        )

    data_root = _unwrap_single_child_dirs(data_input_dir)
    return data_root, True, ""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True,
                        help="Problem statement for RCA (passed through to state.json)")
    parser.add_argument("--job-dir", default=None,
                        help="Reuse an existing job dir (skips validation, updates state.json)")
    parser.add_argument("--data-dir", default=_DEFAULT_DATA_DIR,
                        help="Path to must-gather data (default: /data/input)")
    args = parser.parse_args()

    data_input_dir = Path(args.data_dir)

    if args.job_dir:
        job_dir = Path(args.job_dir)
        job_id  = job_dir.name
    else:
        job_id  = str(uuid.uuid4())[:8]
        job_dir = Path(_JOB_BASE) / job_id

    job_dir.mkdir(parents=True, exist_ok=True)

    mode = "must-gather"

    if args.job_dir:
        cluster_dir, success, error_msg = _check_data_source(data_input_dir)
    else:
        _log_pod(f"Step 1/4 — extract_cluster  job_id={job_id}  mode=must-gather")
        print(f"[extract_cluster] job_id={job_id}  mode=must-gather", file=sys.stderr)

        _log_pod(f"Step 1/4 — checking data source at {data_input_dir}")
        cluster_dir, success, error_msg = _check_data_source(data_input_dir)

    state = {
        "job_id":      job_id,
        "job_dir":     str(job_dir),
        "cluster_dir": str(cluster_dir),
        "query":       args.query,
        "mode":        mode,
    }
    (job_dir / "state.json").write_text(json.dumps(state, indent=2))

    if not success:
        _log_pod(f"Step 1/4 — extract_cluster FAILED: {error_msg}")
        print(json.dumps({
            "job_id":        job_id,
            "job_dir":       str(job_dir),
            "cluster_dir":   str(cluster_dir),
            "mode":          mode,
            "success":       False,
            "return_code":   1,
            "error":         error_msg,
        }))
        sys.exit(1)

    _log_pod(f"Step 1/4 — extract_cluster done  mode={mode}  cluster_dir={cluster_dir}")
    print(f"[extract_cluster] Data source validated: {cluster_dir}", file=sys.stderr)
    print(json.dumps({
        "job_id":      job_id,
        "job_dir":     str(job_dir),
        "cluster_dir": str(cluster_dir),
        "mode":        mode,
        "success":     True,
        "return_code": 0,
    }))


if __name__ == "__main__":
    main()
