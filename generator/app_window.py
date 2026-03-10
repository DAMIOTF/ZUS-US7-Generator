"""
Główne okno aplikacji Generator ZUS US-7.

Klasa ``App`` dziedziczy po mixinach ``SectionsMixin`` i ``HandlersMixin``
oraz ``tk.Tk``.  Inicjalizacja, nagłówek, układ scrollowalny i helpery UI
pozostają tutaj — reszta jest w ``sections.py`` i ``handlers.py``.
"""
from __future__ import annotations

import datetime
import math
import os
import sys
import tkinter as tk
from tkinter import ttk

from .constants import (
    C_ACCENT, C_ACCENT2,
    C_BG, C_BORDER,
    C_SUBTEXT, C_SURFACE, C_SURFACE2,
    C_TEXT, C_WHITE,
    FONT_BODY, FONT_H3,
    resource_path,
)
from .handlers import HandlersMixin
from .sections import SectionsMixin


class App(SectionsMixin, HandlersMixin, tk.Tk):
    """Główne okno aplikacji."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Generator ZUS US-7")
        self.configure(bg=C_BG)
        self.resizable(True, True)
        self.minsize(760, 720)

        ico_path = resource_path("ico.ico")
        if os.path.isfile(ico_path):
            try:
                self.iconbitmap(ico_path)
            except Exception:
                pass

        # ── Wyśrodkowanie okna ────────────────────────────────────────────────
        w, h = 860, 830
        sw   = self.winfo_screenwidth()
        sh   = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        # ── Zmienne stanu ─────────────────────────────────────────────────────
        self._wb_path    = tk.StringVar()
        self._sheet_var  = tk.StringVar()
        self._date_var   = tk.StringVar(
            value=datetime.date.today().strftime("%d.%m.%Y"))
        self._output_var = tk.StringVar(
            value=os.path.join(
                os.path.dirname(os.path.abspath(sys.argv[0])), "wyniki"))

        # ── Zmienne checkboxów / radio ────────────────────────────────────────
        self._cv: dict = {
            "radio_type":        tk.StringVar(value="1"),
            "cb_ubezpieczenia":  tk.BooleanVar(value=True),
            "cb_przerwy":        tk.BooleanVar(value=False),
            "cb_podstawy":       tk.BooleanVar(value=False),
            "cb_warunki":        tk.BooleanVar(value=False),
            "cb_ofe_czlonek":    tk.BooleanVar(value=False),
            "cb_ofe_skladki":    tk.BooleanVar(value=False),
            "delivery_placowka": tk.BooleanVar(value=True),
            "delivery_poczta":   tk.BooleanVar(value=False),
            "delivery_pue":      tk.BooleanVar(value=False),
        }
        self._uzasadnienie_default = (
            "W związku z ubieganiem się o wsparcie w projekcie "
            "współfinansowanym ze środków EFS"
        )

        self._build_ui()
        self._start_header_animation()

    # =========================================================================
    # Animacja nagłówka
    # =========================================================================

    def _start_header_animation(self) -> None:
        self._hdr_phase = 0.0
        self._animate_header()

    def _animate_header(self) -> None:
        self._hdr_phase += 0.02
        t = (math.sin(self._hdr_phase) + 1) / 2
        r = int(13 + (21 - 13) * t)
        g = int(33 + (100 - 33) * t)
        b = int(55 + (140 - 55) * t)
        col = f"#{r:02x}{g:02x}{b:02x}"
        if hasattr(self, "_hdr_frame"):
            self._hdr_frame.configure(bg=col)
            self._hdr_title.configure(bg=col)
            self._hdr_sub.configure(bg=col)
        if hasattr(self, "_left_hdr"):
            self._left_hdr.configure(bg=col)
        self.after(50, self._animate_header)

    # =========================================================================
    # Budowanie UI
    # =========================================================================

    def _build_ui(self) -> None:
        self._build_header()
        self._build_scrollable_body()

    def _build_header(self) -> None:
        self._hdr_frame = tk.Frame(self, bg=C_BG, height=80)
        self._hdr_frame.pack(fill="x")
        self._hdr_frame.pack_propagate(False)

        self._left_hdr = tk.Frame(self._hdr_frame, bg=C_BG)
        self._left_hdr.pack(side="left", padx=28, fill="y")

        self._hdr_title = tk.Label(
            self._left_hdr, text="⚡  Generator ZUS US-7",
            font=("Segoe UI", 20, "bold"), bg=C_BG, fg=C_WHITE)
        self._hdr_title.pack(anchor="w", pady=(18, 0))

        self._hdr_sub = tk.Label(
            self._left_hdr,
            text="Masowe generowanie wniosków PDF — szybko, precyzyjnie, profesjonalnie",
            font=("Segoe UI", 9), bg=C_BG, fg=C_SUBTEXT)
        self._hdr_sub.pack(anchor="w")

        tk.Frame(self, bg=C_BORDER, height=1).pack(fill="x")

    def _build_scrollable_body(self) -> None:
        container    = tk.Frame(self, bg=C_BG)
        container.pack(fill="both", expand=True)

        self._canvas_scroll = tk.Canvas(container, bg=C_BG, bd=0, highlightthickness=0)
        canvas_scroll = self._canvas_scroll
        scrollbar     = ttk.Scrollbar(container, orient="vertical",
                                      command=canvas_scroll.yview)
        canvas_scroll.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas_scroll.pack(side="left", fill="both", expand=True)

        self._body        = tk.Frame(canvas_scroll, bg=C_BG)
        self._body_window = canvas_scroll.create_window(
            (0, 0), window=self._body, anchor="nw")

        self._body.bind(
            "<Configure>",
            lambda e: canvas_scroll.configure(
                scrollregion=canvas_scroll.bbox("all")))
        canvas_scroll.bind(
            "<Configure>",
            lambda e: canvas_scroll.itemconfig(self._body_window, width=e.width))
        canvas_scroll.bind_all(
            "<MouseWheel>",
            lambda e: canvas_scroll.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        pad = dict(padx=24, pady=0)
        body = self._body
        self._build_section_excel(body,          **pad)
        self._build_section_settings(body,       **pad)
        self._build_section_pdf_type(body,       **pad)
        self._build_section_checkboxes(body,     **pad)
        self._build_section_uzasadnienie(body,   **pad)
        self._build_section_delivery(body,       **pad)
        self._build_section_generate(body,       **pad)
        self._build_section_log(body,            **pad)
        self._build_footer(body)

        # Force initial body width sync so text is visible on first render
        self.after(50, self._sync_body_width)

    # =========================================================================
    # Pomocnicze metody UI
    # =========================================================================

    def _card(self, parent, title: str, icon: str = "●") -> tk.Frame:
        """Tworzy kartę z lewym paskiem akcentowym i zwraca kontener treści."""
        outer = tk.Frame(parent, bg=C_SURFACE, pady=0)
        outer.pack(fill="x", padx=0, pady=(0, 12))

        tk.Frame(outer, bg=C_ACCENT, width=4).pack(side="left", fill="y")

        inner = tk.Frame(outer, bg=C_SURFACE)
        inner.pack(side="left", fill="both", expand=True, padx=16, pady=14)

        title_row = tk.Frame(inner, bg=C_SURFACE)
        title_row.pack(fill="x", pady=(0, 10))
        tk.Label(title_row, text=f"{icon}  {title}",
                 font=FONT_H3, bg=C_SURFACE, fg=C_ACCENT2).pack(side="left")

        content = tk.Frame(inner, bg=C_SURFACE)
        content.pack(fill="x")
        return content

    def _section_wrap(
        self, parent, padx: int = 24,
        pady_top: int = 12, pady_bot: int = 4,
    ) -> tk.Frame:
        f = tk.Frame(parent, bg=C_BG)
        f.pack(fill="x", padx=padx, pady=(pady_top, pady_bot))
        return f

    @staticmethod
    def _style_btn(btn: tk.Button, small: bool = False) -> tk.Button:
        btn.configure(
            bg=C_SURFACE2, fg=C_SUBTEXT,
            activebackground=C_BORDER, activeforeground=C_TEXT,
            relief="flat", bd=0,
            padx=8 if small else 12,
            pady=2 if small else 5,
        )
        return btn

    def _padx_only(self, kw: dict) -> dict:
        return {k: v for k, v in kw.items() if k == "padx"}

    def _sync_body_width(self) -> None:
        """Synchronizuje szerokość body z canvasem po pierwszym renderze."""
        self.update_idletasks()
        cw = self._canvas_scroll.winfo_width()
        if cw > 1:
            self._canvas_scroll.itemconfig(self._body_window, width=cw)
