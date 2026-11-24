import unittest
from app import MiniMcpServer

class TestMcp(unittest.TestCase):
    def test_mcp_protocol(self):
        srv = MiniMcpServer()
        @srv.tool("ping", "Egyszerű állapotellenőrzés")
        def ping(args):
            return f"pong:{args.get('msg', '')}"
        init = srv.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
        self.assertEqual(init["result"]["serverInfo"]["name"], "cuppashot-mcp")
        lst = srv.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        self.assertEqual(len(lst["result"]["tools"]), 1)
        call = srv.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "ping", "arguments": {"msg": "ok"}}})
        self.assertEqual(call["result"]["content"][0]["text"], "pong:ok")

if __name__ == "__main__":
    unittest.main()
