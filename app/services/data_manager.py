"""Basic export and deletion operations for local FitTrack data."""
import json
from datetime import datetime, timezone
from pathlib import Path


class DataManager:
    """Exports local SQLite records and deletes user-owned records."""

    def __init__(self, database):
        self.database = database

    def export_json(self, destination):
        """Write a portable JSON export and return the resulting path."""
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with self.database.connect() as connection:
            table_names = [
                row["name"] for row in connection.execute(
                    """
                    SELECT name FROM sqlite_master
                    WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
                      AND name != 'schema_migrations'
                    ORDER BY name
                    """
                )
            ]
            tables = {}
            for table_name in table_names:
                rows = connection.execute(
                    f'SELECT * FROM "{table_name}"'
                ).fetchall()
                tables[table_name] = [dict(row) for row in rows]

            version_row = connection.execute(
                "SELECT COALESCE(MAX(version), 0) AS version "
                "FROM schema_migrations"
            ).fetchone()

        payload = {
            "app": "FitTrack",
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "schema_version": version_row["version"],
            "tables": tables,
        }
        temporary_path = destination.with_suffix(destination.suffix + ".tmp")
        temporary_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary_path.replace(destination)
        return destination

    def delete_all_data(self):
        """Delete all user records while preserving schema migrations."""
        with self.database.connect() as connection:
            connection.execute("DELETE FROM users")
