"""Persistence operations for the local user profile."""
from datetime import datetime, timezone
from uuid import uuid4

from app.features.onboarding.validation import validate_profile


class ProfileRepository:
    """Reads and writes the single local FitTrack profile."""

    def __init__(self, database):
        self.database = database

    def get_profile(self):
        """Return the profile and its latest optional measurements."""
        with self.database.connect() as connection:
            row = connection.execute(
                """
                SELECT u.id, u.display_name, p.experience_level,
                       p.preferred_training_mode,
                       m.height_cm, m.weight_kg, m.measured_at
                FROM users AS u
                JOIN user_profiles AS p ON p.user_id = u.id
                LEFT JOIN body_measurements AS m
                  ON m.id = (
                    SELECT id FROM body_measurements
                    WHERE user_id = u.id
                    ORDER BY measured_at DESC, rowid DESC LIMIT 1
                  )
                ORDER BY u.created_at LIMIT 1
                """
            ).fetchone()
        return dict(row) if row else None

    def save_profile(self, values):
        """Validate and persist profile details and changed measurements."""
        profile = validate_profile(values)
        now = datetime.now(timezone.utc).isoformat()

        with self.database.connect() as connection:
            user = connection.execute(
                "SELECT id FROM users ORDER BY created_at LIMIT 1"
            ).fetchone()
            if user:
                user_id = user["id"]
                connection.execute(
                    "UPDATE users SET display_name = ?, updated_at = ? WHERE id = ?",
                    (profile["display_name"], now, user_id),
                )
                connection.execute(
                    """
                    UPDATE user_profiles
                    SET experience_level = ?, preferred_training_mode = ?,
                        updated_at = ?
                    WHERE user_id = ?
                    """,
                    (profile["experience_level"],
                     profile["preferred_training_mode"], now, user_id),
                )
            else:
                user_id = str(uuid4())
                connection.execute(
                    "INSERT INTO users(id, display_name, created_at, updated_at) "
                    "VALUES (?, ?, ?, ?)",
                    (user_id, profile["display_name"], now, now),
                )
                connection.execute(
                    """
                    INSERT INTO user_profiles(
                        user_id, experience_level, preferred_training_mode,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (user_id, profile["experience_level"],
                     profile["preferred_training_mode"], now, now),
                )
                connection.execute(
                    """
                    INSERT INTO user_settings(
                        user_id, created_at, updated_at
                    ) VALUES (?, ?, ?)
                    """,
                    (user_id, now, now),
                )

            latest = connection.execute(
                """
                SELECT height_cm, weight_kg FROM body_measurements
                WHERE user_id = ?
                ORDER BY measured_at DESC, rowid DESC LIMIT 1
                """,
                (user_id,),
            ).fetchone()
            new_height = profile["height_cm"]
            new_weight = profile["weight_kg"]
            if latest:
                if new_height is None:
                    new_height = latest["height_cm"]
                if new_weight is None:
                    new_weight = latest["weight_kg"]
            changed = (
                (new_height is not None and
                 (latest is None or latest["height_cm"] != new_height))
                or
                (new_weight is not None and
                 (latest is None or latest["weight_kg"] != new_weight))
            )
            if changed:
                connection.execute(
                    """
                    INSERT INTO body_measurements(
                        id, user_id, measured_at, height_cm, weight_kg,
                        note, created_at
                    ) VALUES (?, ?, ?, ?, ?, NULL, ?)
                    """,
                    (str(uuid4()), user_id, now, new_height, new_weight, now),
                )

        return self.get_profile()
