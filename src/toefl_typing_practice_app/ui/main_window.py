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
        content.rowconfigure(2, weight=1)

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

        self.content_host = ttk.Frame(content)
        self.content_host.grid(row=2, column=0, sticky="nsew")
        self.content_host.columnconfigure(0, weight=1)
        self.content_host.rowconfigure(0, weight=1)

        self._build_mode_views()
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

        for mode in (PracticeMode.VOCABULARY_SPELLING, PracticeMode.TIMED_CHALLENGE):
            placeholder = self._build_placeholder_view(mode)
            placeholder.grid(row=0, column=0, sticky="nsew")
            self.mode_views[mode] = placeholder

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

    @staticmethod
    def _stage_message(mode: PracticeMode) -> str:
        if mode == PracticeMode.ESSAY_TYPING:
            return "Stage 2: essay typing practice is active and ready for text generation, typing, and scoring."
        if mode == PracticeMode.VOCABULARY_SPELLING:
            return "Stage 3 will add vocabulary spelling practice after the essay workflow is settled."
        return "Stage 4 will add the timed challenge workflow on top of essay typing."

    @staticmethod
    def _mode_label(mode: PracticeMode) -> str:
        labels = {
            PracticeMode.ESSAY_TYPING: "Essay Typing",
            PracticeMode.VOCABULARY_SPELLING: "Vocabulary Spelling",
            PracticeMode.TIMED_CHALLENGE: "Timed Challenge",
        }
        return labels[mode]

