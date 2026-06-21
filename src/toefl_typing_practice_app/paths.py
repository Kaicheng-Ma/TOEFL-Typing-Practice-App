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


def get_accounts_root(data_dir: Path | None = None) -> Path:
    """Return the root directory that stores all account-specific data."""

    root_dir = data_dir or get_data_dir()
    accounts_root = root_dir / "accounts"
    accounts_root.mkdir(parents=True, exist_ok=True)
    return accounts_root


def get_account_dir(account_slug: str, data_dir: Path | None = None) -> Path:
    """Return the storage directory for one account."""

    account_dir = get_accounts_root(data_dir) / account_slug
    account_dir.mkdir(parents=True, exist_ok=True)
    return account_dir
