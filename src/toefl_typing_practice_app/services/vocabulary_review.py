"""Spaced repetition support for vocabulary review.

The review queue keeps missed words coming back on a simple memory curve so
wrong answers reappear sooner and well-known words fade out more gradually.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Any

from ..models import VocabularyPrompt


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_datetime(value: str) -> datetime:
    if not value:
        return _now()
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return _now()
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


@dataclass(slots=True)
class VocabularyReviewItem:
    """One vocabulary word tracked for spaced repetition."""

    word: str
    topic: str
    prompt_type: str
    meaning: str
    example: str
    due_at: str
    interval_minutes: int = 15
    ease_factor: float = 2.2
    repetitions: int = 0
    miss_count: int = 0
    success_count: int = 0
    last_seen_at: str = ""
    last_result: str = ""
    last_prompt_text: str = ""

    def is_due(self, now: datetime | None = None) -> bool:
        """Check whether this item should reappear now."""

        reference_time = now or _now()
        return _parse_datetime(self.due_at) <= reference_time

    def urgency_score(self, now: datetime | None = None) -> float:
        """Return a score that favors overdue and frequently missed items."""

        reference_time = now or _now()
        due_time = _parse_datetime(self.due_at)
        overdue_minutes = max((reference_time - due_time).total_seconds() / 60.0, 0.0)
        pressure = overdue_minutes + (self.miss_count * 12) - (self.success_count * 2)
        if self.repetitions == 0:
            pressure += 8
        return pressure

    def recommended_prompt_type(self) -> str:
        """Use a friendly prompt style for review rounds."""

        if self.prompt_type in {"meaning_to_word", "definition_to_word"}:
            return self.prompt_type
        return "meaning_to_word"


class VocabularyReviewStore:
    """Persist and schedule vocabulary review items inside one account."""

    def __init__(self, account_dir: Path) -> None:
        self.account_dir = account_dir
        self.account_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.account_dir / "vocabulary_review_queue.json"

    def load_items(self) -> list[VocabularyReviewItem]:
        """Load scheduled review items, oldest due first."""

        if not self.file_path.exists():
            return []

        try:
            payload = json.loads(self.file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(payload, list):
            return []

        items: list[VocabularyReviewItem] = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            try:
                items.append(self._item_from_payload(item))
            except (TypeError, ValueError, KeyError):
                continue
        return items

    def save_items(self, items: list[VocabularyReviewItem]) -> None:
        """Write the review queue back to disk atomically."""

        payload = json.dumps([asdict(item) for item in items], ensure_ascii=False, indent=2)
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
            raise RuntimeError("Unable to save vocabulary review queue locally.") from exc

    def record_attempt(self, prompt: VocabularyPrompt, was_correct: bool, elapsed_seconds: float) -> VocabularyReviewItem:
        """Update the review schedule after one vocabulary attempt."""

        items = self.load_items()
        now = _now()
        item = next((entry for entry in items if entry.word == prompt.answer), None)
        if item is None:
            item = VocabularyReviewItem(
                word=prompt.answer,
                topic=prompt.topic,
                prompt_type=prompt.prompt_type,
                meaning=prompt.meaning,
                example=prompt.example,
                due_at=now.isoformat(),
            )
            items.append(item)

        item.topic = prompt.topic
        item.prompt_type = prompt.prompt_type
        item.meaning = prompt.meaning
        item.example = prompt.example
        item.last_seen_at = now.isoformat()
        item.last_result = "correct" if was_correct else "wrong"
        item.last_prompt_text = prompt.prompt_text

        if was_correct:
            item.success_count += 1
            item.repetitions += 1
            item.ease_factor = min(item.ease_factor + 0.08, 2.5)
            item.interval_minutes = self._next_correct_interval(item)
        else:
            item.miss_count += 1
            item.repetitions = 0
            item.ease_factor = max(item.ease_factor - 0.25, 1.3)
            item.interval_minutes = self._next_miss_interval(elapsed_seconds)

        item.due_at = (now + timedelta(minutes=item.interval_minutes)).isoformat()
        self.save_items(items)
        return item

    def next_due_item(self) -> VocabularyReviewItem | None:
        """Return the most urgent review item that is due now."""

        items = self.load_items()
        due_items = [item for item in items if item.is_due()]
        if not due_items:
            return None
        return max(due_items, key=lambda item: item.urgency_score())

    def build_summary(self) -> str:
        """Create a short human-readable summary for the review UI."""

        items = self.load_items()
        if not items:
            return "No vocabulary review items yet. Missed words will come back here automatically."

        due_items = [item for item in items if item.is_due()]
        upcoming = sorted(items, key=lambda item: _parse_datetime(item.due_at))[0]
        if due_items:
            top_item = max(due_items, key=lambda item: item.urgency_score())
            return (
                f"Review queue: {len(due_items)} due now, {len(items)} tracked total. "
                f"Next focus word: {top_item.word}. "
                f"Upcoming fallback word: {upcoming.word}."
            )
        return (
            f"Review queue: {len(items)} tracked words, none due right now. "
            f"Next scheduled word: {upcoming.word}."
        )

    def build_due_list_summary(self, limit: int = 3) -> str:
        """Describe the most urgent items with their exact return times."""

        items = self.load_items()
        if not items:
            return "No review items yet."

        ordered = sorted(items, key=lambda item: item.urgency_score(), reverse=True)
        due_now = [item for item in ordered if item.is_due()]
        focus_items = due_now[:limit] if due_now else ordered[:limit]
        lines = []
        for item in focus_items:
            due_time = _parse_datetime(item.due_at).astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            if item.is_due():
                status = f"due now, next check {due_time}"
            else:
                status = f"returns at {due_time}"
            lines.append(
                f"- {item.word} | {status} | misses {item.miss_count} | successes {item.success_count} | interval {item.interval_minutes} min"
            )
        return "\n".join(lines)

    def next_due_time(self) -> str:
        """Return the next scheduled due time in a readable format."""

        items = self.load_items()
        if not items:
            return ""
        upcoming = min(items, key=lambda item: _parse_datetime(item.due_at))
        return _parse_datetime(upcoming.due_at).astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    def _item_from_payload(self, item: dict[str, Any]) -> VocabularyReviewItem:
        return VocabularyReviewItem(
            word=str(item.get("word", "")),
            topic=str(item.get("topic", "")),
            prompt_type=str(item.get("prompt_type", "")),
            meaning=str(item.get("meaning", "")),
            example=str(item.get("example", "")),
            due_at=str(item.get("due_at", "")),
            interval_minutes=int(item.get("interval_minutes", 15)),
            ease_factor=float(item.get("ease_factor", 2.2)),
            repetitions=int(item.get("repetitions", 0)),
            miss_count=int(item.get("miss_count", 0)),
            success_count=int(item.get("success_count", 0)),
            last_seen_at=str(item.get("last_seen_at", "")),
            last_result=str(item.get("last_result", "")),
            last_prompt_text=str(item.get("last_prompt_text", "")),
        )

    @staticmethod
    def _next_miss_interval(elapsed_seconds: float) -> int:
        """Shorten the next interval when the learner misses a word."""

        if elapsed_seconds < 20:
            return 10
        if elapsed_seconds < 60:
            return 20
        return 30

    @staticmethod
    def _next_correct_interval(item: VocabularyReviewItem) -> int:
        """Gradually stretch the return interval after successful recalls."""

        if item.repetitions <= 1:
            return 30
        if item.repetitions == 2:
            return 24 * 60
        if item.repetitions == 3:
            return 3 * 24 * 60
        scaled = int(round(item.interval_minutes * item.ease_factor))
        return min(max(scaled, 24 * 60), 30 * 24 * 60)
