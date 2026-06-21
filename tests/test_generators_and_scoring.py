from __future__ import annotations

import unittest
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from toefl_typing_practice_app.content.essay_generator import EssayPromptGenerator
from toefl_typing_practice_app.content.timed_challenge_bank import TimedChallengePromptGenerator
from toefl_typing_practice_app.content.vocabulary_bank import VocabularyPromptGenerator
from toefl_typing_practice_app.services.timed_challenge_scoring import score_timed_challenge
from toefl_typing_practice_app.services.typing_analysis import compare_texts
from toefl_typing_practice_app.services.vocabulary_scoring import score_vocab_response


class GeneratorAndScoringTests(unittest.TestCase):
    def test_essay_generator_honors_preferred_topic(self) -> None:
        prompt = EssayPromptGenerator(seed=1).generate(preferred_topic="email")
        self.assertEqual(prompt.topic, "email")
        self.assertTrue(prompt.text)

    def test_vocabulary_generator_honors_preferences(self) -> None:
        prompt = VocabularyPromptGenerator(seed=2).generate(
            preferred_topic="academic_discussion",
            preferred_prompt_type="meaning_to_word",
        )
        self.assertEqual(prompt.topic, "academic_discussion")
        self.assertEqual(prompt.prompt_type, "meaning_to_word")
        self.assertTrue(prompt.prompt_text)

    def test_timed_challenge_generator_returns_consistent_prompt(self) -> None:
        prompt = TimedChallengePromptGenerator(seed=3).generate("item_sprint", 4)
        self.assertEqual(prompt.challenge_type, "item_sprint")
        self.assertEqual(prompt.target_count, 4)
        self.assertTrue(prompt.text)

    def test_typing_comparison_reports_perfect_accuracy_for_exact_match(self) -> None:
        result = compare_texts("hello world", "hello world", 12)
        self.assertEqual(result.accuracy, 100.0)
        self.assertEqual(result.typo_count, 0)

    def test_vocabulary_scoring_matches_exact_answer(self) -> None:
        prompt = VocabularyPromptGenerator(seed=4).generate(preferred_prompt_type="meaning_to_word")
        result = score_vocab_response(prompt, prompt.answer)
        self.assertTrue(result.is_correct)

    def test_timed_challenge_scoring_produces_score(self) -> None:
        prompt = TimedChallengePromptGenerator(seed=5).generate("content_sprint", 3)
        result = score_timed_challenge(prompt, "sample typed text", 10.0, 60)
        self.assertGreaterEqual(result.score, 0)
        self.assertGreaterEqual(result.completed_units, 0)


if __name__ == "__main__":
    unittest.main()
