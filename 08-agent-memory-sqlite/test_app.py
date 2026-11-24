import unittest
from app import AgentMemoryStore


class TestAgentMemory(unittest.TestCase):
    def test_remember_recall_and_prune(self):
        mem = AgentMemoryStore()
        mem.remember("s1", "fact", "Richárd Miskolcon él és 100% remote állást keres.", importance=9)
        mem.remember("s1", "note", "Apró ideiglenes jegyzet", importance=1)
        mem.remember("s2", "fact", "Másik munkamenet adata", importance=10)
        hits = mem.recall("s1", keyword="miskolcon")
        self.assertEqual(len(hits), 1)
        removed = mem.prune("s1", keep_top=1)
        self.assertEqual(removed, 1)
        self.assertEqual(len(mem.recall("s1")), 1)


if __name__ == "__main__":
    unittest.main()
