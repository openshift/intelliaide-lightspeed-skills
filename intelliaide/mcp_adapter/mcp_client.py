"""MCP HTTP client for calling must-gather MCP server tools.

Uses raw HTTP with the requests library (already vendored) to make
JSON-RPC 2.0 calls over the MCP Streamable HTTP transport. No external
MCP SDK dependency required.
"""

import json
import os
import sys
from typing import Any, Dict, Optional

_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_VENDOR_DIR = os.path.join(_SKILL_DIR, "vendor")
if _VENDOR_DIR not in sys.path:
    sys.path.insert(0, _VENDOR_DIR)

import requests  # noqa: E402


_DEFAULT_TIMEOUT = 120
_MAX_RETRIES = 2


class MCPClientError(Exception):
    """Raised when an MCP tool call fails."""

    def __init__(self, message: str, code: Optional[int] = None, tool: str = ""):
        super().__init__(message)
        self.code = code
        self.tool = tool


class MCPClient:
    """Synchronous HTTP client for MCP Streamable HTTP transport.

    Handles session initialization, tool calls, and resource reads
    against the must-gather-mcp server.
    """

    def __init__(self, mcp_url: str, timeout: int = _DEFAULT_TIMEOUT):
        self._url = mcp_url.rstrip("/")
        self._timeout = timeout
        self._session_id: Optional[str] = None
        self._request_id = 0
        self._http = requests.Session()
        self._http.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        })
        self._initialized = False

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _send_jsonrpc(self, method: str, params: Optional[Dict] = None) -> Any:
        """Send a JSON-RPC 2.0 request and return the result."""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self._next_id(),
        }
        if params is not None:
            payload["params"] = params

        headers = {}
        if self._session_id:
            headers["Mcp-Session-Id"] = self._session_id

        last_error = None
        for attempt in range(_MAX_RETRIES + 1):
            try:
                resp = self._http.post(
                    self._url,
                    json=payload,
                    headers=headers,
                    timeout=self._timeout,
                )
                break
            except requests.exceptions.Timeout:
                last_error = MCPClientError(
                    f"Timeout after {self._timeout}s calling {method}", tool=method
                )
                if attempt == _MAX_RETRIES:
                    raise last_error
            except requests.exceptions.ConnectionError as e:
                last_error = MCPClientError(
                    f"Connection error calling {method}: {e}", tool=method
                )
                if attempt == _MAX_RETRIES:
                    raise last_error

        if resp.status_code >= 400:
            raise MCPClientError(
                f"HTTP {resp.status_code} from MCP server: {resp.text[:500]}",
                code=resp.status_code,
                tool=method,
            )

        # Capture session ID from response headers
        session_id = resp.headers.get("Mcp-Session-Id")
        if session_id:
            self._session_id = session_id

        content_type = resp.headers.get("Content-Type", "")

        # Handle SSE responses (text/event-stream)
        if "text/event-stream" in content_type:
            return self._parse_sse_response(resp.text)

        # Standard JSON response
        try:
            data = resp.json()
        except (json.JSONDecodeError, ValueError):
            raise MCPClientError(
                f"Invalid JSON response from {method}: {resp.text[:200]}",
                tool=method,
            )

        if "error" in data:
            err = data["error"]
            raise MCPClientError(
                err.get("message", "Unknown MCP error"),
                code=err.get("code"),
                tool=method,
            )

        return data.get("result")

    def _parse_sse_response(self, text: str) -> Any:
        """Parse Server-Sent Events response, extracting the JSON-RPC result."""
        result = None
        for line in text.splitlines():
            if line.startswith("data: "):
                data_str = line[6:]
                try:
                    data = json.loads(data_str)
                    if "result" in data:
                        result = data["result"]
                    elif "error" in data:
                        err = data["error"]
                        raise MCPClientError(
                            err.get("message", "Unknown MCP error"),
                            code=err.get("code"),
                        )
                except json.JSONDecodeError:
                    continue
        return result

    def initialize(self) -> None:
        """Perform MCP session initialization handshake."""
        if self._initialized:
            return

        result = self._send_jsonrpc("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "intelliaide-mcp-adapter",
                "version": "1.0.0",
            },
        })

        # Send initialized notification (no id, no response expected)
        notify_payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
        }
        headers = {}
        if self._session_id:
            headers["Mcp-Session-Id"] = self._session_id
        try:
            self._http.post(
                self._url,
                json=notify_payload,
                headers=headers,
                timeout=10,
            )
        except Exception:
            pass

        self._initialized = True
        return result

    def call_tool(self, tool_name: str, arguments: Optional[Dict] = None) -> str:
        """Call an MCP tool and return the text content.

        Returns the concatenated text content from the tool response.
        Raises MCPClientError on failure.
        """
        if not self._initialized:
            self.initialize()

        params = {"name": tool_name}
        if arguments:
            params["arguments"] = arguments

        result = self._send_jsonrpc("tools/call", params)

        if result is None:
            return ""

        # Extract text content from MCP tool result
        if isinstance(result, dict):
            content_list = result.get("content", [])
            if result.get("isError"):
                error_text = ""
                for item in content_list:
                    if isinstance(item, dict) and item.get("type") == "text":
                        error_text += item.get("text", "")
                raise MCPClientError(
                    error_text or "Tool returned isError=true",
                    tool=tool_name,
                )
            texts = []
            for item in content_list:
                if isinstance(item, dict) and item.get("type") == "text":
                    texts.append(item.get("text", ""))
            return "\n".join(texts)

        return str(result)

    def read_resource(self, uri: str) -> str:
        """Read an MCP resource by URI and return the text content."""
        if not self._initialized:
            self.initialize()

        result = self._send_jsonrpc("resources/read", {"uri": uri})

        if result is None:
            return ""

        if isinstance(result, dict):
            contents = result.get("contents", [])
            texts = []
            for item in contents:
                if isinstance(item, dict):
                    text = item.get("text", "")
                    if text:
                        texts.append(text)
            return "\n".join(texts)

        return str(result)

    def close(self) -> None:
        """Close the HTTP session."""
        self._http.close()


def get_mcp_url() -> str:
    """Extract MCP server URL from environment variables.

    Checks (in order):
      1. MCP_SERVER_URL (direct URL)
      2. LIGHTSPEED_MCP_SERVERS (JSON config from sandbox)
    """
    direct = os.environ.get("MCP_SERVER_URL", "").strip()
    if direct:
        return direct

    servers_json = os.environ.get("LIGHTSPEED_MCP_SERVERS", "").strip()
    if servers_json:
        try:
            servers = json.loads(servers_json)
            if isinstance(servers, list):
                for srv in servers:
                    if isinstance(srv, dict) and srv.get("name") == "must-gather":
                        return srv.get("url", "")
            elif isinstance(servers, dict):
                return servers.get("url", "")
        except (json.JSONDecodeError, TypeError):
            pass

    return ""
