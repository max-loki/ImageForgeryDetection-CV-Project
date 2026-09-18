import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "history.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS analysis_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        candidate_matches INTEGER,
        verified_matches INTEGER,
        suspicious_regions INTEGER,
        score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    return conn


def save_analysis(filename, candidate_matches, verified_matches, suspicious_regions, score):
    conn = get_connection()
    conn.execute(
        "INSERT INTO analysis_history(filename,candidate_matches,verified_matches,suspicious_regions,score) VALUES (?,?,?,?,?)",
        (filename, candidate_matches, verified_matches, suspicious_regions, score),
    )
    conn.commit()
    conn.close()


def recent_analyses(limit=10):
    conn = get_connection()
    rows = conn.execute(
        "SELECT filename,candidate_matches,verified_matches,suspicious_regions,score,created_at FROM analysis_history ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return rows
