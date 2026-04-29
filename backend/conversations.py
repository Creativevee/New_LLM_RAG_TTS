import json
import sqlite3
import time
import uuid
from typing import Dict, List, Optional

from config import CONVO_DB_PATH

_SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (
    id          TEXT PRIMARY KEY,
    title       TEXT NOT NULL,
    created_at  REAL NOT NULL,
    updated_at  REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS messages (
    id              TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    role            TEXT NOT NULL,
    content         TEXT NOT NULL,
    sources         TEXT,
    audio_url       TEXT,
    created_at      REAL NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_msg_conv
    ON messages(conversation_id, created_at);
"""


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(CONVO_DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _init_db() -> None:
    with _connect() as conn:
        conn.executescript(_SCHEMA)


_init_db()


def _now() -> float:
    return time.time()


def _new_id() -> str:
    return uuid.uuid4().hex


def create_conversation(title: str = "New conversation") -> Dict:
    cid = _new_id()
    t = _now()
    title = (title or "").strip() or "New conversation"
    with _connect() as conn:
        conn.execute(
            "INSERT INTO conversations (id, title, created_at, updated_at)"
            " VALUES (?, ?, ?, ?)",
            (cid, title, t, t),
        )
    return {"id": cid, "title": title, "created_at": t, "updated_at": t}


def list_conversations() -> List[Dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT c.id, c.title, c.created_at, c.updated_at,"
            " (SELECT COUNT(*) FROM messages m WHERE m.conversation_id = c.id) AS message_count"
            " FROM conversations c"
            " ORDER BY c.updated_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def conversation_exists(conversation_id: str) -> bool:
    with _connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM conversations WHERE id = ?", (conversation_id,)
        ).fetchone()
    return row is not None


def conversation_message_count(conversation_id: str) -> int:
    with _connect() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM messages WHERE conversation_id = ?",
            (conversation_id,),
        ).fetchone()
    return int(row["n"]) if row else 0


def rename_conversation(conversation_id: str, title: str) -> bool:
    title = (title or "").strip() or "Untitled"
    with _connect() as conn:
        cur = conn.execute(
            "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
            (title, _now(), conversation_id),
        )
    return cur.rowcount > 0


def delete_conversation(conversation_id: str) -> bool:
    with _connect() as conn:
        cur = conn.execute(
            "DELETE FROM conversations WHERE id = ?", (conversation_id,)
        )
    return cur.rowcount > 0


def make_title(text: str, max_chars: int = 60) -> str:
    text = " ".join((text or "").split())
    if not text:
        return "New conversation"
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


def get_conversation(conversation_id: str) -> Optional[Dict]:
    with _connect() as conn:
        conv = conn.execute(
            "SELECT id, title, created_at, updated_at FROM conversations WHERE id = ?",
            (conversation_id,),
        ).fetchone()
        if not conv:
            return None
        rows = conn.execute(
            "SELECT id, role, content, sources, audio_url, created_at"
            " FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
            (conversation_id,),
        ).fetchall()
    msgs = []
    for r in rows:
        d = dict(r)
        d["sources"] = json.loads(d["sources"]) if d.get("sources") else []
        msgs.append(d)
    return {**dict(conv), "messages": msgs}


def add_message(
    conversation_id: str,
    role: str,
    content: str,
    sources: Optional[List[Dict]] = None,
    audio_url: Optional[str] = None,
) -> Dict:
    mid = _new_id()
    t = _now()
    sources_json = json.dumps(sources or [])
    with _connect() as conn:
        conn.execute(
            "INSERT INTO messages"
            " (id, conversation_id, role, content, sources, audio_url, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (mid, conversation_id, role, content, sources_json, audio_url, t),
        )
        conn.execute(
            "UPDATE conversations SET updated_at = ? WHERE id = ?",
            (t, conversation_id),
        )
    return {
        "id": mid,
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "sources": sources or [],
        "audio_url": audio_url,
        "created_at": t,
    }
