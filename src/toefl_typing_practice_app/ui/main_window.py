"""Main application window.

The first UI stage stays intentionally minimal: a clear shell with navigation
areas and placeholders for the three core practice modes.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..config import AppConfig
from ..models import PracticeMode


class MainWindow(ttk.Frame):
    """Primary window frame that hosts the mode navigation and content area."""

    def __init__(self, master: tk.Tk, config: AppConfig) -> None:
        super().__init__(master, padding=18)
        self.master = master
        self.config = config
        self._build_layout()

    def _build_layout(self) -> None:
        # Stage 1 focus: establish visual structure first, then fill behavior later.
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

        self.mode_list = tk.Listbox(sidebar, height=8, activestyle="dotbox")
        for mode in PracticeMode:
            self.mode_list.insert(tk.END, self._mode_label(mode))
        self.mode_list.selection_set(0)
        self.mode_list.pack(fill="x", pady=(8, 0))

        content = ttk.Frame(self, relief="groove", padding=16)
        content.grid(row=1, column=1, sticky="nsew", pady=(16, 0))
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)

        ttk.Label(content, text="Current Stage", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, sticky="w"
        )

        self.stage_label = ttk.Label(
            content,
            text="Stage 1: framework shell is ready. The next stage will attach real practice flows.",
            wraplength=520,
            justify="left",
        )
        self.stage_label.grid(row=1, column=0, sticky="nw", pady=(8, 0))

        footer = ttk.Label(
            self,
            text="Local implementation guide drives all later stages.",
            foreground="#555555",
        )
        footer.grid(row=2, column=0, columnspan=2, sticky="w", pady=(16, 0))

        self.pack(fill="both", expand=True)

    @staticmethod
    def _mode_label(mode: PracticeMode) -> str:
        labels = {
            PracticeMode.ESSAY_TYPING: "作文打字模式",
            PracticeMode.VOCABULARY_SPELLING: "词汇拼写模式",
            PracticeMode.TIMED_CHALLENGE: "计时挑战模式",
        }
        return labels[mode]

