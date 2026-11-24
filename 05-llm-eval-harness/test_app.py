import unittest
from app import EvalCase, run_eval

class TestEval(unittest.TestCase):
    def test_harness(self):
        cases = [
            EvalCase("c1", "Mi a MAGMA?", must_contain=["SaaS", "moduláris"], must_not_contain=["hallucináció"]),
            EvalCase("c2", "Rövid válasz", must_contain=["OK"], max_chars=20),
        ]
        rep = run_eval(cases, lambda p: "MAGMA egy moduláris SaaS platform." if "MAGMA" in p else "OK")
        self.assertEqual(rep["score_pct"], 100.0)

if __name__ == "__main__":
    unittest.main()
