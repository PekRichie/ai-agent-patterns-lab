import unittest
from app import parse_with_repair


class TestStructuredOutput(unittest.TestCase):
    def test_fenced_and_repair_loop(self):
        attempts = [0]
        def fake_llm(feedback):
            attempts[0] += 1
            if attempts[0] == 1:
                return 'Íme a válasz: ```json\n{"title": "MAGMA"}\n```'
            return 'Javítva: ```json\n{"title": "MAGMA", "score": 95}\n```'

        res = parse_with_repair(fake_llm, {"title": str, "score": int}, max_retries=2)
        self.assertEqual(res, {"title": "MAGMA", "score": 95})
        self.assertEqual(attempts[0], 2)


if __name__ == "__main__":
    unittest.main()
