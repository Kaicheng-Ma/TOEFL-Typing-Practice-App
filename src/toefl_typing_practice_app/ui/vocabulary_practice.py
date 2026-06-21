"""Vocabulary spelling practice UI.

This frame keeps the interaction simple: show one prompt, accept one answer,
score it immediately, and move on to the next word.
"""

from __future__ import annotations

import time
import tkinter as tk
from tkinter import ttk

from ..content.vocabulary_bank import VocabularyPromptGenerator
from ..models import VocabularyPrompt
from ..services.vocabulary_scoring import VocabularyScoringResult, score_vocab_response


class VocabularyPracticeFrame(ttk.Frame):
    """Interactive vocabulary spelling panel."""

    def __init__(self, master: tk.Widget) -> None:
        super().__init__(master, padding=16)
        self.generator = VocabularyPromptGenerator()
        self.current_prompt: VocabularyPrompt | None = None
        self.session_started_at: float | None = None
        self.correct_count = 0
        self.wrong_count = 0
        self._build_layout()
        self.start_new_prompt()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)

        header = ttk.Frame(self)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(header, text="Vocabulary Spelling Mode", font=("Segoe UI", 14, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w")

        self.topic_label = ttk.Label(header, text="Topic: -")
        self.topic_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        controls = ttk.Frame(header)
        controls.grid(row=0, column=1, rowspan=2, sticky="e")

        self.new_button = ttk.Button(controls, text="New Prompt", command=self.start_new_prompt)
        self.new_button.grid(row=0, column=0, padx=(0, 8))

        self.submit_button = ttk.Button(controls, text="Check Answer", command=self.submit_response)
        self.submit_button.grid(row=0, column=1)

        prompt_box = ttk.LabelFrame(self, text="Prompt")
        prompt_box.grid(row=1, column=0, sticky="ew", pady=(16, 12))
        prompt_box.columnconfigure(0, weight=1)

        self.prompt_text = tk.Text(prompt_box, height=5, wrap="word", relief="flat", padx=8, pady=8)
        self.prompt_text.grid(row=0, column=0, sticky="nsew")
        self.prompt_text.configure(state="disabled")

        answer_box = ttk.LabelFrame(self, text="Your Answer")
        answer_box.grid(row=2, column=0, sticky="ew")
        answer_box.columnconfigure(0, weight=1)

        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(answer_box, textvariable=self.answer_var, font=("Segoe UI", 12))
        self.answer_entry.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        self.answer_entry.bind("<Return>", self._submit_from_keyboard)

        stats_box = ttk.Frame(self)
        stats_box.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        stats_box.columnconfigure(0, weight=1)

        self.stats_label = ttk.Label(stats_box, text="Accuracy: -    Correct: 0    Wrong: 0    Elapsed: -")
        self.stats_label.grid(row=0, column=0, sticky="w")

        self.result_label = ttk.Label(
            stats_box,
            text="Check your answer to see spelling feedback.",
            foreground="#444444",
            wraplength=860,
            justify="left",
        )
        self.result_label.grid(row=1, column=0, sticky="w", pady=(8, 0))

    def start_new_prompt(self) -> None:
        """Generate a new vocabulary prompt and reset the answer box."""

        self.current_prompt = self.generator.generate()
        self.session_started_at = time.perf_counter()
        self._set_prompt_text(self.current_prompt.prompt_text)
        self.topic_label.configure(text=f"Topic: {self.current_prompt.topic}")
        self.answer_var.set("")
        self.answer_entry.focus_set()
        self.result_label.configure(text="A fresh vocabulary item is ready.")
        self._refresh_stats()

    def submit_response(self) -> VocabularyScoringResult | None:
        """Score the typed answer and update the session summary."""

        if self.current_prompt is None or self.session_started_at is None:
            return None

        elapsed_seconds = time.perf_counter() - self.session_started_at
        typed_answer = self.answer_var.get()
        result = score_vocab_response(self.current_prompt, typed_answer)

        if result.is_correct:
            self.correct_count += 1
            feedback = (
                f"Correct. {self.current_prompt.answer} means {self.current_prompt.meaning}. "
                f"Example: {self.current_prompt.example}"
            )
        else:
            self.wrong_count += 1
            feedback = (
                f"Incorrect. Correct answer: {self.current_prompt.answer}. "
                f"Meaning: {self.current_prompt.meaning}. "
                f"Example: {self.current_prompt.example}"
            )

        accuracy = self._current_accuracy()
        self.stats_label.configure(
            text=(
                f"Accuracy: {accuracy:.2f}%    "
                f"Correct: {self.correct_count}    "
                f"Wrong: {self.wrong_count}    "
                f"Elapsed: {elapsed_seconds:.1f}s"
            )
        )
        self.result_label.configure(text=feedback)
        return result

    def _refresh_stats(self) -> None:
        accuracy = self._current_accuracy()
        elapsed_seconds = 0.0
        if self.session_started_at is not None:
            elapsed_seconds = time.perf_counter() - self.session_started_at
        self.stats_label.configure(
            text=(
                f"Accuracy: {accuracy:.2f}%    "
                f"Correct: {self.correct_count}    "
                f"Wrong: {self.wrong_count}    "
                f"Elapsed: {elapsed_seconds:.1f}s"
            )
        )

    def _current_accuracy(self) -> float:
        total = self.correct_count + self.wrong_count
        if total == 0:
            return 0.0
        return round((self.correct_count / total) * 100, 2)

    def _set_prompt_text(self, text: str) -> None:
        self.prompt_text.configure(state="normal")
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert("1.0", text)
        self.prompt_text.configure(state="disabled")

    def _submit_from_keyboard(self, event: tk.Event) -> str:
        self.submit_response()
        return "break"

