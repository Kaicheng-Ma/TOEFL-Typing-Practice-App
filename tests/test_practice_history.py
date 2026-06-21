from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from toefl_typing_practice_app.models import PracticeMode, PracticeSessionRecord
from toefl_typing_practice_app.services.practice_history import PracticeHistoryStore


class PracticeHistoryTests(unittest.TestCase):
    def test_load_sessions_skips_invalid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = PracticeHistoryStore(Path(tmpdir))
            store.file_path.write_text("{not valid json}", encoding="utf-8")
            self.assertEqual(store.load_sessions(), [])

    def test_append_and_reload_session(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = PracticeHistoryStore(Path(tmpdir))
            record = PracticeSessionRecord(
                mode=PracticeMode.ESSAY_TYPING,
                created_at="2026-06-21T00:00:00Z",
                title="Email Practice",
                topic="email",
                accuracy=92.5,
                elapsed_seconds=45.0,
                completed_items=14,
                score=101,
                typo_count=2,
                note="Keep going",
                target_text="Hello world",
                typed_text="Hello world",
            )
            store.append_session(record)
            sessions = store.load_sessions()
            self.assertEqual(len(sessions), 1)
            self.assertEqual(sessions[0].title, "Email Practice")
            self.assertTrue(store.file_path.exists())

    def test_load_sessions_skips_partial_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = PracticeHistoryStore(Path(tmpdir))
            payload = [
                {
                    "mode": "essay_typing",
                    "title": "A",
                    "topic": "email",
                    "accuracy": 90,
                    "elapsed_seconds": 30,
                    "completed_items": 1,
                    "score": 99,
                },
                {"mode": "bad-mode", "title": "broken"},
            ]
            store.file_path.write_text(json.dumps(payload), encoding="utf-8")
            sessions = store.load_sessions()
            self.assertEqual(len(sessions), 1)
            self.assertEqual(sessions[0].mode, PracticeMode.ESSAY_TYPING)


if __name__ == "__main__":
    unittest.main()
