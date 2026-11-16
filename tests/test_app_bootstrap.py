"""Tests for FitTrack UI shell, navigation, and theme behavior."""
from kivy.config import Config
from app.app import FitTrackApp


def test_build_returns_screen_manager_and_all_pages():
    app = FitTrackApp()
    root = app.build()

    assert root is not None
    assert set(app.NAV_ITEMS).issubset(set(app.manager.screen_names))
    assert {"Profile", "Settings"}.issubset(set(app.manager.screen_names))


def test_navigation_changes_current_screen():
    app = FitTrackApp()
    app.build()

    app.go_to("Cardio")

    assert app.manager.current == "Cardio"


def test_theme_toggle_preserves_screen_manager_and_current_page():
    app = FitTrackApp()
    app.build()
    manager_before = app.manager
    app.go_to("Settings")

    app.toggle_theme()

    assert app.theme_name == "dark"
    assert app.manager is manager_before
    assert app.manager.current == "Settings"
    assert app.root_layout is not None


def test_theme_can_be_toggled_back_without_rebuilding():
    app = FitTrackApp()
    app.build()
    manager_before = app.manager

    app.toggle_theme()
    app.toggle_theme()

    assert app.theme_name == "light"
    assert app.manager is manager_before


def test_reusable_components_can_be_created():
    from app.widgets.components import (
        EmptyState, FTButton, FTCard, FTChartContainer, FTInput, LoadingState,
    )

    app = FitTrackApp()
    palette = app.palette

    assert FTCard(palette) is not None
    assert FTButton("Test", palette) is not None
    assert FTInput(palette, hint_text="Nama") is not None
    assert FTChartContainer("Aktivitas", palette) is not None
    assert EmptyState("Kosong", "Belum ada data", palette) is not None
    assert LoadingState(palette) is not None


def test_desktop_preview_configuration_is_portrait():
    assert Config.get("graphics", "width") == "390"
    assert Config.get("graphics", "height") == "844"
