"""
Metody budujące poszczególne sekcje formularza GUI.

Klasa ``SectionsMixin`` jest wmiksowana do ``App`` i zawiera
wszystkie metody ``_build_section_*`` oraz ``_build_footer``.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
import webbrowser

from .constants import (
    C_ACCENT, C_ACCENT2, C_ACCENT_DK,
    C_BG, C_BORDER,
    C_GREEN, C_RED, C_SUBTEXT, C_SURFACE, C_SURFACE2,
    C_TEXT, C_WHITE, C_YELLOW,
    FONT_BODY, FONT_H3, FONT_LOG, FONT_SM,
    GITHUB_URL,
)
from .widgets import AnimatedButton, ModernCheckbox, ProgressBar, PulsingDot


class SectionsMixin:
    """Mixin — sekcje formularza (budowa widgetów)."""

    # ── Źródło danych ─────────────────────────────────────────────────────────

    def _build_section_excel(self, parent, **kw) -> None:
        wrap  = self._section_wrap(parent, **self._padx_only(kw),
                                   pady_top=16, pady_bot=0)
        inner = self._card(wrap, "Źródło danych — plik Excel", "📂")

        file_row = tk.Frame(inner, bg=C_SURFACE)
        file_row.pack(fill="x", pady=(0, 8))

        self._file_entry = tk.Entry(
            file_row, textvariable=self._wb_path,
            font=FONT_BODY, relief="flat", bd=0,
            bg=C_SURFACE2, fg=C_TEXT, insertbackground=C_TEXT,
            state="readonly", readonlybackground=C_SURFACE2)
        self._file_entry.pack(side="left", fill="x", expand=True,
                              ipady=7, padx=(0, 10))

        AnimatedButton(file_row, text="Wybierz plik Excel",
                       command=self._browse_excel,
                       width=170, height=34, font=FONT_BODY).pack(side="left")

        sheet_row = tk.Frame(inner, bg=C_SURFACE)
        sheet_row.pack(fill="x")

        tk.Label(sheet_row, text="Arkusz:", font=FONT_BODY,
                 bg=C_SURFACE, fg=C_SUBTEXT).pack(side="left", padx=(0, 10))

        self._setup_combobox_style()
        self._sheet_cb = ttk.Combobox(
            sheet_row, textvariable=self._sheet_var,
            font=FONT_BODY, state="readonly",
            width=38, style="Dark.TCombobox")
        self._sheet_cb.pack(side="left", ipady=5)
        self._sheet_cb.bind("<<ComboboxSelected>>", self._on_sheet_selected)

        self._record_count_lbl = tk.Label(
            sheet_row, text="", font=FONT_SM, bg=C_SURFACE, fg=C_SUBTEXT)
        self._record_count_lbl.pack(side="left", padx=14)

    def _setup_combobox_style(self) -> None:
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Dark.TCombobox",
                    fieldbackground=C_SURFACE2, background=C_SURFACE2,
                    foreground=C_TEXT, arrowcolor=C_ACCENT,
                    bordercolor=C_BORDER, lightcolor=C_SURFACE2,
                    darkcolor=C_SURFACE2, selectbackground=C_ACCENT,
                    selectforeground=C_WHITE)
        s.map("Dark.TCombobox",
              fieldbackground=[("readonly", C_SURFACE2)],
              foreground=[("readonly", C_TEXT)])

    # ── Ustawienia ────────────────────────────────────────────────────────────

    def _build_section_settings(self, parent, **kw) -> None:
        wrap  = self._section_wrap(parent, **self._padx_only(kw),
                                   pady_top=0, pady_bot=0)
        inner = self._card(wrap, "Ustawienia generowania", "⚙")

        grid = tk.Frame(inner, bg=C_SURFACE)
        grid.pack(fill="x")
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(3, weight=1)

        tk.Label(grid, text="Data wniosku:", font=FONT_BODY,
                 bg=C_SURFACE, fg=C_SUBTEXT).grid(
                     row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        self._date_entry = tk.Entry(
            grid, textvariable=self._date_var,
            font=FONT_BODY, relief="flat", bd=0,
            bg=C_SURFACE2, fg=C_TEXT, insertbackground=C_TEXT, width=14)
        self._date_entry.grid(row=0, column=1, sticky="w",
                              ipady=6, padx=(0, 24))

        tk.Label(grid, text="Folder wynikowy:", font=FONT_BODY,
                 bg=C_SURFACE, fg=C_SUBTEXT).grid(
                     row=0, column=2, sticky="w", padx=(0, 8))
        out_inner = tk.Frame(grid, bg=C_SURFACE)
        out_inner.grid(row=0, column=3, sticky="ew")

        tk.Entry(out_inner, textvariable=self._output_var,
                 font=FONT_BODY, relief="flat", bd=0,
                 bg=C_SURFACE2, fg=C_TEXT, state="readonly",
                 readonlybackground=C_SURFACE2, width=28).pack(
                     side="left", fill="x", expand=True, ipady=6, padx=(0, 8))
        AnimatedButton(out_inner, text="Zmień folder",
                       command=self._browse_output,
                       bg=C_SURFACE2, bg_hover=C_BORDER, bg_press=C_BORDER,
                       fg=C_ACCENT2, width=110, height=30,
                       font=("Segoe UI", 9)).pack(side="left")

    # ── Rodzaj dokumentu ──────────────────────────────────────────────────────

    def _build_section_pdf_type(self, parent, **kw) -> None:
        wrap  = self._section_wrap(parent, **self._padx_only(kw),
                                   pady_top=0, pady_bot=0)
        inner = self._card(wrap, "Rodzaj dokumentu (pkt 2 formularza)", "📄")

        row = tk.Frame(inner, bg=C_SURFACE)
        row.pack(fill="x")

        for val, label, tip in [
            ("1", "ZAŚWIADCZENIA", "Wniosek o wydanie zaświadczenia"),
            ("2", "INFORMACJI",    "Wniosek o udostępnienie informacji"),
        ]:
            opt_frame = tk.Frame(row, bg=C_SURFACE)
            opt_frame.pack(side="left", padx=(0, 28))

            tk.Radiobutton(
                opt_frame,
                text=f"  {label}",
                variable=self._cv["radio_type"], value=val,
                font=("Segoe UI", 11, "bold"),
                bg=C_SURFACE, fg=C_TEXT,
                activebackground=C_SURFACE, activeforeground=C_ACCENT2,
                selectcolor=C_SURFACE2, indicatoron=True, cursor="hand2",
            ).pack(side="left")
            tk.Label(opt_frame, text=tip, font=FONT_SM,
                     bg=C_SURFACE, fg=C_SUBTEXT).pack(side="left", padx=(4, 0))

    # ── Checkboxy (pkt 3) ────────────────────────────────────────────────────

    def _build_section_checkboxes(self, parent, **kw) -> None:
        wrap  = self._section_wrap(parent, **self._padx_only(kw),
                                   pady_top=0, pady_bot=0)
        inner = self._card(wrap, "Jakie dane / zaświadczenia (pkt 3 formularza)", "☑")

        checkboxes_info = [
            ("cb_ubezpieczenia",
             "o zgłoszeniu i okresach podlegania ubezpieczeniom społecznym",
             "CheckBox 1"),

            ("cb_przerwy",
             "o przerwach w opłacaniu składek",
             "CheckBox 2"),

            ("cb_podstawy",
             "o podstawach wymiaru składek",
             "CheckBox 3"),

            ("cb_warunki",
             "o zgłoszeniu przez pracodawcę informacji o wykonywaniu pracy "
             "w szczególnych warunkach lub o szczególnym charakterze",
             "CheckBox 4"),

            ("cb_ofe_czlonek",
             "w zakresie danych o członkostwie w otwartym funduszu emerytalnym (OFE)",
             "CheckBox 5"),

            ("cb_ofe_skladki",
             "o składkach przekazanych do OFE za okres",
             "CheckBox 6"),
        ]

        grid = tk.Frame(inner, bg=C_SURFACE)
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1, uniform="cb_col")
        grid.columnconfigure(1, weight=1, uniform="cb_col")

        for idx, (key, label, tip) in enumerate(checkboxes_info):
            col     = idx % 2
            row_idx = idx // 2
            cell    = tk.Frame(grid, bg=C_SURFACE)
            cell.grid(row=row_idx, column=col, sticky="ew",
                      padx=(0, 20) if col == 0 else (0, 0), pady=4)

            ModernCheckbox(cell, text=label,
                           variable=self._cv[key],
                           fg=C_TEXT, font=FONT_BODY,
                           wraplength=310).pack(anchor="w", fill="x")
            tk.Label(cell, text=tip, font=("Segoe UI", 8),
                     bg=C_SURFACE, fg=C_SUBTEXT).pack(anchor="w", padx=(28, 0))

    # ── Uzasadnienie (pkt 4) ─────────────────────────────────────────────────

    def _build_section_uzasadnienie(self, parent, **kw) -> None:
        wrap  = self._section_wrap(parent, **self._padx_only(kw),
                                   pady_top=0, pady_bot=0)
        inner = self._card(wrap, "Uzasadnienie wniosku (pkt 4 formularza)", "✏")

        self._uzas_text = tk.Text(
            inner, font=FONT_BODY, relief="flat", bd=0,
            bg=C_SURFACE2, fg=C_TEXT, insertbackground=C_TEXT,
            height=3, wrap="word")
        self._uzas_text.insert("1.0", self._uzasadnienie_default)
        self._uzas_text.pack(fill="x", ipady=6, pady=(0, 6))

        hint_row = tk.Frame(inner, bg=C_SURFACE)
        hint_row.pack(fill="x")
        tk.Label(hint_row,
                 text="Tekst zostanie wpisany identycznie do każdego wniosku.",
                 font=("Segoe UI", 8), bg=C_SURFACE, fg=C_SUBTEXT).pack(
                     side="left")
        AnimatedButton(hint_row, text="Przywróć domyślny",
                       command=self._reset_uzas,
                       bg=C_SURFACE2, bg_hover=C_BORDER, bg_press=C_BORDER,
                       fg=C_SUBTEXT, width=150, height=26,
                       font=("Segoe UI", 8)).pack(side="right")

    # ── Sposób odbioru (pkt 5) ────────────────────────────────────────────────

    def _build_section_delivery(self, parent, **kw) -> None:
        wrap  = self._section_wrap(parent, **self._padx_only(kw),
                                   pady_top=0, pady_bot=0)
        inner = self._card(wrap, "Sposób odbioru zaświadczenia (pkt 5 formularza)", "📬")

        row = tk.Frame(inner, bg=C_SURFACE)
        row.pack(fill="x")

        for key, label in [
            ("delivery_placowka", "W placówce ZUS\n(osobiście lub przez upoważnioną osobę)"),
            ("delivery_poczta",   "Pocztą\n(na adres wskazany we wniosku)"),
            ("delivery_pue",      "Konto PUE\n(profil na Platformie Usług Elektronicznych)"),
        ]:
            cell = tk.Frame(row, bg=C_SURFACE)
            cell.pack(side="left", padx=(0, 24), pady=2)
            ModernCheckbox(cell, text=label,
                           variable=self._cv[key],
                           fg=C_TEXT, font=("Segoe UI", 9)).pack()

    # ── Generowanie ──────────────────────────────────────────────────────────

    def _build_section_generate(self, parent, **kw) -> None:
        wrap = self._section_wrap(parent, **self._padx_only(kw),
                                  pady_top=0, pady_bot=0)
        gen_frame = tk.Frame(wrap, bg=C_BG)
        gen_frame.pack(fill="x", pady=(8, 0))

        stats_row = tk.Frame(gen_frame, bg=C_BG)
        stats_row.pack(fill="x", pady=(0, 8))

        self._stat_total = tk.Label(stats_row, text="Wierszy: —",
                                    font=FONT_SM, bg=C_BG, fg=C_SUBTEXT)
        self._stat_total.pack(side="left", padx=(0, 20))
        self._stat_ok = tk.Label(stats_row, text="OK: —",
                                 font=FONT_SM, bg=C_BG, fg=C_GREEN)
        self._stat_ok.pack(side="left", padx=(0, 20))
        self._stat_err = tk.Label(stats_row, text="Błędy: —",
                                  font=FONT_SM, bg=C_BG, fg=C_RED)
        self._stat_err.pack(side="left")

        self._progress_bar = ProgressBar(gen_frame, height=5)
        self._progress_bar.pack(fill="x", pady=(0, 10))

        btn_row = tk.Frame(gen_frame, bg=C_BG)
        btn_row.pack(fill="x")

        self._btn_generate = AnimatedButton(
            btn_row, text="⚡  Generuj PDF",
            command=self._on_generate,
            width=220, height=46,
            font=("Segoe UI", 13, "bold"))
        self._btn_generate._orig_command = self._on_generate
        self._btn_generate.pack(side="left")

        self._dot = PulsingDot(btn_row, size=14)
        self._dot.pack(side="left", padx=14, pady=16)

        self._status_lbl = tk.Label(btn_row, text="Gotowy do generowania",
                                    font=FONT_BODY, bg=C_BG, fg=C_SUBTEXT)
        self._status_lbl.pack(side="left")

    # ── Dziennik operacji ────────────────────────────────────────────────────

    def _build_section_log(self, parent, **kw) -> None:
        wrap = self._section_wrap(parent, **self._padx_only(kw),
                                  pady_top=16, pady_bot=8)

        log_card = tk.Frame(wrap, bg=C_SURFACE)
        log_card.pack(fill="x")

        title_row = tk.Frame(log_card, bg=C_SURFACE)
        title_row.pack(fill="x", padx=14, pady=(10, 4))
        tk.Label(title_row, text="🖥  Dziennik operacji",
                 font=FONT_H3, bg=C_SURFACE, fg=C_ACCENT2).pack(side="left")
        self._style_btn(
            tk.Button(title_row, text="Wyczyść", font=("Segoe UI", 8),
                      command=self._clear_log, cursor="hand2"),
            small=True,
        ).pack(side="right")

        log_inner = tk.Frame(log_card, bg=C_SURFACE2)
        log_inner.pack(fill="x", padx=14, pady=(0, 12))

        self._log = tk.Text(
            log_inner, font=FONT_LOG, bg=C_SURFACE2, fg=C_TEXT,
            relief="flat", state="disabled", wrap="word",
            height=10, bd=0, cursor="arrow",
            selectbackground=C_ACCENT, selectforeground=C_WHITE)
        self._log.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        sb = ttk.Scrollbar(log_inner, orient="vertical", command=self._log.yview)
        sb.pack(side="right", fill="y")
        self._log.configure(yscrollcommand=sb.set)

        self._log.tag_config("ok",    foreground=C_GREEN)
        self._log.tag_config("err",   foreground=C_RED)
        self._log.tag_config("inf",   foreground=C_ACCENT2)
        self._log.tag_config("warn",  foreground=C_YELLOW)
        self._log.tag_config("head",  foreground=C_WHITE,
                              font=("Consolas", 9, "bold"))
        self._log.tag_config("muted", foreground=C_SUBTEXT)

    # ── Stopka ───────────────────────────────────────────────────────────────

    def _build_footer(self, parent) -> None:
        tk.Frame(parent, bg=C_BORDER, height=1).pack(fill="x", pady=(8, 0))

        footer = tk.Frame(parent, bg=C_BG, height=36)
        footer.pack(fill="x")

        tk.Label(footer, text="Damian Marciniak  |  Generator ZUS US-7",
                 font=("Segoe UI", 8), bg=C_BG, fg=C_SUBTEXT).pack(
                     side="left", padx=24, pady=8)

        gh_frame = tk.Frame(footer, bg=C_BG, cursor="hand2")
        gh_frame.pack(side="right", padx=24, pady=8)

        gh_icon = tk.Label(gh_frame, text="⌗",
                           font=("Segoe UI", 11), bg=C_BG, fg=C_SUBTEXT,
                           cursor="hand2")
        gh_icon.pack(side="left", padx=(0, 4))

        gh_lbl = tk.Label(gh_frame, text="github.com/DAMIOTF",
                          font=("Segoe UI", 8, "underline"),
                          bg=C_BG, fg=C_SUBTEXT, cursor="hand2")
        gh_lbl.pack(side="left")

        def _open(_=None):
            webbrowser.open_new_tab(GITHUB_URL)

        def _enter(_=None):
            gh_lbl.configure(fg=C_ACCENT2)
            gh_icon.configure(fg=C_ACCENT2)

        def _leave(_=None):
            gh_lbl.configure(fg=C_SUBTEXT)
            gh_icon.configure(fg=C_SUBTEXT)

        for w in (gh_frame, gh_icon, gh_lbl):
            w.bind("<Button-1>", _open)
            w.bind("<Enter>", _enter)
            w.bind("<Leave>", _leave)
