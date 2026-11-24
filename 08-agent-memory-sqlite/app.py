"""Perzisztens SQLite-alapú epizodikus és szemantikus AI-ügynök memória."""
import sqlite3
from dataclasses import dataclass


@dataclass
class MemoryItem:
    id: int
    session_id: str
    kind: str
    content: str
    importance: int


class AgentMemoryStore:
    def __init__(self, db_path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                content TEXT NOT NULL,
                importance INTEGER NOT NULL DEFAULT 5
            )"""
        )
        self.conn.commit()

    def remember(self, session_id: str, kind: str, content: str, importance: int = 5) -> int:
        cur = self.conn.execute(
            "INSERT INTO memories (session_id, kind, content, importance) VALUES (?, ?, ?, ?)",
            (session_id, kind, content, importance),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def recall(self, session_id: str, keyword: str = "", limit: int = 5) -> list[MemoryItem]:
        if keyword:
            rows = self.conn.execute(
                "SELECT id, session_id, kind, content, importance FROM memories WHERE session_id = ? AND lower(content) LIKE ? ORDER BY importance DESC, id DESC LIMIT ?",
                (session_id, f"%{keyword.lower()}%", limit),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT id, session_id, kind, content, importance FROM memories WHERE session_id = ? ORDER BY importance DESC, id DESC LIMIT ?",
                (session_id, limit),
            ).fetchall()
        return [MemoryItem(*r) for r in rows]

    def prune(self, session_id: str, keep_top: int = 10) -> int:
        cur = self.conn.execute(
            """DELETE FROM memories WHERE session_id = ? AND id NOT IN (
                SELECT id FROM memories WHERE session_id = ? ORDER BY importance DESC, id DESC LIMIT ?
            )""",
            (session_id, session_id, keep_top),
        )
        self.conn.commit()
        return cur.rowcount
