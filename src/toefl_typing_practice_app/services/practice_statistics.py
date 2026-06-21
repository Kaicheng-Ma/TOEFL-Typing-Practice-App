"""Practice statistics and trend analysis.

This module turns raw history records into small summaries that can be shown on
screen without requiring a heavy analytics stack.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..models import PracticeMode, PracticeSessionRecord


@dataclass(slots=True)
class ModeStatistics:
    """Aggregated statistics for one practice mode."""

    mode: PracticeMode
    session_count: int
    average_accuracy: float
    best_accuracy: float
    average_score: float


@dataclass(slots=True)
class PracticeStatistics:
    """Top-level statistics bundle for the dashboard."""

    total_sessions: int
    overall_accuracy: float
    overall_score: float
    best_session_score: int
    mode_stats: list[ModeStatistics]
    recent_trend: list[float]
    strongest_mode: str
    weakest_mode: str


def build_practice_statistics(sessions: list[PracticeSessionRecord]) -> PracticeStatistics:
    """Create a compact summary from a list of history records."""

    if not sessions:
        return PracticeStatistics(
            total_sessions=0,
            overall_accuracy=0.0,
            overall_score=0.0,
            best_session_score=0,
            mode_stats=[],
            recent_trend=[],
            strongest_mode="",
            weakest_mode="",
        )

    total_sessions = len(sessions)
    overall_accuracy = round(sum(session.accuracy for session in sessions) / total_sessions, 2)
    overall_score = round(sum(session.score for session in sessions) / total_sessions, 2)
    best_session_score = max(session.score for session in sessions)
    recent_trend = [round(session.accuracy, 2) for session in sessions[-6:]]

    mode_stats: list[ModeStatistics] = []
    for mode in PracticeMode:
        mode_sessions = [session for session in sessions if session.mode == mode]
        if not mode_sessions:
            continue
        mode_stats.append(
            ModeStatistics(
                mode=mode,
                session_count=len(mode_sessions),
                average_accuracy=round(sum(session.accuracy for session in mode_sessions) / len(mode_sessions), 2),
                best_accuracy=round(max(session.accuracy for session in mode_sessions), 2),
                average_score=round(sum(session.score for session in mode_sessions) / len(mode_sessions), 2),
            )
        )

    strongest_mode = ""
    weakest_mode = ""
    if mode_stats:
        strongest_mode = max(mode_stats, key=lambda item: item.average_accuracy).mode.value
        weakest_mode = min(mode_stats, key=lambda item: item.average_accuracy).mode.value

    return PracticeStatistics(
        total_sessions=total_sessions,
        overall_accuracy=overall_accuracy,
        overall_score=overall_score,
        best_session_score=best_session_score,
        mode_stats=mode_stats,
        recent_trend=recent_trend,
        strongest_mode=strongest_mode,
        weakest_mode=weakest_mode,
    )

