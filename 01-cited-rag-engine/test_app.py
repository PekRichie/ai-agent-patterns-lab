import unittest
from app import CitedRagEngine, chunk_document

class TestRag(unittest.TestCase):
    def test_cited_answer(self):
        chunks = chunk_document("magma.md", "A MAGMA egy moduláris SaaS platform csapatmenedzsmenthez és beosztástervezéshez.")
        chunks += chunk_document("borostyan.md", "A Borostyán egy közös AI memória és tudásgráf MCP szerverrel.")
        rag = CitedRagEngine(chunks)
        res = rag.answer_with_citations("Mire való a Borostyán MCP szerver?")
        self.assertIn("borostyan.md#c1", res["citations"])

if __name__ == "__main__":
    unittest.main()
