from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import sys
import tkinter as tk

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from toefl_typing_practice_app.app import create_app
from toefl_typing_practice_app.content.essay_generator import EssayPromptGenerator
from toefl_typing_practice_app.content.timed_challenge_bank import TimedChallengePromptGenerator
from toefl_typing_practice_app.content.vocabulary_bank import VOCABULARY_ITEMS, VocabularyPromptGenerator
from toefl_typing_practice_app.models import PracticeMode, PracticeSessionRecord, TimedChallengePrompt
from toefl_typing_practice_app.services.practice_history import PracticeHistoryStore
from toefl_typing_practice_app.services.timed_challenge_scoring import score_timed_challenge
from toefl_typing_practice_app.services.typing_analysis import compare_texts


class BoundaryCaseTests(unittest.TestCase):
    def test_load_sessions_skips_non_list_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = PracticeHistoryStore(Path(tmpdir))
            store.file_path.write_text(json.dumps({"mode": "essay_typing"}), encoding="utf-8")
            self.assertEqual(store.load_sessions(), [])

    def test_recent_sessions_returns_empty_for_nonpositive_limit(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = PracticeHistoryStore(Path(tmpdir))
            self.assertEqual(store.recent_sessions(0), [])
            self.assertEqual(store.recent_sessions(-3), [])

    def test_append_session_cleans_temporary_file_when_replace_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = PracticeHistoryStore(Path(tmpdir))
            record = PracticeSessionRecord(
                mode=PracticeMode.ESSAY_TYPING,
                created_at="2026-06-21T00:00:00Z",
                title="Essay",
                topic="email",
                accuracy=90.0,
                elapsed_seconds=30.0,
                completed_items=1,
                score=91,
            )

            with mock.patch.object(Path, "replace", side_effect=OSError("disk error")):
                with self.assertRaises(RuntimeError):
                    store.append_session(record)

            self.assertFalse(store.file_path.with_suffix(".tmp").exists())

    def test_compare_texts_clamps_negative_elapsed_time(self) -> None:
        result = compare_texts("hello world", "hello world", -15.0)
        self.assertEqual(result.elapsed_seconds, 0.0)
        self.assertEqual(result.accuracy, 100.0)
        self.assertGreater(result.words_per_minute, 0.0)

    def test_timed_scoring_clamps_negative_inputs(self) -> None:
        prompt = TimedChallengePrompt(
            prompt_id="demo",
            challenge_type="content_sprint",
            title="Content Sprint",
            text="alpha beta",
            target_count=2,
        )
        result = score_timed_challenge(prompt, "alpha beta", -8.0, -20)
        self.assertEqual(result.elapsed_seconds, 0.0)
        self.assertGreaterEqual(result.score, 0)
        self.assertEqual(result.completed_units, 2)

    def test_timed_generator_clamps_nonpositive_target_count(self) -> None:
        prompt = TimedChallengePromptGenerator(seed=11).generate("item_sprint", 0)
        self.assertGreaterEqual(prompt.target_count, 1)
        self.assertTrue(prompt.text)

    def test_generators_fallback_when_preferences_do_not_match(self) -> None:
        essay_prompt = EssayPromptGenerator(seed=12).generate(preferred_topic="not-a-topic")
        vocab_prompt = VocabularyPromptGenerator(seed=13).generate(
            preferred_topic="not-a-topic",
            preferred_prompt_type="not-a-style",
        )
        essay_topics = {"email", "academic_discussion", "campus_life"}
        vocab_topics = {item.topic for item in VOCABULARY_ITEMS}
        self.assertIn(essay_prompt.topic, essay_topics)
        self.assertIn(vocab_prompt.topic, vocab_topics)
        self.assertTrue(vocab_prompt.prompt_text)

    def test_create_app_raises_clear_error_when_display_is_unavailable(self) -> None:
        with mock.patch("toefl_typing_practice_app.app.tk.Tk", side_effect=tk.TclError("display error")):
            with self.assertRaises(RuntimeError) as context:
                create_app()
        self.assertIn("graphical display", str(context.exception))

    def test_create_app_destroys_root_when_main_window_initialization_fails(self) -> None:
        fake_root = mock.Mock()
        with mock.patch("toefl_typing_practice_app.app.tk.Tk", return_value=fake_root):
            with mock.patch("toefl_typing_practice_app.app.MainWindow", side_effect=Exception("boom")):
                with self.assertRaises(Exception):
                    create_app()
        fake_root.destroy.assert_called_once()


if __name__ == "__main__":
    unittest.main()
