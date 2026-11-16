"""Tests for FitTrack UI shell, navigation, and theme behavior."""
from kivy.config import Config

from app.app import FitTrackApp


def _build_app(tmp_path):
    app = FitTrackApp(database_path=tmp_path / "ui-test.sqlite3")
    app.build()
    return app


def test_build_returns_screen_manager_and_all_pages(tmp_path):
    app = _build_app(tmp_path)
    assert set(app.NAV_ITEMS).issubset(set(app.manager.screen_names))
    assert {"Onboarding", "Profile", "Settings"}.issubset(
        set(app.manager.screen_names)
    )
    assert app.manager.current == "Onboarding"


def test_navigation_changes_current_screen(tmp_path):
    app = _build_app(tmp_path)
    app.go_to("Cardio")
    assert app.manager.current == "Cardio"


def test_theme_toggle_preserves_screen_manager_and_current_page(tmp_path):
    app = _build_app(tmp_path)
    manager_before = app.manager
    app.go_to("Settings")
    app.toggle_theme()
    assert app.theme_name == "dark"
    assert app.manager is manager_before
    assert app.manager.current == "Settings"


def test_theme_can_be_toggled_back_without_rebuilding(tmp_path):
    app = _build_app(tmp_path)
    manager_before = app.manager
    app.toggle_theme()
    app.toggle_theme()
    assert app.theme_name == "light"
    assert app.manager is manager_before


def test_onboarding_save_navigates_to_home_and_profile_persists(tmp_path):
    app = _build_app(tmp_path)
    fields = app.profile_forms["Onboarding"]
    fields["display_name"].text = "Test User"
    app._save_profile_form("Onboarding")
    assert app.manager.current == "Home"
    assert app.profile_repository.get_profile()["display_name"] == "Test User"


def test_profile_screen_loads_saved_values(tmp_path):
    app = _build_app(tmp_path)
    app.profile_repository.save_profile({
        "display_name": "Saved User", "height_cm": 165,
        "weight_kg": 55, "experience_level": "intermediate",
        "preferred_training_mode": "gym",
    })
    app._load_profile_form()
    fields = app.profile_forms["Profile"]
    assert fields["display_name"].text == "Saved User"
    assert fields["height_cm"].text == "165.0"
    assert fields["experience_level"].text == "Menengah"
    assert fields["preferred_training_mode"].text == "Gym"


def test_optional_profile_data_can_be_skipped(tmp_path):
    app = _build_app(tmp_path)
    fields = app.profile_forms["Onboarding"]
    fields["display_name"].text = "No Measurements"
    app._save_profile_form("Onboarding")
    profile = app.profile_repository.get_profile()
    assert profile["height_cm"] is None
    assert profile["weight_kg"] is None


def test_desktop_preview_configuration_is_portrait():
    assert Config.get("graphics", "width") == "390"
    assert Config.get("graphics", "height") == "844"


def test_delete_data_requires_two_confirmations(tmp_path):
    app = _build_app(tmp_path)
    app.profile_repository.save_profile({"display_name": "Delete Me"})

    assert app.request_delete_data() is False
    assert app.profile_repository.get_profile() is not None
    assert app.request_delete_data() is True
    assert app.profile_repository.get_profile() is None
    assert app.manager.current == "Onboarding"


def test_settings_button_opens_theme_settings(tmp_path):
    app = _build_app(tmp_path)
    app.settings_button.dispatch("on_release")
    assert app.manager.current == "Settings"
    assert app.theme_label is not None



def test_workout_screen_builds_catalogue_and_template_controls(tmp_path):
    app = _build_app(tmp_path)
    app.go_to("Workout")
    assert app.manager.current == "Workout"
    assert "Full Body" in app.workout_template_map
    assert "Chest Press" in app.workout_exercise_map


def test_workout_ui_can_record_and_finish_session(tmp_path):
    app = _build_app(tmp_path)
    app.profile_repository.save_profile({"display_name": "Workout UI"})
    app.go_to("Workout")
    app._start_workout(False)
    assert app.active_workout_id is not None
    app.workout_reps_input.text = "8"
    app._add_workout_set()
    assert "Set berhasil" in app.workout_message.text
    app._finish_workout()
    assert app.active_workout_id is None
    assert len(app.workout_history_map) == 1


def test_workout_ui_can_create_custom_routine(tmp_path):
    app = _build_app(tmp_path)
    app.profile_repository.save_profile({"display_name": "Routine UI"})
    app.go_to("Workout")
    app.custom_routine_name.text = "Routine UI Test"
    app._add_custom_routine_exercise()
    app._save_custom_routine()
    assert "Routine UI Test" in app.workout_template_map



def test_workout_ui_restores_active_session_after_rebuild(tmp_path):
    app = _build_app(tmp_path)
    app.profile_repository.save_profile({"display_name": "Resume UI"})
    app.go_to("Workout")
    app.workout_mode_spinner.text = "Home workout"
    app._start_workout(False)
    session_id = app.active_workout_id

    reopened_app = _build_app(tmp_path)
    reopened_app.go_to("Workout")
    assert reopened_app.active_workout_id == session_id
    assert reopened_app.workout_mode_spinner.text == "Home workout"
