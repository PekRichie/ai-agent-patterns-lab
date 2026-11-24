"""Szabványos MCP (Model Context Protocol) JSON-RPC 2.0 szerver minta."""
from typing import Callable


class MiniMcpServer:
    def __init__(self, name: str = "cuppashot-mcp", version: str = "1.0.0") -> None:
        self.name = name
        self.version = version
        self._tools: dict[str, tuple[str, Callable[[dict], str]]] = {}

    def tool(self, name: str, description: str):
        def deco(fn: Callable[[dict], str]):
            self._tools[name] = (description, fn)
            return fn
        return deco

    def handle(self, req: dict) -> dict:
        rid = req.get("id")
        method = req.get("method")
        params = req.get("params") or {}
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": rid, "result": {"serverInfo": {"name": self.name, "version": self.version}, "capabilities": {"tools": {}}}}
        if method == "tools/list":
            tools = [{"name": k, "description": d} for k, (d, _) in self._tools.items()]
            return {"jsonrpc": "2.0", "id": rid, "result": {"tools": tools}}
        if method == "tools/call":
            tname = params.get("name")
            if tname not in self._tools:
                return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": f"Unknown tool: {tname}"}}
            _, fn = self._tools[tname]
            out = fn(params.get("arguments") or {})
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": out}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": f"Method not found: {method}"}}
