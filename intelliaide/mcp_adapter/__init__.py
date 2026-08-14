"""MCP Bridging Adapter for IntelliAide.

Translates must-gather file paths into MCP tool calls over HTTP,
populating a local cache so DataAnalyzer can read files as if they
were mounted locally.
"""

from .adapter import MCPMustGatherAdapter

__all__ = ["MCPMustGatherAdapter"]
