"""Dynamic content generation for essay typing practice.

The generator uses a small set of themed sentence banks and prompt templates.
This keeps Stage 2 compact while still producing changing practice text.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from uuid import uuid4

from ..models import EssayPrompt


@dataclass(frozen=True, slots=True)
class EssayTheme:
    """A themed pool of sentence fragments."""

    name: str
    title: str
    sentences: tuple[str, ...]


THEMES: tuple[EssayTheme, ...] = (
    EssayTheme(
        name="email",
        title="Email Response Practice",
        sentences=(
            "Thank you for your message about the schedule change.",
            "I appreciate the clarification you provided earlier today.",
            "Please let me know whether the meeting should be moved to Friday.",
            "I will review the updated plan and reply with my comments soon.",
            "This adjustment should help everyone prepare more effectively.",
        ),
    ),
    EssayTheme(
        name="academic_discussion",
        title="Academic Discussion Practice",
        sentences=(
            "Many students believe that discussion improves their understanding of a topic.",
            "Others argue that independent reading creates deeper concentration and better recall.",
            "A balanced approach can support both critical thinking and long-term retention.",
            "In academic settings, clear evidence is often more persuasive than a strong opinion.",
            "The final conclusion should connect the main idea to the supporting examples.",
        ),
    ),
    EssayTheme(
        name="campus_life",
        title="Campus Life Practice",
        sentences=(
            "University life often requires students to manage time carefully.",
            "A busy schedule can make it difficult to balance coursework and personal responsibilities.",
            "Reliable planning helps students reduce stress during the semester.",
            "Access to campus resources can improve both academic and social experiences.",
            "Students benefit when they use their time with purpose and consistency.",
        ),
    ),
)


class EssayPromptGenerator:
    """Create varied essay typing prompts from a small themed sentence bank."""

    def __init__(self, seed: int | None = None) -> None:
        self._rng = Random(seed)

    def generate(self, preferred_topic: str = "") -> EssayPrompt:
        """Generate a new prompt with a changing theme and sentence mix."""

        theme_pool = [theme for theme in THEMES if not preferred_topic or theme.name == preferred_topic]
        if not theme_pool:
            theme_pool = list(THEMES)
        theme = self._rng.choice(theme_pool)
        sentence_count = self._rng.randint(3, 5)
        sampled_sentences = self._rng.sample(theme.sentences, k=sentence_count)
        prompt_text = " ".join(sampled_sentences)
        return EssayPrompt(
            prompt_id=str(uuid4()),
            title=theme.title,
            topic=theme.name,
            text=prompt_text,
        )
