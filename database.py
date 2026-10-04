import datetime
from pathlib import Path
import sqlite3

class Database:
    def __init__(self, db_path: str | Path = "habits.db") -> None:
        self.db_path = str(db_path)
        self.init.db()

    def _get_connection(self) ->sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """ Creates tables and indexes fi they do not already exist. """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Habits table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    category TEXT DEFAULT 'General',
                    created_at TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1
                )
                """
            )

            # Daily logs tables
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    logged_date TEXT NOT NULL,
                    completed_at TEXT NOT NULL,
                    UNIQUE(habit_id, logged_date),
                    FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
                )
                """
            )

            # Indexes dor analytical performance
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_logs_date ON logs (logged_date)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_habit_history "
                "ON logs (habit_id, logged_date DESC)"
            )
            conn.commit()

    def add_habit(self, name: str, category: str = "General") -> bool:
        today = datetime.date.today().isoformat()
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO habits (name, category, created_at)
                    VALUES (?, ?, ?)
                    """,
                    (name.strip(), category.strip)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def mark_completed(self, habit_id: int, target_date: datetime.date | None = None) -> bool:
        if target_date is None:
            target_date = datetime.date.today()

        date_str = target_date.isoformat()
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO logs (habit_id, logged_date, completed_at)
                    VALUES (?, ?, ?)
                    """,
                    (habit_id, date_str, timestamp),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def get_activate_habits(self) -> list[sqlite3.Row]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, category, created_at "
                "FROM habits WHERE is_active = 1 "
                "ORDER BY id ASC"
            )
            return cursor.fetchall()