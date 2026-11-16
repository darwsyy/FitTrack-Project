"""Versioned SQLite schema migrations."""
from datetime import datetime, timezone

LATEST_SCHEMA_VERSION = 3


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



def _migration_2(connection):
    """Create exercise catalogue, workout templates, and session records."""
    statements = (
        """
        CREATE TABLE exercises (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            equipment TEXT NOT NULL DEFAULT 'none',
            training_mode TEXT NOT NULL
                CHECK (training_mode IN ('gym', 'home', 'both')),
            instructions TEXT NOT NULL DEFAULT '',
            is_active INTEGER NOT NULL DEFAULT 1
        )
        """,
        """
        CREATE TABLE workout_templates (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
            description TEXT NOT NULL DEFAULT '',
            training_mode TEXT NOT NULL
                CHECK (training_mode IN ('gym', 'home', 'both')),
            is_custom INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE template_exercises (
            id TEXT PRIMARY KEY,
            template_id TEXT NOT NULL
                REFERENCES workout_templates(id) ON DELETE CASCADE,
            exercise_id TEXT NOT NULL
                REFERENCES exercises(id) ON DELETE RESTRICT,
            sort_order INTEGER NOT NULL,
            UNIQUE(template_id, sort_order),
            UNIQUE(template_id, exercise_id)
        )
        """,
        """
        CREATE TABLE workout_sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            template_id TEXT REFERENCES workout_templates(id) ON DELETE SET NULL,
            name TEXT NOT NULL,
            training_mode TEXT NOT NULL
                CHECK (training_mode IN ('gym', 'home')),
            started_at TEXT NOT NULL,
            finished_at TEXT,
            notes TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'in_progress'
                CHECK (status IN ('in_progress', 'completed', 'cancelled'))
        )
        """,
        """
        CREATE TABLE workout_session_exercises (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL
                REFERENCES workout_sessions(id) ON DELETE CASCADE,
            exercise_id TEXT NOT NULL
                REFERENCES exercises(id) ON DELETE RESTRICT,
            sort_order INTEGER NOT NULL,
            notes TEXT NOT NULL DEFAULT '',
            UNIQUE(session_id, sort_order)
        )
        """,
        """
        CREATE TABLE workout_sets (
            id TEXT PRIMARY KEY,
            session_exercise_id TEXT NOT NULL
                REFERENCES workout_session_exercises(id) ON DELETE CASCADE,
            set_number INTEGER NOT NULL,
            reps INTEGER,
            weight_kg REAL,
            duration_seconds INTEGER,
            distance_m REAL,
            is_completed INTEGER NOT NULL DEFAULT 0,
            CHECK (reps IS NULL OR reps > 0),
            CHECK (weight_kg IS NULL OR weight_kg >= 0),
            CHECK (duration_seconds IS NULL OR duration_seconds > 0),
            CHECK (distance_m IS NULL OR distance_m > 0),
            CHECK (reps IS NOT NULL OR duration_seconds IS NOT NULL
                   OR distance_m IS NOT NULL),
            UNIQUE(session_exercise_id, set_number)
        )
        """,
        "CREATE INDEX idx_workout_sessions_user_date "
        "ON workout_sessions(user_id, started_at DESC)",
        "CREATE INDEX idx_workout_session_exercises_session "
        "ON workout_session_exercises(session_id, sort_order)",
        "CREATE INDEX idx_workout_sets_exercise "
        "ON workout_sets(session_exercise_id, set_number)",
    )
    for statement in statements:
        connection.execute(statement)


def _migration_3(connection):
    """Add ownership to workout templates created by the earlier v2 schema."""
    columns = {
        row["name"] for row in connection.execute(
            "PRAGMA table_info(workout_templates)"
        )
    }
    if "user_id" not in columns:
        connection.execute(
            "ALTER TABLE workout_templates ADD COLUMN user_id TEXT "
            "REFERENCES users(id) ON DELETE CASCADE"
        )


MIGRATIONS = {
    1: _migration_1,
    2: _migration_2,
    3: _migration_3,
}


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
