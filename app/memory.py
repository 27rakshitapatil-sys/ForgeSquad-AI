import sqlite3
from datetime import datetime

DB_FILE = "memory.db"


def _connect():
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS runs ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "created_at TEXT, "
        "goal TEXT, "
        "result TEXT)"
    )
    return conn


def save_run(goal: str, result: str):
    conn = _connect()
    conn.execute(
        "INSERT INTO runs (created_at, goal, result) VALUES (?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), goal, result),
    )
    conn.commit()
    conn.close()


def get_runs(limit: int = 5):
    conn = _connect()
    rows = conn.execute(
        "SELECT created_at, goal, result FROM runs ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return rows
    

def find_related(goal: str, limit: int = 2):
    """Find past runs whose goal shares words with the new goal."""
    words = [w.lower() for w in goal.split() if len(w) > 4]
    if not words:
        return []
    conn = _connect()
    rows = conn.execute(
        "SELECT goal, result FROM runs ORDER BY id DESC LIMIT 50"
    ).fetchall()
    conn.close()
    scored = []
    for past_goal, result in rows:
        score = sum(1 for w in words if w in past_goal.lower())
        if score > 0:
            scored.append((score, past_goal, result))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [(g, r) for _, g, r in scored[:limit]]