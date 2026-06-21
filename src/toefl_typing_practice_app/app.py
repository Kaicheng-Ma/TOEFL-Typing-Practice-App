"""Application bootstrap and lifecycle management."""

from __future__ import annotations

import tkinter as tk

from .config import AppConfig
from .paths import get_data_dir
from .ui.main_window import MainWindow


class TypingPracticeApp:
    """Owns the Tk root window and wires the main screen together."""

    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or AppConfig()
        self.root = tk.Tk()
        self.root.title(self.config.app_name)
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        self.root.minsize(self.config.min_window_width, self.config.min_window_height)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # The data directory is created early so future stages can persist content
        # without having to duplicate path bootstrap logic.
        self.data_dir = get_data_dir()
        self.main_window = MainWindow(self.root, self.config)
        self.main_window.grid(row=0, column=0, sticky="nsew")

    def run(self) -> None:
        """Start the Tk event loop."""

        self.root.mainloop()


def create_app() -> TypingPracticeApp:
    """Factory used by scripts, tests, and the console entry point."""

    return TypingPracticeApp()

