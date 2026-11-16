"""Workout catalogue, templates, sessions, and set persistence tests."""
import pytest

from app.database.connection import Database
from app.database.repositories.profile_repository import ProfileRepository
from app.database.repositories.workout_repository import (
    WorkoutRepository, WorkoutValidationError,
)


@pytest.fixture
def setup_workout(tmp_path):
    database = Database(tmp_path / "workout.sqlite3")
    ProfileRepository(database).save_profile({"display_name": "Workout Tester"})
    return database, WorkoutRepository(database)


def test_catalogue_and_builtin_templates_are_seeded_idempotently(setup_workout):
    database, repository = setup_workout
    exercises_before = len(repository.list_exercises())
    templates_before = len(repository.list_templates())
    repository.seed_catalogue()
    assert len(repository.list_exercises()) == exercises_before
    assert len(repository.list_templates()) == templates_before
    assert exercises_before >= 10
    assert {"PPL - Push", "PPL - Pull", "PPL - Legs",
            "Upper Body", "Lower Body", "Full Body"}.issubset(
        {item["name"] for item in repository.list_templates("gym")}
    )
    assert {"Home Full Body", "Home Lower Body"}.issubset(
        {item["name"] for item in repository.list_templates("home")}
    )


def test_home_catalogue_does_not_show_gym_only_exercises(setup_workout):
    _, repository = setup_workout
    names = {item["name"] for item in repository.list_exercises("home")}
    assert "Push-up" in names
    assert "Chest Press" not in names
    assert "Squat" in names


def test_custom_routine_requires_name_and_at_least_one_exercise(setup_workout):
    _, repository = setup_workout
    exercise = repository.list_exercises("home")[0]
    with pytest.raises(WorkoutValidationError):
        repository.create_custom_template("", "home", [exercise["id"]])
    with pytest.raises(WorkoutValidationError):
        repository.create_custom_template("My Routine", "home", [])
    routine_id = repository.create_custom_template(
        "My Routine", "home", [exercise["id"]]
    )
    assert routine_id
    assert any(
        item["name"] == "My Routine" and item["is_custom"]
        for item in repository.list_templates("home")
    )


def test_template_session_records_exercises_sets_and_history(setup_workout):
    _, repository = setup_workout
    template = next(
        item for item in repository.list_templates("home")
        if item["name"] == "Home Full Body"
    )
    session = repository.start_session(
        training_mode="home", template_id=template["id"]
    )
    assert session["status"] == "in_progress"
    assert len(session["exercises"]) == 4

    first_exercise = session["exercises"][0]
    repository.add_set(
        first_exercise["session_exercise_id"],
        reps=12, weight_kg=0,
    )
    completed = repository.finish_session(session["id"], notes="Sesi uji")
    assert completed["status"] == "completed"
    assert completed["notes"] == "Sesi uji"
    assert len(completed["exercises"][0]["sets"]) == 1
    assert completed["exercises"][0]["sets"][0]["reps"] == 12

    history = repository.list_history()
    assert len(history) == 1
    assert history[0]["completed_sets"] == 1
    assert history[0]["exercise_count"] == 4


def test_empty_session_cannot_be_finished(setup_workout):
    _, repository = setup_workout
    session = repository.start_session(training_mode="gym")
    with pytest.raises(WorkoutValidationError):
        repository.finish_session(session["id"])
    assert repository.get_session(session["id"])["status"] == "in_progress"


def test_session_accepts_bodyweight_duration_sets(setup_workout):
    _, repository = setup_workout
    session = repository.start_session(training_mode="home")
    exercise = repository.list_exercises("home")[0]
    exercise_id = repository.add_exercise(session["id"], exercise["id"])
    repository.add_set(exercise_id, duration_seconds=30)
    stored = repository.get_session(session["id"])
    assert stored["exercises"][0]["sets"][0]["duration_seconds"] == 30


def test_invalid_set_values_are_rejected(setup_workout):
    _, repository = setup_workout
    session = repository.start_session(training_mode="gym")
    exercise = repository.list_exercises("gym")[0]
    exercise_id = repository.add_exercise(session["id"], exercise["id"])
    for values in (
        {"reps": 0},
        {"reps": -2},
        {"weight_kg": -1, "reps": 5},
        {"reps": "not-a-number"},
        {},
    ):
        with pytest.raises(WorkoutValidationError):
            repository.add_set(exercise_id, **values)


def test_completed_session_cannot_be_modified(setup_workout):
    _, repository = setup_workout
    session = repository.start_session(training_mode="gym")
    exercise = repository.list_exercises("gym")[0]
    exercise_id = repository.add_exercise(session["id"], exercise["id"])
    repository.add_set(exercise_id, reps=8)
    repository.finish_session(session["id"])
    with pytest.raises(WorkoutValidationError):
        repository.add_set(exercise_id, reps=8)
    with pytest.raises(WorkoutValidationError):
        repository.add_exercise(session["id"], exercise["id"])


def test_workout_records_are_removed_with_user_data(setup_workout):
    database, repository = setup_workout
    session = repository.start_session(training_mode="home")
    exercise = repository.list_exercises("home")[0]
    repository.add_exercise(session["id"], exercise["id"])
    with database.connect() as connection:
        connection.execute("DELETE FROM users")
        remaining = connection.execute(
            "SELECT COUNT(*) FROM workout_sessions"
        ).fetchone()[0]
    assert remaining == 0



def test_only_one_active_session_is_allowed_and_can_be_resumed(setup_workout):
    database, repository = setup_workout
    session = repository.start_session(training_mode="home")
    with pytest.raises(WorkoutValidationError):
        repository.start_session(training_mode="gym")

    reopened = WorkoutRepository(Database(database.path))
    active = reopened.get_active_session()
    assert active["id"] == session["id"]
    assert active["status"] == "in_progress"


def test_custom_templates_are_deleted_with_their_owner(setup_workout):
    database, repository = setup_workout
    exercise = repository.list_exercises("home")[0]
    template_id = repository.create_custom_template(
        "Private Routine", "home", [exercise["id"]]
    )
    assert any(
        item["id"] == template_id for item in repository.list_templates("home")
    )
    with database.connect() as connection:
        connection.execute("DELETE FROM users")
    assert not any(
        item["id"] == template_id for item in repository.list_templates("home")
    )



def test_session_rejects_exercises_from_another_training_mode(setup_workout):
    _, repository = setup_workout
    session = repository.start_session(training_mode="home")
    gym_exercise = next(
        item for item in repository.list_exercises("gym")
        if item["training_mode"] == "gym"
    )
    with pytest.raises(WorkoutValidationError):
        repository.add_exercise(session["id"], gym_exercise["id"])
