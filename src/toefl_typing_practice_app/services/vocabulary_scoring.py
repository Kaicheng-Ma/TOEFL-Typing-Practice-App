"""Vocabulary spelling scoring helpers."""

from __future__ import annotations

from dataclasses import dataclass

from ..models import VocabularyPrompt


@dataclass(slots=True)
class VocabularyScoringResult:
    """Outcome of one vocabulary spelling attempt."""

    prompt: VocabularyPrompt
    typed_answer: str
    is_correct: bool
    normalized_answer: str
    normalized_typed_answer: str


def normalize_answer(text: str) -> str:
    """Normalize user answers for simple spelling comparison."""

    return text.strip().lower()


def score_vocab_response(prompt: VocabularyPrompt, typed_answer: str) -> VocabularyScoringResult:
    """Check one typed answer against the expected spelling."""

    normalized_answer = normalize_answer(prompt.answer)
    normalized_typed_answer = normalize_answer(typed_answer)
    return VocabularyScoringResult(
        prompt=prompt,
        typed_answer=typed_answer,
        is_correct=normalized_answer == normalized_typed_answer,
        normalized_answer=normalized_answer,
        normalized_typed_answer=normalized_typed_answer,
    )
