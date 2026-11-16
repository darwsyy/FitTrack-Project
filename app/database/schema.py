"""Versioned SQLite schema migrations."""
from datetime import datetime, timezone

LATEST_SCHEMA_VERSION = 1


def _migration_1(connection):
    """Create the local user, profile, and optional measurement tables."""
    statements = (
        """
        CREATE TABLE users (
            id TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE user_profiles (
            user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
            experience_level TEXT NOT NULL DEFAULT 'unspecified'
                CHECK (experience_level IN
                    ('unspecified', 'beginner', 'intermediate', 'advanced')),
            preferred_training_mode TEXT NOT NULL DEFAULT 'both'
                CHECK (preferred_training_mode IN ('gym', 'home', 'both')),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE body_measurements (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            measured_at TEXT NOT NULL,
            height_cm REAL,
            weight_kg REAL,
            note TEXT,
            created_at TEXT NOT NULL,
            CHECK (height_cm IS NULL OR height_cm > 0),
            CHECK (weight_kg IS NULL OR weight_kg > 0),
            CHECK (height_cm IS NOT NULL OR weight_kg IS NOT NULL)
        )
        """,
        """
        CREATE INDEX idx_body_measurements_user_date
            ON body_measurements(user_id, measured_at DESC)
        """,
        """
        CREATE TABLE user_settings (
            user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
            theme TEXT NOT NULL DEFAULT 'system'
                CHECK (theme IN ('system', 'light', 'dark')),
            distance_unit TEXT NOT NULL DEFAULT 'km',
            weight_unit TEXT NOT NULL DEFAULT 'kg',
            notifications_enabled INTEGER NOT NULL DEFAULT 1,
            gps_privacy_mode TEXT NOT NULL DEFAULT 'local_only',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
    )
    for statement in statements:
        connection.execute(statement)


MIGRATIONS = {1: _migration_1}


def apply_migrations(connection):
    """Apply every migration newer than the recorded schema version."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            applied_at TEXT NOT NULL
        )
        """
    )
    row = connection.execute(
        "SELECT COALESCE(MAX(version), 0) AS version FROM schema_migrations"
    ).fetchone()
    current_version = row["version"]

    for version in sorted(MIGRATIONS):
        if version <= current_version:
            continue
        MIGRATIONS[version](connection)
        connection.execute(
            "INSERT INTO schema_migrations(version, applied_at) VALUES (?, ?)",
            (version, datetime.now(timezone.utc).isoformat()),
        )
