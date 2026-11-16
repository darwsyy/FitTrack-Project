"""Kivy application entry and initial root interface."""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class FitTrackApp(App):
    """Minimal desktop-runnable FitTrack application."""

    title = "FitTrack"

    def build(self) -> BoxLayout:
        """Create the initial root layout."""
        root = BoxLayout(
            orientation="vertical",
            padding=24,
            spacing=12,
        )
        root.add_widget(
            Label(
                text="FitTrack",
                font_size="28sp",
                bold=True,
            )
        )
        root.add_widget(
            Label(
                text="Fondasi aplikasi siap dijalankan.",
                font_size="16sp",
            )
        )
        return root
