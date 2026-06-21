"""Typing analysis helpers.

Stage 2 only needs a compact comparison routine. Later stages can expand this
module into a richer scoring and mistake-analysis service.
"""

from __future__ import annotations

from ..models import TextComparisonResult


def normalize_text(text: str) -> str:
    """Collapse line breaks and repeated whitespace for comparison."""

    return " ".join(text.split())


def compare_texts(target_text: str, typed_text: str, elapsed_seconds: float) -> TextComparisonResult:
    """Compare user input against the target and compute a simple score."""

    normalized_target = normalize_text(target_text)
    normalized_typed = normalize_text(typed_text)
    elapsed_seconds = max(elapsed_seconds, 0.0)
    total_characters = max(len(normalized_target), 1)

    correct_characters = sum(
        1 for expected, actual in zip(normalized_target, normalized_typed) if expected == actual
    )
    typo_count = max(len(normalized_target), len(normalized_typed)) - correct_characters
    accuracy = round((correct_characters / total_characters) * 100, 2)

    minutes = max(elapsed_seconds / 60.0, 1 / 60.0)
    words = len(normalized_typed.split()) if normalized_typed else 0
    words_per_minute = round(words / minutes, 2)

    return TextComparisonResult(
        target_text=target_text,
        typed_text=typed_text,
        correct_characters=correct_characters,
        total_characters=total_characters,
        typo_count=typo_count,
        accuracy=accuracy,
        elapsed_seconds=round(elapsed_seconds, 2),
        words_per_minute=words_per_minute,
    )
