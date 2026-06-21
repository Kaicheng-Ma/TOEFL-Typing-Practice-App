"""Main application window.

The shell keeps the stage-based navigation visible while the practice panels
provide the interactive workflow for the currently signed-in account.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from ..config import AppConfig
from ..models import PracticeMode
from ..services.account_store import AccountSessionContext
from .essay_practice import EssayPracticeFrame
from .review_center import ReviewCenterFrame
from .stats_dashboard import StatsDashboardFrame
from .timed_challenge import TimedChallengeFrame
from .vocabulary_practice import VocabularyPracticeFrame


class MainWindow(ttk.Frame):
    """Primary window frame that hosts the mode navigation and content area."""

    def __init__(
        self,
        master: tk.Tk,
        config: AppConfig,
        account_context: AccountSessionContext,
        on_switch_account=None,
    ) -> None:
        super().__init__(master, padding=18)
        self.master = master
        self.config = config
        self.account_context = account_context
        self.on_switch_account = on_switch_account
        self.mode_views: dict[PracticeMode, ttk.Frame] = {}
        self.current_practice_mode = PracticeMode.ESSAY_TYPING
        self._build_layout()
        self._bind_shortcuts()

    def _build_layout(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        header = ttk.Frame(self)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)

        title_block = ttk.Frame(header)
        title_block.grid(row=0, column=0, sticky="w")
        title = ttk.Label(title_block, text=self.config.app_name, font=("Segoe UI", 20, "bold"))
        title.pack(anchor="w")

        subtitle = ttk.Label(
            title_block,
            text="Dynamic TOEFL typing drills for essays, vocabulary, and timed challenges.",
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        self.account_label = ttk.Label(
            header,
            text=f"Signed in as {self.account_context.profile.username}",
            foreground="#4d4d4d",
        )
        self.account_label.grid(row=0, column=1, sticky="e")

        sidebar = ttk.Frame(self)
        sidebar.grid(row=1, column=0, sticky="nsw", padx=(0, 16), pady=(16, 0))

        ttk.Label(sidebar, text="Practice Modes", font=("Segoe UI", 11, "bold")).pack(anchor="w")

        account_card = ttk.LabelFrame(sidebar, text="Current Account")
        account_card.pack(fill="x", pady=(8, 10))
        account_card.columnconfigure(0, weight=1)
        ttk.Label(account_card, text=self.account_context.profile.username, font=("Segoe UI", 10, "bold")).grid(
            row=0, column=0, sticky="w", padx=8, pady=(8, 2)
        )
        self.account_state_label = ttk.Label(
            account_card,
            text=self._password_state_text(),
            wraplength=180,
            justify="left",
            foreground="#666666",
        )
        self.account_state_label.grid(row=1, column=0, sticky="w", padx=8, pady=(0, 8))
        ttk.Button(account_card, text="Change Password", command=self._open_password_dialog).grid(
            row=2, column=0, sticky="ew", padx=8, pady=(0, 6)
        )
        ttk.Button(account_card, text="Switch Account", command=self._switch_account).grid(
            row=3, column=0, sticky="ew", padx=8, pady=(0, 8)
        )

        ttk.Button(sidebar, text="Review Center", command=self.show_review_center).pack(fill="x", pady=(8, 6))
        ttk.Button(sidebar, text="Stats Dashboard", command=self.show_stats_dashboard).pack(fill="x", pady=(0, 6))
        if self.on_switch_account is not None:
            ttk.Button(sidebar, text="Switch Account", command=self._switch_account).pack(fill="x", pady=(0, 6))

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
        content.rowconfigure(4, weight=1)

        ttk.Label(content, text="Current Stage", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w")

        self.stage_label = ttk.Label(
            content,
            text="Stage 2: essay typing practice is active and ready for text generation, typing, and scoring.",
            wraplength=520,
            justify="left",
        )
        self.stage_label.grid(row=1, column=0, sticky="nw", pady=(8, 12))

        self.context_label = ttk.Label(
            content,
            text="Choose a practice mode to start a focused session.",
            wraplength=520,
            justify="left",
            foreground="#4d4d4d",
        )
        self.context_label.grid(row=2, column=0, sticky="nw", pady=(0, 12))

        self.shortcut_label = ttk.Label(
            content,
            text="Shortcuts: Ctrl+1/2/3 switch modes, Ctrl+4 review, Ctrl+5 stats, Esc return to practice.",
            wraplength=520,
            justify="left",
            foreground="#666666",
        )
        self.shortcut_label.grid(row=3, column=0, sticky="nw", pady=(0, 12))

        self.content_host = ttk.Frame(content)
        self.content_host.grid(row=4, column=0, sticky="nsew")
        self.content_host.columnconfigure(0, weight=1)
        self.content_host.rowconfigure(0, weight=1)

        self._build_mode_views()
        self.review_view = ReviewCenterFrame(
            self.content_host,
            on_resume=self.resume_practice,
            history_store=self.account_context.history_store,
            review_store=self.account_context.review_store,
        )
        self.review_view.grid(row=0, column=0, sticky="nsew")
        self.stats_view = StatsDashboardFrame(
            self.content_host,
            on_resume=self.resume_practice,
            history_store=self.account_context.history_store,
            account_name=self.account_context.profile.username,
        )
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

        essay_view = EssayPracticeFrame(self.content_host, history_store=self.account_context.history_store)
        essay_view.grid(row=0, column=0, sticky="nsew")
        self.mode_views[PracticeMode.ESSAY_TYPING] = essay_view

        vocabulary_view = VocabularyPracticeFrame(
            self.content_host,
            history_store=self.account_context.history_store,
            review_store=self.account_context.review_store,
        )
        vocabulary_view.grid(row=0, column=0, sticky="nsew")
        self.mode_views[PracticeMode.VOCABULARY_SPELLING] = vocabulary_view

        timed_view = TimedChallengeFrame(self.content_host, history_store=self.account_context.history_store)
        timed_view.grid(row=0, column=0, sticky="nsew")
        self.mode_views[PracticeMode.TIMED_CHALLENGE] = timed_view

    def show_mode(self, mode: PracticeMode) -> None:
        """Raise the selected mode frame to the top of the content host."""

        self.current_practice_mode = mode
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
        self.context_label.configure(text="Review the latest sessions, spaced review queue, and next focus items.")

    def show_stats_dashboard(self) -> None:
        """Show the statistics dashboard and refresh its content."""

        self.stats_view.refresh()
        self.stats_view.tkraise()
        self.stage_label.configure(text="Stage 6: statistics and UX polish are now active.")
        self.context_label.configure(text="Inspect overall accuracy, mode balance, and account-level summary data.")

    def resume_practice(self) -> None:
        """Return to the most recently selected practice mode."""

        self.show_mode(self.current_practice_mode)

    def _switch_account(self) -> None:
        """Return to the account gate so another learner can sign in."""

        if self.on_switch_account is not None:
            self.on_switch_account()

    def _password_state_text(self) -> str:
        if self.account_context.profile.password_hash:
            return "Password enabled. You can change or clear it from here."
        return "No password set. Use Change Password to add one if needed."

    def _open_password_dialog(self) -> None:
        """Open a small modal dialog for changing the current account password."""

        dialog = tk.Toplevel(self)
        dialog.title("Change Password")
        dialog.transient(self.master)
        dialog.grab_set()
        dialog.resizable(False, False)

        ttk.Label(
            dialog,
            text="Leave the field blank to remove the password.",
            wraplength=340,
            justify="left",
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(12, 8))

        ttk.Label(dialog, text="New Password").grid(row=1, column=0, sticky="w", padx=12, pady=4)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(dialog, textvariable=password_var, show="*")
        password_entry.grid(row=1, column=1, sticky="ew", padx=12, pady=4)
        dialog.columnconfigure(1, weight=1)

        status_label = ttk.Label(dialog, text="", foreground="#8b4513", wraplength=340, justify="left")
        status_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=12, pady=(4, 8))

        def apply_change() -> None:
            try:
                updated_profile = self.account_context.registry.update_password(
                    self.account_context.profile.username,
                    password_var.get(),
                )
            except ValueError as exc:
                status_label.configure(text=str(exc))
                return
            self.account_context.profile = updated_profile
            self.account_label.configure(text=f"Signed in as {self.account_context.profile.username}")
            self.account_state_label.configure(text=self._password_state_text())
            messagebox.showinfo("Password Updated", "The account password has been updated.")
            dialog.destroy()

        button_bar = ttk.Frame(dialog)
        button_bar.grid(row=3, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 12))
        ttk.Button(button_bar, text="Save", command=apply_change).pack(side="left")
        ttk.Button(button_bar, text="Cancel", command=dialog.destroy).pack(side="right")
        password_entry.focus_set()

    def _bind_shortcuts(self) -> None:
        """Register global shortcuts for quick mode switching and navigation."""

        self.master.bind_all("<Control-1>", lambda _event: self._switch_mode_from_shortcut(PracticeMode.ESSAY_TYPING))
        self.master.bind_all(
            "<Control-2>", lambda _event: self._switch_mode_from_shortcut(PracticeMode.VOCABULARY_SPELLING)
        )
        self.master.bind_all(
            "<Control-3>", lambda _event: self._switch_mode_from_shortcut(PracticeMode.TIMED_CHALLENGE)
        )
        self.master.bind_all("<Control-4>", lambda _event: self.show_review_center())
        self.master.bind_all("<Control-5>", lambda _event: self.show_stats_dashboard())
        self.master.bind_all("<Escape>", lambda _event: self.resume_practice())

    def destroy(self) -> None:
        """Unbind global shortcuts before the frame is torn down."""

        for sequence in ("<Control-1>", "<Control-2>", "<Control-3>", "<Control-4>", "<Control-5>", "<Escape>"):
            try:
                self.master.unbind_all(sequence)
            except tk.TclError:
                pass
        super().destroy()

    def _switch_mode_from_shortcut(self, mode: PracticeMode) -> str:
        """Switch modes from a keyboard shortcut and stop event bubbling."""

        self.show_mode(mode)
        return "break"

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
