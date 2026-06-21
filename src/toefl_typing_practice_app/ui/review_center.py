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
from ..services.vocabulary_review import VocabularyReviewStore


class ReviewCenterFrame(ttk.Frame):
    """A lightweight dashboard for review and personalization."""

    def __init__(
        self,
        master: tk.Widget,
        on_resume=None,
        history_store: PracticeHistoryStore | None = None,
        review_store: VocabularyReviewStore | None = None,
    ) -> None:
        super().__init__(master, padding=16)
        self.history = history_store or PracticeHistoryStore(get_data_dir())
        self.review_store = review_store
        self.on_resume = on_resume
        self._build_layout()
        self.refresh()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ttk.Label(self, text="Review Center", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w")
        self.plan_card = ttk.LabelFrame(self, text="Personalized Review")
        self.plan_card.grid(row=1, column=0, sticky="ew", pady=(8, 12))
        self.plan_card.columnconfigure(0, weight=1)

        self.plan_label = ttk.Label(
            self.plan_card,
            text="",
            wraplength=860,
            justify="left",
            foreground="#2f4f4f",
        )
        self.plan_label.grid(row=0, column=0, sticky="w", padx=8, pady=8)

        self.sessions_card = ttk.LabelFrame(self, text="Recent Sessions")
        self.sessions_card.grid(row=2, column=0, sticky="nsew")
        self.sessions_card.columnconfigure(0, weight=1)

        self.summary_label = ttk.Label(
            self.sessions_card,
            text="Recent sessions will appear here.",
            wraplength=860,
            justify="left",
        )
        self.summary_label.grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))

        self.sessions_text = tk.Text(self.sessions_card, height=14, wrap="word", padx=8, pady=8)
        self.sessions_text.grid(row=1, column=0, sticky="nsew", padx=8, pady=(6, 0))
        self.sessions_text.configure(state="disabled")

        button_bar = ttk.Frame(self.sessions_card)
        button_bar.grid(row=2, column=0, sticky="ew", padx=8, pady=(10, 8))
        button_bar.columnconfigure(0, weight=1)

        self.resume_button = ttk.Button(button_bar, text="Resume Practice", command=self._resume)
        self.resume_button.grid(row=0, column=0, sticky="w")

        self.refresh_button = ttk.Button(button_bar, text="Refresh", command=self.refresh)
        self.refresh_button.grid(row=0, column=1, sticky="e")

    def refresh(self) -> None:
        """Reload the latest sessions and review plan from local history."""

        plan = self.history.build_review_plan()
        sessions = self.history.recent_sessions(8)
        self.plan_label.configure(text=self._format_plan(plan))
        self.summary_label.configure(text=f"Recent sessions: {len(sessions)}")
        sessions_text = self._format_sessions(sessions)
        if self.review_store is not None:
            sessions_text = sessions_text + "\n\n" + self.review_store.build_summary()
        self._set_sessions_text(sessions_text)

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

    def _resume(self) -> None:
        """Return to the practice view the user was most recently using."""

        if self.on_resume is not None:
            self.on_resume()
