"""Main application window.

The shell keeps the stage-based navigation visible while the essay practice
panel provides the first real interactive workflow.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..config import AppConfig
from ..models import PracticeMode
from .essay_practice import EssayPracticeFrame
from .review_center import ReviewCenterFrame
from .stats_dashboard import StatsDashboardFrame
from .vocabulary_practice import VocabularyPracticeFrame
from .timed_challenge import TimedChallengeFrame


class MainWindow(ttk.Frame):
    """Primary window frame that hosts the mode navigation and content area."""

    def __init__(self, master: tk.Tk, config: AppConfig) -> None:
        super().__init__(master, padding=18)
        self.master = master
        self.config = config
        self.mode_views: dict[PracticeMode, ttk.Frame] = {}
        self._build_layout()

    def _build_layout(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        header = ttk.Frame(self)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")

        title = ttk.Label(header, text=self.config.app_name, font=("Segoe UI", 20, "bold"))
        title.pack(anchor="w")

        subtitle = ttk.Label(
            header,
            text="Dynamic TOEFL typing drills for essays, vocabulary, and timed challenges.",
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        sidebar = ttk.Frame(self)
        sidebar.grid(row=1, column=0, sticky="nsw", padx=(0, 16), pady=(16, 0))

        ttk.Label(sidebar, text="Practice Modes", font=("Segoe UI", 11, "bold")).pack(anchor="w")

        ttk.Button(sidebar, text="Review Center", command=self.show_review_center).pack(fill="x", pady=(8, 6))
        ttk.Button(sidebar, text="Stats Dashboard", command=self.show_stats_dashboard).pack(fill="x", pady=(0, 6))

        mode_specs = [
            (PracticeMode.ESSAY_TYPING, "Essay Typing"),
            (PracticeMode.VOCABULARY_SPELLING, "Vocabulary Spelling"),
            (PracticeMode.TIMED_CHALLENGE, "Timed Challenge"),
        ]
        for index, (mode, label) in enumerate(mode_specs):
            button = ttk.Button(sidebar, text=label, command=lambda m=mode: self.show_mode(m))
            button.pack(fill="x", pady=(8 if index == 0 else 6, 0))

        content = ttk.Frame(self, relief="groove", padding=16)
        content.grid(row=1, column=1, sticky="nsew", pady=(16, 0))
        content.columnconfigure(0, weight=1)
        content.rowconfigure(3, weight=1)

        ttk.Label(content, text="Current Stage", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, sticky="w"
        )

        self.stage_label = ttk.Label(
            content,
            text="Stage 2: essay typing practice is active and ready for text generation, typing, and scoring.",
            wraplength=520,
            justify="left",
        )
        self.stage_label.grid(row=1, column=0, sticky="nw", pady=(8, 12))

        # A compact context line helps the user understand what action the
        # current panel expects without reading the whole page.
        self.context_label = ttk.Label(
            content,
            text="Choose a practice mode to start a focused session.",
            wraplength=520,
            justify="left",
            foreground="#4d4d4d",
        )
        self.context_label.grid(row=2, column=0, sticky="nw", pady=(0, 12))

        self.content_host = ttk.Frame(content)
        self.content_host.grid(row=3, column=0, sticky="nsew")
        self.content_host.columnconfigure(0, weight=1)
        self.content_host.rowconfigure(0, weight=1)

        self._build_mode_views()
        self.review_view = ReviewCenterFrame(self.content_host)
        self.review_view.grid(row=0, column=0, sticky="nsew")
        self.stats_view = StatsDashboardFrame(self.content_host)
        self.stats_view.grid(row=0, column=0, sticky="nsew")
        self.show_mode(PracticeMode.ESSAY_TYPING)

        footer = ttk.Label(
            self,
            text="Local implementation guide drives all later stages.",
            foreground="#555555",
        )
        footer.grid(row=2, column=0, columnspan=2, sticky="w", pady=(16, 0))

        self.pack(fill="both", expand=True)

    def _build_mode_views(self) -> None:
        """Create one frame per mode so the shell can swap views cleanly."""

        essay_view = EssayPracticeFrame(self.content_host)
        essay_view.grid(row=0, column=0, sticky="nsew")
        self.mode_views[PracticeMode.ESSAY_TYPING] = essay_view

        vocabulary_view = VocabularyPracticeFrame(self.content_host)
        vocabulary_view.grid(row=0, column=0, sticky="nsew")
        self.mode_views[PracticeMode.VOCABULARY_SPELLING] = vocabulary_view

        timed_view = TimedChallengeFrame(self.content_host)
        timed_view.grid(row=0, column=0, sticky="nsew")
        self.mode_views[PracticeMode.TIMED_CHALLENGE] = timed_view

    def _build_placeholder_view(self, mode: PracticeMode) -> ttk.Frame:
        """Return a temporary placeholder panel for modes not yet implemented."""

        frame = ttk.Frame(self.content_host, padding=12)
        ttk.Label(frame, text=self._mode_label(mode), font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(
            frame,
            text="This mode will be implemented in a later stage. The current stage keeps the navigation ready.",
            wraplength=560,
            justify="left",
        ).pack(anchor="w", pady=(8, 0))
        return frame

    def show_mode(self, mode: PracticeMode) -> None:
        """Raise the selected mode frame to the top of the content host."""

        view = self.mode_views.get(mode)
        if view is not None:
            view.tkraise()
        self.stage_label.configure(text=self._stage_message(mode))
        self.context_label.configure(text=self._context_message(mode))

    def show_review_center(self) -> None:
        """Show the review dashboard and refresh its content."""

        self.review_view.refresh()
        self.review_view.tkraise()
        self.stage_label.configure(text="Stage 5: review center and personalization data are now active.")
        self.context_label.configure(text="Review the latest sessions and see which topics the app will prioritize next.")

    def show_stats_dashboard(self) -> None:
        """Show the statistics dashboard and refresh its content."""

        self.stats_view.refresh()
        self.stats_view.tkraise()
        self.stage_label.configure(text="Stage 6: statistics and UX polish are now active.")
        self.context_label.configure(text="Inspect overall accuracy, mode balance, and recent trend data.")

    @staticmethod
    def _stage_message(mode: PracticeMode) -> str:
        if mode == PracticeMode.ESSAY_TYPING:
            return "Stage 2: essay typing practice is active and ready for text generation, typing, and scoring."
        if mode == PracticeMode.VOCABULARY_SPELLING:
            return "Stage 3: vocabulary spelling practice is now active alongside essay typing."
        return "Stage 4: timed challenge practice is now active with time limits and score-based feedback."

    @staticmethod
    def _context_message(mode: PracticeMode) -> str:
        """Explain the immediate task for the selected mode."""

        if mode == PracticeMode.ESSAY_TYPING:
            return "Essay mode focuses on sentence flow, punctuation, and long-form typing stability."
        if mode == PracticeMode.VOCABULARY_SPELLING:
            return "Vocabulary mode focuses on single-word recall and accurate spelling under light pressure."
        return "Timed challenge mode focuses on speed, completion, and accuracy balance within a fixed window."

    @staticmethod
    def _mode_label(mode: PracticeMode) -> str:
        labels = {
            PracticeMode.ESSAY_TYPING: "Essay Typing",
            PracticeMode.VOCABULARY_SPELLING: "Vocabulary Spelling",
            PracticeMode.TIMED_CHALLENGE: "Timed Challenge",
        }
        return labels[mode]
