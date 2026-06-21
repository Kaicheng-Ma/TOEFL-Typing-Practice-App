"""Project path helpers.

All data-related paths are centralized here so later stages can store
generated content, history, and caches in predictable locations.
"""

from __future__ import annotations

from pathlib import Path


def get_project_root() -> Path:
    """Return the repository root based on the package location."""

    return Path(__file__).resolve().parents[2]


def get_data_dir() -> Path:
    """Return the local data directory and create it on demand."""

    data_dir = get_project_root() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

