"""Scoring helpers for timed challenge practice."""

from __future__ import annotations

from dataclasses import dataclass

from ..models import TimedChallengePrompt, TimedChallengeSummary
from .typing_analysis import compare_texts, normalize_text


@dataclass(slots=True)
class TimedChallengeResult:
    """Normalized result for a timed challenge attempt."""

    prompt: TimedChallengePrompt
    typed_text: str
    elapsed_seconds: float
    completed_units: int
    accuracy: float
    score: int


def _split_units(text: str) -> list[str]:
    """Break input into comparable units for timed mode scoring."""

    normalized = normalize_text(text)
    if not normalized:
        return []
    return normalized.split(" ")


def score_timed_challenge(
    prompt: TimedChallengePrompt,
    typed_text: str,
    elapsed_seconds: float,
    time_limit_seconds: int,
) -> TimedChallengeResult:
    """Score a timed challenge session using a simple speed-accuracy balance."""

    comparison = compare_texts(prompt.text, typed_text, elapsed_seconds)
    units = _split_units(typed_text)
    completed_units = len(units)
    time_factor = max(time_limit_seconds - int(elapsed_seconds), 0)
    score = int((completed_units * 12) + comparison.accuracy + time_factor)
    return TimedChallengeResult(
        prompt=prompt,
        typed_text=typed_text,
        elapsed_seconds=round(elapsed_seconds, 2),
        completed_units=completed_units,
        accuracy=comparison.accuracy,
        score=score,
    )

