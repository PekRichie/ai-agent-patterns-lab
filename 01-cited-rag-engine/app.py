"""Hivatkozásos mini-RAG motor (chunking + BM25 retrieval + citation verification)."""
import math
import re
from collections import Counter
from dataclasses import dataclass


@dataclass
class Chunk:
    chunk_id: str
    source: str
    text: str


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-ZáéíóöőúüűÁÉÍÓÖŐÚÜŰ0-9]+", text.lower())


def chunk_document(source: str, text: str, max_words: int = 40, overlap: int = 8) -> list[Chunk]:
    words = text.split()
    chunks: list[Chunk] = []
    step = max(1, max_words - overlap)
    for i in range(0, len(words), step):
        part = " ".join(words[i : i + max_words])
        if part:
            chunks.append(Chunk(chunk_id=f"{source}#c{len(chunks)+1}", source=source, text=part))
        if i + max_words >= len(words):
            break
    return chunks


class CitedRagEngine:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.tokens = [tokenize(c.text) for c in chunks]
        self.avgdl = sum(len(t) for t in self.tokens) / max(1, len(chunks))
        self.df: Counter[str] = Counter()
        for toks in self.tokens:
            for w in set(toks):
                self.df[w] += 1

    def retrieve(self, query: str, top_k: int = 2) -> list[tuple[Chunk, float]]:
        q = tokenize(query)
        n = len(self.chunks)
        scored: list[tuple[Chunk, float]] = []
        for c, toks in zip(self.chunks, self.tokens):
            tf = Counter(toks)
            score = 0.0
            for term in q:
                if term not in tf:
                    continue
                idf = math.log((n - self.df[term] + 0.5) / (self.df[term] + 0.5) + 1.0)
                f = tf[term]
                score += idf * (f * 2.5) / (f + 1.5 * (0.25 + 0.75 * len(toks) / max(1e-9, self.avgdl)))
            if score > 0:
                scored.append((c, round(score, 4)))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def answer_with_citations(self, query: str) -> dict[str, object]:
        hits = self.retrieve(query, top_k=2)
        if not hits:
            return {"answer": "Nem található forrás a kérdés megválaszolásához.", "citations": []}
        citations = [c.chunk_id for c, _ in hits]
        summary = " ".join(f"[{c.chunk_id}] {c.text}" for c, _ in hits)
        return {"answer": summary, "citations": citations}
