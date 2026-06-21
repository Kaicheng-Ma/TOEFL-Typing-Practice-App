"""Timed challenge content bank.

The timed challenge mode needs shorter, repeatable content units so learners can
focus on speed, consistency, and partial completion under a time limit.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from uuid import uuid4

from ..models import TimedChallengePrompt


@dataclass(frozen=True, slots=True)
class ChallengeBankEntry:
    """A reusable challenge item pool."""

    challenge_type: str
    title: str
    units: tuple[str, ...]


CONTENT_SPRINT_UNITS: tuple[str, ...] = (
    "Students should balance study time and rest time.",
    "A clear outline helps organize complex ideas quickly.",
    "The professor explained the main theory in simple terms.",
    "Good writing often depends on careful revision.",
    "Time management can reduce stress during exams.",
    "Academic discussion encourages deeper thinking.",
)

ITEM_SPRINT_UNITS: tuple[str, ...] = (
    "analyze",
    "beneficial",
    "clarify",
    "consistent",
    "evidence",
    "flexible",
    "important",
    "responsibility",
    "significant",
    "technology",
)

CHALLENGE_BANK: tuple[ChallengeBankEntry, ...] = (
    ChallengeBankEntry(
        challenge_type="content_sprint",
        title="Content Sprint",
        units=CONTENT_SPRINT_UNITS,
    ),
    ChallengeBankEntry(
        challenge_type="item_sprint",
        title="Item Sprint",
        units=ITEM_SPRINT_UNITS,
    ),
)


class TimedChallengePromptGenerator:
    """Create a challenge prompt for the timed practice mode."""

    def __init__(self, seed: int | None = None) -> None:
        self._rng = Random(seed)

    def generate(self, challenge_type: str = "content_sprint", target_count: int = 6) -> TimedChallengePrompt:
        """Generate a timed challenge prompt with a specific item count."""

        bank = next((entry for entry in CHALLENGE_BANK if entry.challenge_type == challenge_type), CHALLENGE_BANK[0])
        if challenge_type == "item_sprint":
            units = self._rng.sample(bank.units, k=min(target_count, len(bank.units)))
            prompt_text = "Type these items one by one:\n" + "\n".join(f"{index + 1}. {unit}" for index, unit in enumerate(units))
        else:
            units = self._rng.sample(bank.units, k=min(target_count, len(bank.units)))
            prompt_text = " ".join(units)
        return TimedChallengePrompt(
            prompt_id=str(uuid4()),
            challenge_type=bank.challenge_type,
            title=bank.title,
            text=prompt_text,
            target_count=len(units),
        )
