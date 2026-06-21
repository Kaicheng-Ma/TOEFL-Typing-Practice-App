"""Shared domain models.

These models intentionally stay small in Stage 1 so the rest of the app can
grow around clear, typed contracts for practice modes, prompts, and results.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PracticeMode(str, Enum):
    """Top-level practice modes shown in the UI."""

    ESSAY_TYPING = "essay_typing"
    VOCABULARY_SPELLING = "vocabulary_spelling"
    TIMED_CHALLENGE = "timed_challenge"


@dataclass(slots=True)
class PracticeSessionSummary:
    """Minimal placeholder for a practice result record."""

    mode: PracticeMode
    accuracy: float = 0.0
    elapsed_seconds: int = 0
    completed_items: int = 0

