"""Shared domain models.

The first implementation stage only needs a small set of typed objects, but
they should already reflect the app's core concepts so later stages can build
on them without reshaping the whole project.
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
class EssayPrompt:
    """Generated text for one essay typing practice session."""

    prompt_id: str
    title: str
    topic: str
    text: str


@dataclass(slots=True)
class PracticeSessionSummary:
    """Summary for one completed practice session."""

    mode: PracticeMode
    accuracy: float = 0.0
    elapsed_seconds: int = 0
    completed_items: int = 0
    typed_characters: int = 0
    correct_characters: int = 0
    typo_count: int = 0


@dataclass(slots=True)
class TextComparisonResult:
    """Character-level comparison result for essay typing practice."""

    target_text: str
    typed_text: str
    correct_characters: int
    total_characters: int
    typo_count: int
    accuracy: float
    elapsed_seconds: float
    words_per_minute: float

