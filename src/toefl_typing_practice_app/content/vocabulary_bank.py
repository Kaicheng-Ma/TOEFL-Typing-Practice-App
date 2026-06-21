"""Vocabulary content bank for spelling practice.

Stage 3 keeps the first bank intentionally small but structured around the
project's target domains so later stages can scale the set without changing
the calling code.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from uuid import uuid4

from ..models import VocabularyPrompt


@dataclass(frozen=True, slots=True)
class VocabularyItem:
    """A vocabulary entry with multiple prompt styles."""

    word: str
    meaning: str
    example: str
    topic: str
    prompt_types: tuple[str, ...]


VOCABULARY_ITEMS: tuple[VocabularyItem, ...] = (
    VocabularyItem(
        word="influence",
        meaning="the power to affect how someone or something develops, behaves, or thinks",
        example="Teachers can influence how students approach learning.",
        topic="academic_discussion",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="maintain",
        meaning="to keep something in the same state or continue something",
        example="Students should maintain a steady study routine before the exam.",
        topic="campus_life",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="significant",
        meaning="large enough or important enough to have an effect",
        example="The study found a significant improvement after the new method was used.",
        topic="academic_discussion",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="clarify",
        meaning="to make something easier to understand",
        example="The professor asked the student to clarify the main point.",
        topic="email",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="effective",
        meaning="successful in producing the intended result",
        example="A clear outline can be an effective way to organize ideas.",
        topic="academic_discussion",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="perspective",
        meaning="a way of thinking about something",
        example="The discussion offered a new perspective on the issue.",
        topic="academic_discussion",
        prompt_types=("meaning_to_word", "definition_to_word", "root_hint"),
    ),
    VocabularyItem(
        word="responsibility",
        meaning="a duty to take care of something or someone",
        example="Time management is an important responsibility for university students.",
        topic="campus_life",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="contribute",
        meaning="to help cause something to happen",
        example="Regular practice can contribute to stronger writing performance.",
        topic="academic_discussion",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
)


class VocabularyPromptGenerator:
    """Generate vocabulary spelling questions with controlled variation."""

    def __init__(self, seed: int | None = None) -> None:
        self._rng = Random(seed)

    def generate(self, preferred_topic: str = "", preferred_prompt_type: str = "") -> VocabularyPrompt:
        """Return a question that matches one of the supported prompt styles."""

        eligible_items = [
            item
            for item in VOCABULARY_ITEMS
            if (not preferred_topic or item.topic == preferred_topic)
            and (not preferred_prompt_type or preferred_prompt_type in item.prompt_types)
        ]
        if not eligible_items:
            eligible_items = list(VOCABULARY_ITEMS)
        item = self._rng.choice(eligible_items)
        prompt_type_pool = list(item.prompt_types)
        if preferred_prompt_type and preferred_prompt_type in prompt_type_pool:
            prompt_type = preferred_prompt_type
        else:
            prompt_type = self._rng.choice(prompt_type_pool)
        prompt_text = self._build_prompt_text(item, prompt_type)
        return VocabularyPrompt(
            prompt_id=str(uuid4()),
            prompt_type=prompt_type,
            topic=item.topic,
            prompt_text=prompt_text,
            answer=item.word,
            meaning=item.meaning,
            example=item.example,
        )

    def _build_prompt_text(self, item: VocabularyItem, prompt_type: str) -> str:
        if prompt_type == "meaning_to_word":
            return f"Spell the TOEFL vocabulary word for this meaning: {item.meaning}"
        if prompt_type == "definition_to_word":
            return f"Write the word that matches this definition: {item.meaning}"
        if prompt_type == "cloze":
            return f"Complete the sentence: {self._build_cloze(item.example, item.word)}"
        if prompt_type == "root_hint":
            return f"Spell the word using this hint: related to 'view' or 'look' in a broader sense."
        return f"Spell this word: {item.word}"

    @staticmethod
    def _build_cloze(example: str, answer: str) -> str:
        lower_example = example
        return lower_example.replace(answer, "_____", 1)
