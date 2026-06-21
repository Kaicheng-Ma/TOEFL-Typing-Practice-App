from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from toefl_typing_practice_app.content.vocabulary_bank import VocabularyPromptGenerator
from toefl_typing_practice_app.models import PracticeMode, PracticeSessionRecord
from toefl_typing_practice_app.services.account_store import AccountRegistry
from toefl_typing_practice_app.services.practice_history import PracticeHistoryStore
from toefl_typing_practice_app.services.vocabulary_review import VocabularyReviewStore


class AccountAndReviewTests(unittest.TestCase):
    def test_create_account_without_password_and_login(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = AccountRegistry(Path(tmpdir))
            created = registry.create_account("Alice")
            authed = registry.authenticate("Alice")
            self.assertEqual(created.username, "Alice")
            self.assertEqual(authed.username, "Alice")
            self.assertTrue((Path(tmpdir) / "accounts" / created.slug).exists())

    def test_update_password_requires_new_password_for_login(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = AccountRegistry(Path(tmpdir))
            registry.create_account("Alice")
            registry.update_password("Alice", "secret")
            with self.assertRaises(ValueError):
                registry.authenticate("Alice")
            authed = registry.authenticate("Alice", "secret")
            self.assertEqual(authed.username, "Alice")

    def test_account_history_stays_isolated(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = AccountRegistry(Path(tmpdir))
            alice = registry.create_account("Alice")
            bob = registry.create_account("Bob")
            alice_history = PracticeHistoryStore(Path(tmpdir), account_slug=alice.slug)
            bob_history = PracticeHistoryStore(Path(tmpdir), account_slug=bob.slug)

            alice_history.append_session(
                PracticeSessionRecord(
                    mode=PracticeMode.ESSAY_TYPING,
                    created_at="2026-06-21T00:00:00Z",
                    title="Essay",
                    topic="email",
                    accuracy=88.0,
                    elapsed_seconds=60.0,
                    completed_items=1,
                    score=90,
                )
            )

            self.assertEqual(len(alice_history.load_sessions()), 1)
            self.assertEqual(len(bob_history.load_sessions()), 0)

    def test_vocabulary_review_queue_returns_due_items_first(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = AccountRegistry(Path(tmpdir))
            profile = registry.create_account("Reviewer")
            context = registry.build_context(profile)
            review_store = VocabularyReviewStore(context.account_dir)
            prompt = VocabularyPromptGenerator(seed=7).generate(preferred_word="clarify")

            review_store.record_attempt(prompt, was_correct=False, elapsed_seconds=18.0)
            items = review_store.load_items()
            self.assertEqual(len(items), 1)
            items[0].due_at = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
            review_store.save_items(items)

            due_item = review_store.next_due_item()
            self.assertIsNotNone(due_item)
            self.assertEqual(due_item.word, "clarify")
            self.assertIn("due now", review_store.build_summary())
            self.assertIn("clarify", review_store.build_due_list_summary())
            self.assertIn("UTC", review_store.build_due_list_summary())


if __name__ == "__main__":
    unittest.main()
