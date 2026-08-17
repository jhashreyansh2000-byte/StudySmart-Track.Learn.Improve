"""
StudySmart — database layer.

Handles the SQLite connection and one-time table setup for user accounts.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "users.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_column(conn, table, column, ddl):
    """Add a column to an existing table if it isn't there yet. Lets us
    evolve the schema (profile fields, theme) without forcing everyone to
    delete users.db every time a new feature ships."""
    cols = [r["name"] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {ddl}")


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE
        )
    """)
    # Profile & preferences (Settings page). Added via migration so existing
    # installs pick these up automatically instead of needing a fresh DB.
    _ensure_column(conn, "users", "full_name", "full_name TEXT")
    _ensure_column(conn, "users", "class_name", "class_name TEXT")
    _ensure_column(conn, "users", "avatar", "avatar TEXT NOT NULL DEFAULT '🎓'")
    _ensure_column(conn, "users", "theme", "theme TEXT NOT NULL DEFAULT 'system'")
    _ensure_column(conn, "users", "xp", "xp INTEGER NOT NULL DEFAULT 0")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            chapters_total INTEGER NOT NULL DEFAULT 1,
            chapters_done INTEGER NOT NULL DEFAULT 0,
            color TEXT NOT NULL DEFAULT 'purple'
        )
    """)
    # Every completed timer (Pomodoro or stopwatch) is logged here. This is
    # what the dashboard's "Study Hours" graph and streak are computed from,
    # instead of the old hardcoded demo numbers.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            subject_id INTEGER,
            subject_name TEXT,
            chapter_name TEXT,
            mode TEXT NOT NULL DEFAULT 'stopwatch',
            planned_minutes INTEGER,
            duration_seconds INTEGER NOT NULL,
            started_at TEXT NOT NULL
        )
    """)
    # Named, individually-checkable chapters per subject. This is separate
    # from subjects.chapters_total/chapters_done (the quick +/- counter on
    # the Subjects page) -- that counter still works on its own. This table
    # is the detailed "actually name each chapter" tracker.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            subject_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            subject_id INTEGER,
            subject_name TEXT,
            name TEXT NOT NULL,
            score REAL NOT NULL,
            max_score REAL NOT NULL DEFAULT 100,
            test_date TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            subject_id INTEGER,
            subject_name TEXT,
            title TEXT NOT NULL,
            due_date TEXT,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            subject_id INTEGER,
            subject_name TEXT,
            att_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'present'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            target_date TEXT,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            subject_id INTEGER,
            subject_name TEXT,
            title TEXT NOT NULL,
            body TEXT,
            created_at TEXT NOT NULL
        )
    """)
    # Calendar / Exam Planner — dated entries with a live day countdown.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            subject_id INTEGER,
            subject_name TEXT,
            title TEXT NOT NULL,
            exam_date TEXT NOT NULL
        )
    """)
    # One row per user, only while a Study Sessions timer is running/paused.
    # Storing real timestamps (not a live countdown) is what lets the timer
    # survive navigating away, closing the tab, or refreshing -- the
    # server always knows the true elapsed time and can reconstruct
    # exactly where the timer should be, even across a pomodoro phase
    # change that happened while nobody was looking at the page.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS active_sessions (
            username TEXT PRIMARY KEY,
            subject_id INTEGER,
            subject_name TEXT,
            chapter_name TEXT,
            mode TEXT NOT NULL DEFAULT 'stopwatch',
            work_minutes INTEGER,
            break_minutes INTEGER,
            phase TEXT NOT NULL DEFAULT 'work',
            phase_elapsed_seconds INTEGER NOT NULL DEFAULT 0,
            accumulated_work_seconds INTEGER NOT NULL DEFAULT 0,
            running INTEGER NOT NULL DEFAULT 1,
            run_started_at TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()