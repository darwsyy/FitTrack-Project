"""Command-line entry point for FitTrack."""

from app.app import FitTrackApp


def main() -> None:
    """Start the Kivy event loop."""
    FitTrackApp().run()


if __name__ == "__main__":
    main()
