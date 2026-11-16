#Smoke tests for the initial Kivy application

from kivy.uix.boxlayout import BoxLayout

from app.app import FitTrackApp


def test_build_returns_root_layout() -> None:
    app = FitTrackApp()

    root = app.build()

    assert isinstance(root, BoxLayout)
    assert len(root.children) == 2
