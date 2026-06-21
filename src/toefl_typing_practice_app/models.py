"""Shared domain models.

The app grows stage by stage, but the underlying objects should already map to
the same core concepts across writing practice, vocabulary drills, timed
challenge sessions, and review history.
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
class VocabularyPrompt:
    """A single vocabulary spelling question."""

    prompt_id: str
    prompt_type: str
    topic: str
    prompt_text: str
    prefix_hint: str
    answer: str
    meaning: str
    example: str


@dataclass(slots=True)
class TimedChallengePrompt:
    """A challenge prompt used in the timed practice mode."""

    prompt_id: str
    challenge_type: str
    title: str
    text: str
    target_count: int


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
class VocabularySessionSummary:
    """Summary for one vocabulary spelling practice session."""

    accuracy: float = 0.0
    elapsed_seconds: int = 0
    total_questions: int = 0
    correct_answers: int = 0
    wrong_answers: int = 0


@dataclass(slots=True)
class TimedChallengeSummary:
    """Summary for one timed challenge session."""

    challenge_type: str
    time_limit_seconds: int
    elapsed_seconds: float
    total_units: int
    completed_units: int
    accuracy: float
    score: int


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


@dataclass(slots=True)
class PracticeSessionRecord:
    """Persisted session record used for review and personalization."""

    mode: PracticeMode
    created_at: str
    title: str
    topic: str
    accuracy: float
    elapsed_seconds: float
    completed_items: int
    score: int
    challenge_type: str = ""
    prompt_type: str = ""
    typo_count: int = 0
    note: str = ""
    target_text: str = ""
    typed_text: str = ""


@dataclass(slots=True)
class PracticeReviewPlan:
    """Small recommendation bundle derived from recent history."""

    note: str
    essay_topic: str = ""
    vocab_topic: str = ""
    vocab_prompt_type: str = ""
    challenge_type: str = ""


@dataclass(slots=True)
class PracticeAccountProfile:
    """Stored account identity used to separate one learner's data from another."""

    username: str
    slug: str
    password_salt: str = ""
    password_hash: str = ""
    created_at: str = ""
    last_login_at: str = ""
