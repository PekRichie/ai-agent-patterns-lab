import unittest
from app import MultiAgentOrchestrator

class TestOrch(unittest.TestCase):
    def test_revision_loop(self):
        orch = MultiAgentOrchestrator(
            planner=lambda g: ["spec", "code", "test"],
            builder=lambda ctx: "v1_no_tests" if ctx.rounds == 1 else "v2_with_tests",
            reviewer=lambda ctx: ("with_tests" in ctx.artifact, "OK" if "with_tests" in ctx.artifact else "Hiányzik a teszt"),
        )
        res = orch.execute("Build feature")
        self.assertTrue(res.approved)
        self.assertEqual(res.rounds, 2)

if __name__ == "__main__":
    unittest.main()
