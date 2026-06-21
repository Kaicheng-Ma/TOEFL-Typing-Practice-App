"""Local practice history storage.

This module persists session-level records in a single JSON file so the app can
build lightweight personalization and review suggestions without needing a full
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

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.data_dir / "practice_history.json"

    def load_sessions(self) -> list[PracticeSessionRecord]:
        """Return all stored sessions, newest last."""

        if not self.file_path.exists():
            return []

        try:
            payload = json.loads(self.file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

        sessions: list[PracticeSessionRecord] = []
        for item in payload:
            sessions.append(
                PracticeSessionRecord(
                    mode=PracticeMode(item["mode"]),
                    created_at=item.get("created_at", ""),
                    title=item.get("title", ""),
                    topic=item.get("topic", ""),
                    accuracy=float(item.get("accuracy", 0.0)),
                    elapsed_seconds=float(item.get("elapsed_seconds", 0.0)),
                    completed_items=int(item.get("completed_items", 0)),
                    score=int(item.get("score", 0)),
                    challenge_type=item.get("challenge_type", ""),
                    prompt_type=item.get("prompt_type", ""),
                    typo_count=int(item.get("typo_count", 0)),
                    note=item.get("note", ""),
                    target_text=item.get("target_text", ""),
                    typed_text=item.get("typed_text", ""),
                )
            )
        return sessions

    def append_session(self, record: PracticeSessionRecord) -> None:
        """Add one new session record to the store."""

        sessions = self.load_sessions()
        sessions.append(record)
        self.file_path.write_text(
            json.dumps([self._serialize_session(session) for session in sessions], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def recent_sessions(self, limit: int = 12) -> list[PracticeSessionRecord]:
        """Return the most recent sessions."""

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
        return min(topic_scores.items(), key=lambda item: sum(item[1]) / len(item[1]))[0]

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

