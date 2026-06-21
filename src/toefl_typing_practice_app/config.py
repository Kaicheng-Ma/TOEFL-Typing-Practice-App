"""Application configuration objects.

Keeping configuration in dedicated dataclasses makes it easier to change
window settings, data paths, and future feature toggles without scattering
constants across the codebase.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AppConfig:
    """Static settings for the desktop app shell."""

    app_name: str = "TOEFL Typing Practice App"
    window_width: int = 980
    window_height: int = 680
    min_window_width: int = 860
    min_window_height: int = 560

