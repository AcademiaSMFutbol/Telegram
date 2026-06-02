import os
import sqlite3
from contextlib import contextmanager
from bot.config import DB_PATH


@contextmanager
def _db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with _db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                chat_id    INTEGER PRIMARY KEY,
                username   TEXT,
                first_name TEXT,
                joined_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active     INTEGER DEFAULT 1
            )
        """)


def subscribe(chat_id: int, username: str | None, first_name: str | None) -> bool:
    """Returns True if newly subscribed, False if already was active."""
    with _db() as conn:
        row = conn.execute(
            "SELECT active FROM subscribers WHERE chat_id = ?", (chat_id,)
        ).fetchone()
        if row and row[0] == 1:
            return False
        conn.execute(
            "INSERT INTO subscribers (chat_id, username, first_name, active) VALUES (?, ?, ?, 1) "
            "ON CONFLICT(chat_id) DO UPDATE SET active=1, username=excluded.username, first_name=excluded.first_name",
            (chat_id, username, first_name),
        )
        return True


def unsubscribe(chat_id: int) -> bool:
    """Returns True if was active, False if wasn't subscribed."""
    with _db() as conn:
        row = conn.execute(
            "SELECT active FROM subscribers WHERE chat_id = ?", (chat_id,)
        ).fetchone()
        if not row or row[0] == 0:
            return False
        conn.execute("UPDATE subscribers SET active=0 WHERE chat_id=?", (chat_id,))
        return True


def get_active_subscribers() -> list[int]:
    with _db() as conn:
        rows = conn.execute(
            "SELECT chat_id FROM subscribers WHERE active=1"
        ).fetchall()
        return [r[0] for r in rows]


def count_active() -> int:
    with _db() as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM subscribers WHERE active=1"
        ).fetchone()[0]
