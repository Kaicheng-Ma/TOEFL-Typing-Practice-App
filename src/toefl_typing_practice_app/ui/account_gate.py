"""Account login and creation gate."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..services.account_store import AccountRegistry


class AccountGateFrame(ttk.Frame):
    """A simple entry screen that lets learners log in or create an account."""

    def __init__(self, master: tk.Widget, registry: AccountRegistry, on_success) -> None:
        super().__init__(master, padding=20)
        self.registry = registry
        self.on_success = on_success
        self._profiles_by_name = {}
        self._build_layout()
        self.refresh_accounts()

    def _build_layout(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        ttk.Label(self, text="Account Login", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(
            self,
            text="Choose an existing account or create a new one. Password is optional, and each account keeps its own practice data.",
            wraplength=860,
            justify="left",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(8, 16))

        list_card = ttk.LabelFrame(self, text="Existing Accounts")
        list_card.grid(row=2, column=0, sticky="nsw", padx=(0, 16))
        list_card.rowconfigure(0, weight=1)

        self.account_list = tk.Listbox(list_card, height=10, exportselection=False)
        self.account_list.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.account_list.bind("<<ListboxSelect>>", self._select_account)

        form_card = ttk.LabelFrame(self, text="Sign In Or Create")
        form_card.grid(row=2, column=1, sticky="nsew")
        form_card.columnconfigure(1, weight=1)

        ttk.Label(form_card, text="Username").grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(form_card, textvariable=self.username_var)
        self.username_entry.grid(row=0, column=1, sticky="ew", padx=8, pady=(8, 4))

        ttk.Label(form_card, text="Password").grid(row=1, column=0, sticky="w", padx=8, pady=4)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(form_card, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew", padx=8, pady=4)

        self.hint_label = ttk.Label(
            form_card,
            text="If an account has no password, leave the password field blank.",
            wraplength=460,
            justify="left",
            foreground="#666666",
        )
        self.hint_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=(4, 8))

        button_bar = ttk.Frame(form_card)
        button_bar.grid(row=3, column=0, columnspan=2, sticky="ew", padx=8, pady=(4, 8))
        button_bar.columnconfigure(0, weight=1)

        self.login_button = ttk.Button(button_bar, text="Log In", command=self._login)
        self.login_button.grid(row=0, column=0, sticky="w")

        self.create_button = ttk.Button(button_bar, text="Create Account", command=self._create_account)
        self.create_button.grid(row=0, column=1, sticky="e")

        self.refresh_button = ttk.Button(button_bar, text="Refresh List", command=self.refresh_accounts)
        self.refresh_button.grid(row=0, column=2, sticky="e", padx=(8, 0))

        self.status_label = ttk.Label(form_card, text="", foreground="#8b4513", wraplength=460, justify="left")
        self.status_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 8))

    def refresh_accounts(self) -> None:
        """Reload the account list from disk."""

        profiles = self.registry.list_accounts()
        self._profiles_by_name = {profile.username: profile for profile in profiles}
        self.account_list.delete(0, tk.END)
        for profile in profiles:
            suffix = "password set" if profile.password_hash else "no password"
            self.account_list.insert(tk.END, f"{profile.username} ({suffix})")
        if profiles:
            self.account_list.selection_set(0)
            self._select_account()

    def _select_account(self, _event: tk.Event | None = None) -> None:
        selection = self.account_list.curselection()
        if not selection:
            return
        label = self.account_list.get(selection[0])
        username = label.split(" (", 1)[0]
        self.username_var.set(username)
        profile = self._profiles_by_name.get(username)
        if profile and profile.password_hash:
            self.status_label.configure(text=f"{username} uses a password. Enter it and press Log In.")
        elif profile:
            self.status_label.configure(text=f"{username} has no password. You can log in with the username only.")

    def _login(self) -> None:
        username = self.username_var.get().strip()
        password = self.password_var.get()
        if not username:
            self.status_label.configure(text="Please enter a username.")
            return
        try:
            profile = self.registry.authenticate(username, password)
        except ValueError as exc:
            self.status_label.configure(text=str(exc))
            return
        self.status_label.configure(text=f"Welcome back, {profile.username}.")
        self.on_success(profile)

    def _create_account(self) -> None:
        username = self.username_var.get().strip()
        password = self.password_var.get()
        if not username:
            self.status_label.configure(text="Please enter a username.")
            return
        try:
            profile = self.registry.create_account(username, password)
        except ValueError as exc:
            self.status_label.configure(text=str(exc))
            return
        self.status_label.configure(text=f"Account created for {profile.username}.")
        self.on_success(profile)
