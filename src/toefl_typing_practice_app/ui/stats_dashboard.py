"""Practice statistics dashboard.

The dashboard turns the stored session history into a concise snapshot of
progress, trend, and per-mode performance.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..paths import get_data_dir
from ..services.practice_history import PracticeHistoryStore
from ..services.practice_statistics import build_practice_statistics


class StatsDashboardFrame(ttk.Frame):
    """Display overall performance and recent trends."""

    def __init__(self, master: tk.Widget) -> None:
        super().__init__(master, padding=16)
        self.history = PracticeHistoryStore(get_data_dir())
        self._build_layout()
        self.refresh()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        ttk.Label(self, text="Stats Dashboard", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w")
        self.summary_label = ttk.Label(self, text="", wraplength=860, justify="left")
        self.summary_label.grid(row=1, column=0, sticky="w", pady=(8, 12))

        self.metrics_box = ttk.Frame(self)
        self.metrics_box.grid(row=2, column=0, sticky="ew")
        self.metrics_box.columnconfigure(0, weight=1)

        self.trend_label = ttk.Label(self, text="", wraplength=860, justify="left", foreground="#2f4f4f")
        self.trend_label.grid(row=3, column=0, sticky="nw", pady=(12, 10))

        self.mode_box = ttk.Frame(self)
        self.mode_box.grid(row=4, column=0, sticky="ew")
        self.mode_box.columnconfigure(0, weight=1)

        self.refresh_button = ttk.Button(self, text="Refresh Stats", command=self.refresh)
        self.refresh_button.grid(row=5, column=0, sticky="e", pady=(12, 0))

    def refresh(self) -> None:
        """Reload history and rebuild all dashboard sections."""

        sessions = self.history.recent_sessions(100)
        stats = build_practice_statistics(sessions)
        self.summary_label.configure(
            text=(
                f"Total sessions: {stats.total_sessions}    "
                f"Overall accuracy: {stats.overall_accuracy:.2f}%    "
                f"Average score: {stats.overall_score:.2f}    "
                f"Best session score: {stats.best_session_score}"
            )
        )
        self.trend_label.configure(
            text=self._format_trend(stats.recent_trend, stats.strongest_mode, stats.weakest_mode)
        )
        self._render_mode_stats(stats.mode_stats)

    def _format_trend(self, trend: list[float], strongest_mode: str, weakest_mode: str) -> str:
        if not trend:
            return "No trend data yet. Complete a few sessions to see your progress line."

        trend_text = ", ".join(f"{value:.0f}%" for value in trend)
        pieces = [f"Recent accuracy trend: {trend_text}."]
        if strongest_mode:
            pieces.append(f"Strongest mode: {strongest_mode}.")
        if weakest_mode:
            pieces.append(f"Weakest mode: {weakest_mode}.")
        return " ".join(pieces)

    def _render_mode_stats(self, mode_stats) -> None:
        # Rebuild the mode summary rows each refresh so the dashboard always
        # reflects the latest history without stale widgets hanging around.
        for child in self.metrics_box.winfo_children():
            child.destroy()

        if not mode_stats:
            ttk.Label(self.metrics_box, text="No mode statistics yet.").pack(anchor="w")
            return

        for stat in mode_stats:
            row = ttk.Frame(self.metrics_box)
            row.pack(fill="x", pady=4)
            label = ttk.Label(
                row,
                text=f"{stat.mode.value} | sessions: {stat.session_count} | avg accuracy: {stat.average_accuracy:.2f}% | best: {stat.best_accuracy:.2f}% | avg score: {stat.average_score:.2f}",
                wraplength=860,
                justify="left",
            )
            label.pack(anchor="w")
