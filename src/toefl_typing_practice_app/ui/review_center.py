"""Review center UI.

This panel summarizes recent sessions and surfaces the current review plan so
users can quickly see what the app thinks they should work on next.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..models import PracticeReviewPlan
from ..paths import get_data_dir
from ..services.practice_history import PracticeHistoryStore


class ReviewCenterFrame(ttk.Frame):
    """A lightweight dashboard for review and personalization."""

    def __init__(self, master: tk.Widget) -> None:
        super().__init__(master, padding=16)
        self.history = PracticeHistoryStore(get_data_dir())
        self._build_layout()
        self.refresh()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ttk.Label(self, text="Review Center", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w")
        self.plan_label = ttk.Label(
            self,
            text="",
            wraplength=860,
            justify="left",
            foreground="#2f4f4f",
        )
        self.plan_label.grid(row=1, column=0, sticky="w", pady=(8, 12))

        self.sessions_box = ttk.Frame(self)
        self.sessions_box.grid(row=2, column=0, sticky="nsew")
        self.sessions_box.columnconfigure(0, weight=1)

        self.summary_label = ttk.Label(
            self.sessions_box,
            text="Recent sessions will appear here.",
            wraplength=860,
            justify="left",
        )
        self.summary_label.grid(row=0, column=0, sticky="w")

        self.sessions_text = tk.Text(self.sessions_box, height=14, wrap="word", padx=8, pady=8)
        self.sessions_text.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.sessions_text.configure(state="disabled")

        self.refresh_button = ttk.Button(self.sessions_box, text="Refresh", command=self.refresh)
        self.refresh_button.grid(row=2, column=0, sticky="e", pady=(10, 0))

    def refresh(self) -> None:
        """Reload the latest sessions and review plan from local history."""

        plan = self.history.build_review_plan()
        sessions = self.history.recent_sessions(8)
        self.plan_label.configure(text=self._format_plan(plan))
        self.summary_label.configure(text=f"Recent sessions: {len(sessions)}")
        self._set_sessions_text(self._format_sessions(sessions))

    def _format_plan(self, plan: PracticeReviewPlan) -> str:
        pieces = [plan.note]
        if plan.essay_topic:
            pieces.append(f"Essay focus topic: {plan.essay_topic}.")
        if plan.vocab_topic:
            pieces.append(f"Vocabulary focus topic: {plan.vocab_topic}.")
        if plan.vocab_prompt_type:
            pieces.append(f"Vocabulary prompt style: {plan.vocab_prompt_type}.")
        if plan.challenge_type:
            pieces.append(f"Timed challenge focus: {plan.challenge_type}.")
        return " ".join(pieces)

    def _format_sessions(self, sessions) -> str:
        """Render a short text block so users can scan recent practice quickly."""

        if not sessions:
            return "No session history has been recorded yet."

        lines: list[str] = []
        for session in sessions:
            lines.append(
                f"- {session.created_at[:19]} | {session.mode.value} | {session.title} | "
                f"Accuracy {session.accuracy:.2f}% | Score {session.score}"
            )
        return "\n".join(lines)

    def _set_sessions_text(self, text: str) -> None:
        self.sessions_text.configure(state="normal")
        self.sessions_text.delete("1.0", tk.END)
        self.sessions_text.insert("1.0", text)
        self.sessions_text.configure(state="disabled")
