from __future__ import annotations

import unittest
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from toefl_typing_practice_app.models import PracticeMode, PracticeSessionRecord
from toefl_typing_practice_app.services.practice_statistics import build_practice_statistics


class StatisticsTests(unittest.TestCase):
    def test_statistics_reflect_mode_strengths(self) -> None:
        sessions = [
            PracticeSessionRecord(
                mode=PracticeMode.ESSAY_TYPING,
                created_at="2026-06-21T00:00:00Z",
                title="Essay",
                topic="email",
                accuracy=80.0,
                elapsed_seconds=60,
                completed_items=10,
                score=84,
            ),
            PracticeSessionRecord(
                mode=PracticeMode.VOCABULARY_SPELLING,
                created_at="2026-06-21T00:10:00Z",
                title="Word",
                topic="academic_discussion",
                accuracy=100.0,
                elapsed_seconds=10,
                completed_items=1,
                score=10,
            ),
        ]
        stats = build_practice_statistics(sessions)
        self.assertEqual(stats.total_sessions, 2)
        self.assertEqual(stats.strongest_mode, "vocabulary_spelling")
        self.assertEqual(stats.weakest_mode, "essay_typing")
        self.assertEqual(stats.recent_trend, [80.0, 100.0])


if __name__ == "__main__":
    unittest.main()
