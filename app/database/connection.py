"""SQLite connection management for FitTrack."""
from contextlib import contextmanager
from pathlib import Path
import sqlite3

from app.database.schema import apply_migrations


class Database:
    """Owns the SQLite database file and applies schema migrations."""

    def __init__(self, db_path):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connect(self):
        """Open a transaction with foreign-key checks enabled."""
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self):
        """Create the migration ledger and apply pending migrations."""
        with self.connect() as connection:
            apply_migrations(connection)
