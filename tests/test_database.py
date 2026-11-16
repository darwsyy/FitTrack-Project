"""Tests for SQLite schema, profile persistence, export, and deletion."""
import json
import sqlite3

import pytest

from app.database.connection import Database
from app.database.repositories.profile_repository import ProfileRepository
from app.features.onboarding.validation import ProfileValidationError
from app.services.data_manager import DataManager


@pytest.fixture
def database(tmp_path):
    return Database(tmp_path / "fittrack-test.sqlite3")


def test_database_applies_versioned_schema(database):
    with database.connect() as connection:
        version = connection.execute(
            "SELECT MAX(version) FROM schema_migrations"
        ).fetchone()[0]
        tables = {
            row["name"] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
    assert version == 1
    assert {"users", "user_profiles", "body_measurements",
            "user_settings"}.issubset(tables)


def test_database_migration_is_idempotent(database):
    Database(database.path)
    Database(database.path)
    with database.connect() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM schema_migrations"
        ).fetchone()[0]
    assert count == 1


def test_profile_can_be_created_and_loaded(database):
    repository = ProfileRepository(database)
    profile = repository.save_profile({
        "display_name": "Example User",
        "experience_level": "beginner",
        "preferred_training_mode": "home",
    })
    assert profile["display_name"] == "Example User"
    assert profile["experience_level"] == "beginner"
    assert profile["preferred_training_mode"] == "home"
    assert profile["height_cm"] is None
    assert profile["weight_kg"] is None


def test_profile_update_and_measurement_history(database):
    repository = ProfileRepository(database)
    repository.save_profile({"display_name": "Example User"})
    repository.save_profile({
        "display_name": "Updated User",
        "height_cm": "166",
        "weight_kg": "54",
    })
    repository.save_profile({
        "display_name": "Updated User",
        "height_cm": "166",
        "weight_kg": "54",
    })
    profile = repository.get_profile()
    assert profile["display_name"] == "Updated User"
    assert profile["height_cm"] == 166
    assert profile["weight_kg"] == 54
    with database.connect() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM body_measurements"
        ).fetchone()[0]
    assert count == 1


def test_updating_one_measurement_preserves_the_other(database):
    repository = ProfileRepository(database)
    repository.save_profile({
        "display_name": "Example User",
        "height_cm": 166,
        "weight_kg": 54,
    })
    repository.save_profile({
        "display_name": "Example User",
        "height_cm": 167,
    })
    profile = repository.get_profile()
    assert profile["height_cm"] == 167
    assert profile["weight_kg"] == 54


def test_invalid_profile_input_is_rejected(database):
    repository = ProfileRepository(database)
    with pytest.raises(ProfileValidationError):
        repository.save_profile({"display_name": " "})
    with pytest.raises(ProfileValidationError):
        repository.save_profile({
            "display_name": "User", "height_cm": "-5"
        })
    with pytest.raises(ProfileValidationError):
        repository.save_profile({
            "display_name": "User", "experience_level": "expert"
        })


def test_json_export_contains_profile_data(database, tmp_path):
    repository = ProfileRepository(database)
    repository.save_profile({"display_name": "Export Test"})
    destination = DataManager(database).export_json(
        tmp_path / "exports" / "fittrack.json"
    )
    payload = json.loads(destination.read_text(encoding="utf-8"))
    assert payload["app"] == "FitTrack"
    assert payload["schema_version"] == 1
    assert payload["tables"]["users"][0]["display_name"] == "Export Test"


def test_delete_all_data_preserves_schema(database):
    repository = ProfileRepository(database)
    repository.save_profile({"display_name": "Delete Test"})
    DataManager(database).delete_all_data()
    assert repository.get_profile() is None
    with database.connect() as connection:
        version = connection.execute(
            "SELECT MAX(version) FROM schema_migrations"
        ).fetchone()[0]
    assert version == 1


def test_database_rejects_orphan_measurements(database):
    with pytest.raises(sqlite3.IntegrityError):
        with database.connect() as connection:
            connection.execute(
                """
                INSERT INTO body_measurements(
                    id, user_id, measured_at, height_cm, weight_kg, created_at
                ) VALUES ('orphan', 'missing-user', 'now', 160, NULL, 'now')
                """
            )


def test_profile_persists_after_database_reopen(tmp_path):
    db_path = tmp_path / "persistent.sqlite3"
    first_repository = ProfileRepository(Database(db_path))
    first_repository.save_profile({"display_name": "Persistent User"})

    reopened_repository = ProfileRepository(Database(db_path))
    assert reopened_repository.get_profile()["display_name"] == "Persistent User"
