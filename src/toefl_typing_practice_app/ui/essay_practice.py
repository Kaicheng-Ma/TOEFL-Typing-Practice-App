"""Essay typing practice UI.

This frame provides the first real practice flow: generate a prompt, type it,
submit the input, and receive a compact result summary.
"""

from __future__ import annotations

from datetime import datetime, timezone
import time
import tkinter as tk
from tkinter import ttk

from ..content.essay_generator import EssayPromptGenerator
from ..models import EssayPrompt, PracticeMode, PracticeReviewPlan, PracticeSessionRecord, TextComparisonResult
from ..paths import get_data_dir
from ..services.practice_history import PracticeHistoryStore
from ..services.typing_analysis import compare_texts


class EssayPracticeFrame(ttk.Frame):
    """Interactive essay typing practice panel."""

    def __init__(self, master: tk.Widget) -> None:
        super().__init__(master, padding=16)
        self.generator = EssayPromptGenerator()
        self.history = PracticeHistoryStore(get_data_dir())
        self.current_prompt: EssayPrompt | None = None
        self.started_at: float | None = None
        self.review_plan = PracticeReviewPlan(note="Start a practice session to build a personalized review plan.")
        self._build_layout()
        self.start_new_prompt()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        header = ttk.Frame(self)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(header, text="Essay Typing Mode", font=("Segoe UI", 14, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w")

        self.topic_label = ttk.Label(header, text="Topic: -", foreground="#4d4d4d")
        self.topic_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.prompt_state_label = ttk.Label(
            header,
            text="A new prompt will appear here each round.",
            foreground="#6b6b6b",
        )
        self.prompt_state_label.grid(row=2, column=0, sticky="w", pady=(4, 0))

        controls = ttk.Frame(header)
        controls.grid(row=0, column=1, rowspan=2, sticky="e")

        self.new_button = ttk.Button(controls, text="New Prompt", command=self.start_new_prompt)
        self.new_button.grid(row=0, column=0, padx=(0, 8))

        self.submit_button = ttk.Button(controls, text="Submit", command=self.submit_response)
        self.submit_button.grid(row=0, column=1)

        prompt_box = ttk.LabelFrame(self, text="Prompt")
        prompt_box.grid(row=1, column=0, sticky="ew", pady=(16, 12))
        prompt_box.columnconfigure(0, weight=1)

        self.prompt_text = tk.Text(prompt_box, height=7, wrap="word", relief="flat", padx=8, pady=8)
        self.prompt_text.grid(row=0, column=0, sticky="nsew")
        self.prompt_text.configure(state="disabled")

        input_box = ttk.LabelFrame(self, text="Your Typing")
        input_box.grid(row=2, column=0, sticky="nsew")
        input_box.columnconfigure(0, weight=1)
        input_box.rowconfigure(0, weight=1)

        self.input_text = tk.Text(input_box, height=10, wrap="word", padx=8, pady=8)
        self.input_text.grid(row=0, column=0, sticky="nsew")
        self.input_text.bind("<KeyRelease>", self._update_live_stats)
        self.input_text.bind("<Control-Return>", self._submit_from_keyboard)

        output_box = ttk.Frame(self)
        output_box.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        output_box.columnconfigure(0, weight=1)

        self.summary_card = ttk.LabelFrame(output_box, text="Session Summary")
        self.summary_card.grid(row=0, column=0, sticky="ew")
        self.summary_card.columnconfigure(0, weight=1)

        self.stats_label = ttk.Label(self.summary_card, text="Accuracy: -    WPM: -    Elapsed: -")
        self.stats_label.grid(row=0, column=0, sticky="w", padx=8, pady=(8, 2))

        self.result_label = ttk.Label(
            self.summary_card,
            text="Submit to see your result summary.",
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

    def start_new_prompt(self) -> None:
        """Generate a fresh prompt and reset the practice state."""

        self.review_plan = self.history.build_review_plan()
        self.current_prompt = self.generator.generate(preferred_topic=self.review_plan.essay_topic)
        self.started_at = time.perf_counter()
        self._set_prompt_text(self.current_prompt.text)
        self.topic_label.configure(text=f"Topic: {self.current_prompt.title}")
        self.prompt_state_label.configure(text="Focus on punctuation and sentence flow while you type.")
        self.result_label.configure(text="A fresh prompt is ready. Start typing when you are ready.")
        self.review_label.configure(text=self.review_plan.note)
        self.stats_label.configure(text="Accuracy: -    WPM: -    Elapsed: 0.0s")
        self.input_text.delete("1.0", tk.END)
        self.input_text.focus_set()

    def submit_response(self) -> TextComparisonResult | None:
        """Compare the current answer and render a compact summary."""

        if not self.current_prompt or self.started_at is None:
            return None

        elapsed_seconds = time.perf_counter() - self.started_at
        typed_text = self.input_text.get("1.0", tk.END).strip()
        result = compare_texts(self.current_prompt.text, typed_text, elapsed_seconds)
        self._render_result(result)
        self._save_session(result, typed_text)
        return result

    def _render_result(self, result: TextComparisonResult) -> None:
        summary = (
            f"Accuracy: {result.accuracy:.2f}%    "
            f"WPM: {result.words_per_minute:.2f}    "
            f"Elapsed: {result.elapsed_seconds:.1f}s    "
            f"Typos: {result.typo_count}"
        )
        detail = (
            f"Correct characters: {result.correct_characters}/{result.total_characters}. "
            f"Submit Ctrl+Enter for quick practice review, or generate a new prompt for the next round."
        )
        self.stats_label.configure(text=summary)
        self.result_label.configure(text=detail)
        self.review_label.configure(text=self.review_plan.note)
        self.prompt_state_label.configure(text="Round complete. Use New Prompt for another pass or review the feedback below.")

    def _set_prompt_text(self, text: str) -> None:
        self.prompt_text.configure(state="normal")
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert("1.0", text)
        self.prompt_text.configure(state="disabled")

    def _update_live_stats(self, _event: tk.Event | None = None) -> None:
        if self.started_at is None or self.current_prompt is None:
            return

        elapsed_seconds = time.perf_counter() - self.started_at
        typed_text = self.input_text.get("1.0", tk.END).strip()
        result = compare_texts(self.current_prompt.text, typed_text, elapsed_seconds)
        self.stats_label.configure(
            text=(
                f"Accuracy: {result.accuracy:.2f}%    "
                f"WPM: {result.words_per_minute:.2f}    "
                f"Elapsed: {result.elapsed_seconds:.1f}s"
            )
        )

    def _submit_from_keyboard(self, event: tk.Event) -> str:
        self.submit_response()
        return "break"

    def _save_session(self, result: TextComparisonResult, typed_text: str) -> None:
        if self.current_prompt is None:
            return

        record = PracticeSessionRecord(
            mode=PracticeMode.ESSAY_TYPING,
            created_at=datetime.now(timezone.utc).isoformat(),
            title=self.current_prompt.title,
            topic=self.current_prompt.topic,
            accuracy=result.accuracy,
            elapsed_seconds=result.elapsed_seconds,
            completed_items=len(typed_text.split()),
            score=int(result.accuracy + result.words_per_minute),
            typo_count=result.typo_count,
            note=self.review_plan.note,
            target_text=self.current_prompt.text,
            typed_text=typed_text,
        )
        self.history.append_session(record)
