"""Timed challenge practice UI.

The timed challenge mode sits on top of essay-style practice but adds a fixed
time limit, challenge type selection, and a score that balances speed with
completion.
"""

from __future__ import annotations

from datetime import datetime, timezone
import time
import tkinter as tk
from tkinter import ttk

from ..content.timed_challenge_bank import TimedChallengePromptGenerator
from ..models import PracticeMode, PracticeReviewPlan, PracticeSessionRecord, TimedChallengePrompt
from ..paths import get_data_dir
from ..services.practice_history import PracticeHistoryStore
from ..services.timed_challenge_scoring import TimedChallengeResult, score_timed_challenge


class TimedChallengeFrame(ttk.Frame):
    """Interactive timed challenge panel."""

    def __init__(self, master: tk.Widget) -> None:
        super().__init__(master, padding=16)
        self.generator = TimedChallengePromptGenerator()
        self.history = PracticeHistoryStore(get_data_dir())
        self.current_prompt: TimedChallengePrompt | None = None
        self.started_at: float | None = None
        self.time_limit_seconds = 60
        self.challenge_type = tk.StringVar(value="content_sprint")
        self.time_limit_var = tk.IntVar(value=60)
        self.review_plan = PracticeReviewPlan(note="Start a timed challenge session to build a personalized review plan.")
        self._timer_job: str | None = None
        self._build_layout()
        self.start_new_challenge()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        header = ttk.Frame(self)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(header, text="Timed Challenge Mode", font=("Segoe UI", 14, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w")

        self.info_label = ttk.Label(
            header,
            text="Pick a challenge style and a time limit, then type as much as you can before time runs out.",
            wraplength=860,
            justify="left",
        )
        self.info_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.timer_label = ttk.Label(
            header,
            text="Time left: 00:00",
            foreground="#8b4513",
            font=("Segoe UI", 11, "bold"),
        )
        self.timer_label.grid(row=2, column=0, sticky="w", pady=(4, 0))

        controls = ttk.LabelFrame(self, text="Challenge Settings")
        controls.grid(row=1, column=0, sticky="ew", pady=(16, 12))
        controls.columnconfigure(1, weight=1)

        ttk.Label(controls, text="Challenge Type").grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))
        type_box = ttk.Frame(controls)
        type_box.grid(row=0, column=1, sticky="w", padx=8, pady=(8, 4))
        ttk.Radiobutton(
            type_box,
            text="Content Sprint",
            value="content_sprint",
            variable=self.challenge_type,
        ).pack(side="left", padx=(0, 16))
        ttk.Radiobutton(
            type_box,
            text="Item Sprint",
            value="item_sprint",
            variable=self.challenge_type,
        ).pack(side="left")

        ttk.Label(controls, text="Time Limit").grid(row=1, column=0, sticky="w", padx=8, pady=(4, 8))
        time_box = ttk.Frame(controls)
        time_box.grid(row=1, column=1, sticky="w", padx=8, pady=(4, 8))
        for label, value in (("30s", 30), ("60s", 60), ("180s", 180), ("300s", 300)):
            ttk.Radiobutton(
                time_box,
                text=label,
                value=value,
                variable=self.time_limit_var,
                command=self._sync_time_limit,
            ).pack(side="left", padx=(0, 12))

        action_bar = ttk.Frame(self)
        action_bar.grid(row=2, column=0, sticky="ew")
        action_bar.columnconfigure(0, weight=1)

        self.new_button = ttk.Button(action_bar, text="New Challenge", command=self.start_new_challenge)
        self.new_button.grid(row=0, column=0, sticky="w")

        self.submit_button = ttk.Button(action_bar, text="Submit", command=self.submit_response)
        self.submit_button.grid(row=0, column=1, sticky="e")

        prompt_box = ttk.LabelFrame(self, text="Challenge Prompt")
        prompt_box.grid(row=3, column=0, sticky="ew", pady=(16, 12))
        prompt_box.columnconfigure(0, weight=1)

        self.prompt_text = tk.Text(prompt_box, height=8, wrap="word", relief="flat", padx=8, pady=8)
        self.prompt_text.grid(row=0, column=0, sticky="nsew")
        self.prompt_text.configure(state="disabled")

        self.challenge_hint_label = ttk.Label(
            prompt_box,
            text="The score rewards both progress and accuracy, so steady typing usually beats rushing.",
            wraplength=860,
            justify="left",
            foreground="#666666",
        )
        self.challenge_hint_label.grid(row=1, column=0, sticky="w", padx=8, pady=(8, 0))

        input_box = ttk.LabelFrame(self, text="Your Input")
        input_box.grid(row=4, column=0, sticky="nsew")
        input_box.columnconfigure(0, weight=1)
        input_box.rowconfigure(0, weight=1)

        self.input_text = tk.Text(input_box, height=10, wrap="word", padx=8, pady=8)
        self.input_text.grid(row=0, column=0, sticky="nsew")
        self.input_text.bind("<KeyRelease>", self._update_live_stats)
        self.input_text.bind("<Control-Return>", self._submit_from_keyboard)

        stats_box = ttk.Frame(self)
        stats_box.grid(row=5, column=0, sticky="ew", pady=(12, 0))
        stats_box.columnconfigure(0, weight=1)

        self.summary_card = ttk.LabelFrame(stats_box, text="Session Summary")
        self.summary_card.grid(row=0, column=0, sticky="ew")
        self.summary_card.columnconfigure(0, weight=1)

        self.stats_label = ttk.Label(
            self.summary_card,
            text="Time Left: -    Completed: -    Score: -    Accuracy: -",
        )
        self.stats_label.grid(row=0, column=0, sticky="w", padx=8, pady=(8, 2))

        self.result_label = ttk.Label(
            self.summary_card,
            text="The timed challenge summary will appear here after you submit.",
            foreground="#444444",
            wraplength=860,
            justify="left",
        )
        self.result_label.grid(row=1, column=0, sticky="w", padx=8, pady=(4, 2))

        ttk.Separator(self.summary_card).grid(row=2, column=0, sticky="ew", padx=8, pady=8)

        self.review_label = ttk.Label(
            self.summary_card,
            text=self.review_plan.note,
            foreground="#2f4f4f",
            wraplength=860,
            justify="left",
        )
        self.review_label.grid(row=3, column=0, sticky="w", padx=8, pady=(0, 8))

    def start_new_challenge(self) -> None:
        """Generate a new challenge prompt and start the timer."""

        self._cancel_timer()
        self.review_plan = self.history.build_review_plan()
        self.time_limit_seconds = int(self.time_limit_var.get())
        if self.review_plan.challenge_type in {"content_sprint", "item_sprint"}:
            self.challenge_type.set(self.review_plan.challenge_type)
        self.current_prompt = self.generator.generate(
            challenge_type=self.challenge_type.get(),
            target_count=6 if self.challenge_type.get() == "content_sprint" else 10,
        )
        self.started_at = time.perf_counter()
        self._set_prompt_text(self.current_prompt.text)
        self.input_text.delete("1.0", tk.END)
        self.input_text.focus_set()
        self.result_label.configure(text="Challenge started. Type as much as you can before time expires.")
        self.review_label.configure(text=self.review_plan.note)
        self.challenge_hint_label.configure(
            text=f"Challenge mode: {self.current_prompt.title}. Focus on a steady pace and avoid unnecessary corrections."
        )
        self._schedule_timer_tick()
        self._update_live_stats()

    def submit_response(self) -> TimedChallengeResult | None:
        """Score the current attempt and show the challenge summary."""

        if self.current_prompt is None or self.started_at is None:
            return None

        elapsed_seconds = time.perf_counter() - self.started_at
        typed_text = self.input_text.get("1.0", tk.END).strip()
        result = score_timed_challenge(
            self.current_prompt,
            typed_text,
            elapsed_seconds,
            self.time_limit_seconds,
        )
        self._render_result(result)
        self._save_session(result, typed_text)
        self._cancel_timer()
        return result

    def _render_result(self, result: TimedChallengeResult) -> None:
        summary = (
            f"Score: {result.score}    "
            f"Completed: {result.completed_units}    "
            f"Accuracy: {result.accuracy:.2f}%    "
            f"Elapsed: {result.elapsed_seconds:.1f}s"
        )
        detail = (
            f"Challenge type: {result.prompt.challenge_type}. "
            f"Target units: {result.prompt.target_count}. "
            f"Type Ctrl+Enter to submit quickly or start a new challenge for another round."
        )
        self.stats_label.configure(text=summary)
        self.result_label.configure(text=detail)

    def _set_prompt_text(self, text: str) -> None:
        self.prompt_text.configure(state="normal")
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert("1.0", text)
        self.prompt_text.configure(state="disabled")

    def _sync_time_limit(self) -> None:
        self.time_limit_seconds = int(self.time_limit_var.get())
        self._update_live_stats()

    def _schedule_timer_tick(self) -> None:
        self._timer_job = self.after(200, self._timer_tick)

    def _cancel_timer(self) -> None:
        if self._timer_job is not None:
            self.after_cancel(self._timer_job)
            self._timer_job = None

    def _timer_tick(self) -> None:
        self._timer_job = None
        if self.started_at is None:
            return
        elapsed_seconds = time.perf_counter() - self.started_at
        if elapsed_seconds >= self.time_limit_seconds:
            self.submit_response()
            return
        self._update_live_stats()
        self._schedule_timer_tick()

    def _update_live_stats(self, _event: tk.Event | None = None) -> None:
        if self.started_at is None or self.current_prompt is None:
            return

        elapsed_seconds = time.perf_counter() - self.started_at
        remaining = max(self.time_limit_seconds - elapsed_seconds, 0.0)
        typed_text = self.input_text.get("1.0", tk.END).strip()
        word_count = len(typed_text.split()) if typed_text else 0
        result = score_timed_challenge(
            self.current_prompt,
            typed_text,
            elapsed_seconds,
            self.time_limit_seconds,
        )
        self.stats_label.configure(
            text=(
                f"Time Left: {remaining:.1f}s    "
                f"Completed: {result.completed_units}    "
                f"Score: {result.score}    "
                f"Accuracy: {result.accuracy:.2f}%    "
                f"Words: {word_count}"
            )
        )
        self.timer_label.configure(text=f"Time left: {int(remaining // 60):02d}:{int(remaining % 60):02d}")

    def _submit_from_keyboard(self, event: tk.Event) -> str:
        self.submit_response()
        return "break"

    def _save_session(self, result: TimedChallengeResult, typed_text: str) -> None:
        if self.current_prompt is None:
            return

        record = PracticeSessionRecord(
            mode=PracticeMode.TIMED_CHALLENGE,
            created_at=datetime.now(timezone.utc).isoformat(),
            title=self.current_prompt.title,
            topic=self.current_prompt.challenge_type,
            accuracy=result.accuracy,
            elapsed_seconds=result.elapsed_seconds,
            completed_items=result.completed_units,
            score=result.score,
            challenge_type=self.current_prompt.challenge_type,
            note=self.review_plan.note,
            target_text=self.current_prompt.text,
            typed_text=typed_text,
        )
        self.history.append_session(record)
