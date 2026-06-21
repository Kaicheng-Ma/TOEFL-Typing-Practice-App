"""Console entry point for the desktop app."""

from __future__ import annotations

from .app import create_app


def main() -> None:
    """Launch the application."""

    app = create_app()
    app.run()


if __name__ == "__main__":
    main()

