import unittest
from app import ReActAgent, ToolRegistry

class TestReAct(unittest.TestCase):
    def test_tool_loop(self):
        reg = ToolRegistry()
        reg.register("vat", lambda a: str(round(a["net"] * 1.27)))
        def planner(goal, trace):
            if not trace:
                return {"thought": "ÁFA számítás kell", "tool": "vat", "args": {"net": 10000}}
            return {"thought": "Megvan az összeg", "final_answer": f"Bruttó: {trace[-1].observation} Ft"}
        res = ReActAgent(reg, planner).run("Számold ki 10000 Ft bruttóját")
        self.assertEqual(res["answer"], "Bruttó: 12700 Ft")
        self.assertEqual(res["steps"], 2)

if __name__ == "__main__":
    unittest.main()
