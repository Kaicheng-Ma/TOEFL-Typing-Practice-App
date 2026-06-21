"""Local practice history storage.

This module persists session-level records in an account-specific JSON file so
each learner keeps separate history and review suggestions without needing a
database yet.
"""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from ..models import PracticeMode, PracticeReviewPlan, PracticeSessionRecord


class PracticeHistoryStore:
    """Persist and retrieve practice session history locally."""

    def __init__(self, data_dir: Path, account_slug: str = "shared") -> None:
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.account_slug = account_slug
        self.account_dir = self.data_dir / "accounts" / self.account_slug
        self.account_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.account_dir / "practice_history.json"

    def load_sessions(self) -> list[PracticeSessionRecord]:
        """Return all stored sessions, newest last."""

        if not self.file_path.exists():
            return []

        try:
            payload = json.loads(self.file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(payload, list):
            return []

        sessions: list[PracticeSessionRecord] = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            try:
                sessions.append(self._session_from_payload(item))
            except (TypeError, ValueError, KeyError):
                continue
        return sessions

    def append_session(self, record: PracticeSessionRecord) -> None:
        """Add one new session record to the store."""

        sessions = self.load_sessions()
        sessions.append(record)
        payload = json.dumps([self._serialize_session(session) for session in sessions], ensure_ascii=False, indent=2)
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
            raise RuntimeError("Unable to save practice history locally.") from exc

    def recent_sessions(self, limit: int = 12) -> list[PracticeSessionRecord]:
        """Return the most recent sessions."""

        if limit <= 0:
            return []
        sessions = self.load_sessions()
        return sessions[-limit:]

    def build_review_plan(self) -> PracticeReviewPlan:
        """Derive a short review plan from recent sessions."""

        sessions = self.recent_sessions(12)
        if not sessions:
            return PracticeReviewPlan(note="No practice history yet. Start a session to generate personalized review.")

        essay_sessions = [session for session in sessions if session.mode == PracticeMode.ESSAY_TYPING]
        vocab_sessions = [session for session in sessions if session.mode == PracticeMode.VOCABULARY_SPELLING]
        timed_sessions = [session for session in sessions if session.mode == PracticeMode.TIMED_CHALLENGE]

        essay_topic = self._lowest_average_topic(essay_sessions)
        vocab_topic = self._lowest_average_topic(vocab_sessions)
        vocab_prompt_type = self._most_common_field(vocab_sessions, "prompt_type")
        challenge_type = self._most_common_field(timed_sessions, "challenge_type")

        note = self._build_note(essay_sessions, vocab_sessions, timed_sessions)
        return PracticeReviewPlan(
            note=note,
            essay_topic=essay_topic,
            vocab_topic=vocab_topic,
            vocab_prompt_type=vocab_prompt_type,
            challenge_type=challenge_type,
        )

    def _session_from_payload(self, item: dict[str, Any]) -> PracticeSessionRecord:
        """Coerce a JSON payload into a session record with safe fallbacks."""

        mode_value = str(item.get("mode", ""))
        mode = PracticeMode(mode_value)

        return PracticeSessionRecord(
            mode=mode,
            created_at=str(item.get("created_at", "")),
            title=str(item.get("title", "")),
            topic=str(item.get("topic", "")),
            accuracy=float(item.get("accuracy", 0.0)),
            elapsed_seconds=float(item.get("elapsed_seconds", 0.0)),
            completed_items=int(item.get("completed_items", 0)),
            score=int(item.get("score", 0)),
            challenge_type=str(item.get("challenge_type", "")),
            prompt_type=str(item.get("prompt_type", "")),
            typo_count=int(item.get("typo_count", 0)),
            note=str(item.get("note", "")),
            target_text=str(item.get("target_text", "")),
            typed_text=str(item.get("typed_text", "")),
        )

    def _serialize_session(self, record: PracticeSessionRecord) -> dict[str, Any]:
        payload = asdict(record)
        payload["mode"] = record.mode.value
        return payload

    @staticmethod
    def _lowest_average_topic(sessions: list[PracticeSessionRecord]) -> str:
        if not sessions:
            return ""

        topic_scores: dict[str, list[float]] = {}
        for session in sessions:
            topic_scores.setdefault(session.topic, []).append(session.accuracy)

        scored_topics = [
            (topic, sum(scores) / len(scores))
            for topic, scores in topic_scores.items()
            if topic
        ]
        if not scored_topics:
            return ""
        return min(scored_topics, key=lambda item: item[1])[0]

    @staticmethod
    def _most_common_field(sessions: list[PracticeSessionRecord], field_name: str) -> str:
        if not sessions:
            return ""

        counts: dict[str, int] = {}
        for session in sessions:
            value = getattr(session, field_name, "")
            if value:
                counts[value] = counts.get(value, 0) + 1
        if not counts:
            return ""
        return max(counts.items(), key=lambda item: item[1])[0]

    @staticmethod
    def _build_note(
        essay_sessions: list[PracticeSessionRecord],
        vocab_sessions: list[PracticeSessionRecord],
        timed_sessions: list[PracticeSessionRecord],
    ) -> str:
        if essay_sessions and essay_sessions[-1].accuracy < 90:
            return "Essay mode review: focus on punctuation, capitalization, and smoother long-sentence typing."
        if vocab_sessions and vocab_sessions[-1].accuracy < 85:
            return "Vocabulary review: focus on recent missed words and spelling recall."
        if timed_sessions and timed_sessions[-1].accuracy < 90:
            return "Timed challenge review: keep speed steady while protecting accuracy."
        return "Keep rotating between modes to strengthen recall and typing stability."
