"""Account registry and per-user data context.

The app now treats each learner as a separate account so practice history,
review scheduling, and statistics stay isolated instead of sharing one global
data file.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
import re
import secrets
from pathlib import Path
from typing import Any

from ..models import PracticeAccountProfile
from ..paths import get_account_dir, get_data_dir
from .practice_history import PracticeHistoryStore
from .vocabulary_review import VocabularyReviewStore


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify_username(username: str) -> str:
    """Turn a user-visible name into a stable filesystem-safe slug."""

    normalized = username.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized)
    slug = slug.strip("-")
    return slug or "account"


def _hash_password(password: str, salt_hex: str) -> str:
    salt = bytes.fromhex(salt_hex)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return digest.hex()


@dataclass(slots=True)
class AccountSessionContext:
    """Convenience bundle for the active account's storage services."""

    profile: PracticeAccountProfile
    account_dir: Path
    history_store: PracticeHistoryStore
    review_store: VocabularyReviewStore


class AccountRegistry:
    """Store, authenticate, and load local practice accounts."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or get_data_dir()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.data_dir / "account_registry.json"

    def list_accounts(self) -> list[PracticeAccountProfile]:
        """Return every stored account profile, newest first."""

        if not self.file_path.exists():
            return []

        try:
            payload = json.loads(self.file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(payload, list):
            return []

        profiles: list[PracticeAccountProfile] = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            try:
                profiles.append(self._profile_from_payload(item))
            except (TypeError, ValueError, KeyError):
                continue
        return sorted(profiles, key=lambda profile: profile.last_login_at or profile.created_at, reverse=True)

    def find_account(self, username: str) -> PracticeAccountProfile | None:
        """Look up an account by user-visible name."""

        normalized = username.strip().lower()
        if not normalized:
            return None
        for profile in self.list_accounts():
            if profile.username.strip().lower() == normalized:
                return profile
        return None

    def create_account(self, username: str, password: str = "") -> PracticeAccountProfile:
        """Create a new account profile and persist it immediately."""

        cleaned_username = username.strip()
        if not cleaned_username:
            raise ValueError("Username cannot be empty.")
        if self.find_account(cleaned_username) is not None:
            raise ValueError("That account name already exists.")

        salt_hex = secrets.token_bytes(16).hex() if password else ""
        password_hash = _hash_password(password, salt_hex) if password else ""
        profile = PracticeAccountProfile(
            username=cleaned_username,
            slug=slugify_username(cleaned_username),
            password_salt=salt_hex,
            password_hash=password_hash,
            created_at=_now_iso(),
            last_login_at=_now_iso(),
        )
        self._save_profiles(self.list_accounts() + [profile])
        get_account_dir(profile.slug, self.data_dir)
        return profile

    def authenticate(self, username: str, password: str = "") -> PracticeAccountProfile:
        """Validate credentials and return the matching profile."""

        profile = self.find_account(username)
        if profile is None:
            raise ValueError("That account does not exist yet.")
        if profile.password_hash:
            if not password:
                raise ValueError("This account requires a password.")
            if _hash_password(password, profile.password_salt) != profile.password_hash:
                raise ValueError("The password is incorrect.")
        self.touch_last_login(profile.username)
        return self.find_account(profile.username) or profile

    def touch_last_login(self, username: str) -> None:
        """Update the last login timestamp for one account."""

        accounts = self.list_accounts()
        updated = False
        for index, profile in enumerate(accounts):
            if profile.username.strip().lower() == username.strip().lower():
                accounts[index] = PracticeAccountProfile(
                    username=profile.username,
                    slug=profile.slug,
                    password_salt=profile.password_salt,
                    password_hash=profile.password_hash,
                    created_at=profile.created_at,
                    last_login_at=_now_iso(),
                )
                updated = True
                break
        if updated:
            self._save_profiles(accounts)

    def build_context(self, profile: PracticeAccountProfile) -> AccountSessionContext:
        """Construct the active account's storage bundle."""

        account_dir = get_account_dir(profile.slug, self.data_dir)
        history_store = PracticeHistoryStore(self.data_dir, account_slug=profile.slug)
        review_store = VocabularyReviewStore(account_dir)
        return AccountSessionContext(
            profile=profile,
            account_dir=account_dir,
            history_store=history_store,
            review_store=review_store,
        )

    def _profile_from_payload(self, item: dict[str, Any]) -> PracticeAccountProfile:
        return PracticeAccountProfile(
            username=str(item.get("username", "")),
            slug=str(item.get("slug", "")) or slugify_username(str(item.get("username", ""))),
            password_salt=str(item.get("password_salt", "")),
            password_hash=str(item.get("password_hash", "")),
            created_at=str(item.get("created_at", "")),
            last_login_at=str(item.get("last_login_at", "")),
        )

    def _save_profiles(self, profiles: list[PracticeAccountProfile]) -> None:
        payload = json.dumps([asdict(profile) for profile in profiles], ensure_ascii=False, indent=2)
        temp_path = self.file_path.with_suffix(".tmp")
        try:
            temp_path.write_text(payload, encoding="utf-8")
            temp_path.replace(self.file_path)
        except OSError as exc:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    pass
            raise RuntimeError("Unable to save account registry locally.") from exc
