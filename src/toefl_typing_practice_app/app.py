"""Application bootstrap and lifecycle management."""

from __future__ import annotations

import tkinter as tk

from .config import AppConfig
from .paths import get_data_dir
from .services.account_store import AccountRegistry, AccountSessionContext, PracticeAccountProfile
from .ui.account_gate import AccountGateFrame
from .ui.main_window import MainWindow


class TypingPracticeApp:
    """Owns the Tk root window and wires the login and practice screens."""

    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or AppConfig()
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            raise RuntimeError("Unable to start the desktop UI. Please make sure a graphical display is available.") from exc
        self.root.title(self.config.app_name)
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        self.root.minsize(self.config.min_window_width, self.config.min_window_height)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.data_dir = get_data_dir()
        self.account_registry = AccountRegistry(self.data_dir)
        self.active_account_context: AccountSessionContext | None = None
        self.current_view: tk.Widget | None = None
        self._show_account_gate()

    def _clear_current_view(self) -> None:
        if self.current_view is not None:
            self.current_view.destroy()
            self.current_view = None

    def _show_account_gate(self) -> None:
        """Show the login/create-account screen."""

        self._clear_current_view()
        self.active_account_context = None
        self.root.title(f"{self.config.app_name} - Login")
        gate = AccountGateFrame(self.root, self.account_registry, on_success=self._activate_account)
        gate.grid(row=0, column=0, sticky="nsew")
        self.current_view = gate

    def _activate_account(self, profile: PracticeAccountProfile) -> None:
        """Load the selected account and switch into the main practice shell."""

        self.active_account_context = self.account_registry.build_context(profile)
        self._show_main_window()

    def _show_main_window(self) -> None:
        """Build the practice UI for the active account."""

        if self.active_account_context is None:
            return

        self._clear_current_view()
        self.root.title(f"{self.config.app_name} - {self.active_account_context.profile.username}")
        try:
            window = MainWindow(
                self.root,
                self.config,
                self.active_account_context,
                on_switch_account=self._show_account_gate,
            )
            window.grid(row=0, column=0, sticky="nsew")
            self.current_view = window
        except Exception:
            self.root.destroy()
            raise

    def run(self) -> None:
        """Start the Tk event loop."""

        self.root.mainloop()


def create_app() -> TypingPracticeApp:
    """Factory used by scripts, tests, and the console entry point."""

    return TypingPracticeApp()
