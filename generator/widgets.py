# -*- coding: utf-8 -*-
"""
Niestandardowe widgety tkinter używane przez aplikację Generator ZUS US-7.

Zawiera:
    AnimatedButton   — płaski przycisk z animacją koloru hover/press
    ModernCheckbox   — ciemny checkbox z animowanym znacznikiem
    ProgressBar      — animowany pasek postępu
    PulsingDot       — pulsujący wskaźnik aktywności

Moduł rejestruje też metodę ``tk.Canvas.create_rounded_bg`` (monkey-patch)
dostępną globalnie dla wszystkich instancji Canvas w aplikacji.
"""
import math
import tkinter as tk
from typing import Optional

from .constants import (
    C_ACCENT, C_ACCENT2, C_ACCENT_DK,
    C_BORDER, C_GREEN, C_SURFACE2,
    C_TEXT, C_WHITE,
    FONT_BODY,
)


# ─── Canvas.create_rounded_bg (monkey-patch) ─────────────────────────────────

def _canvas_rounded_bg(
    self: tk.Canvas,
    x1: int, y1: int, x2: int, y2: int,
    r: int, fill: str, border: str = "",
) -> None:
    """Rysuje zaokrąglony prostokąt wypełniony kolorem *fill*.

    Opcjonalny parametr *border* dodaje widoczną ramkę.
    Używa techniki pieslice + rectangle bez widocznych szwów.
    """
    kw = {"fill": fill, "outline": fill}
    self.create_arc(x1,      y1,      x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kw)
    self.create_arc(x2-2*r,  y1,      x2,     y1+2*r, start=0,   extent=90,  style="pieslice", **kw)
    self.create_arc(x2-2*r,  y2-2*r,  x2,     y2,     start=270, extent=90,  style="pieslice", **kw)
    self.create_arc(x1,      y2-2*r,  x1+2*r, y2,     start=180, extent=90,  style="pieslice", **kw)
    self.create_rectangle(x1+r, y1, x2-r, y2, **kw)
    self.create_rectangle(x1, y1+r, x2, y2-r, **kw)
    if border:
        kw_b = {"fill": "", "outline": border}
        self.create_arc(x1,      y1,      x1+2*r, y1+2*r, start=90,  extent=90,  style="arc", **kw_b)
        self.create_arc(x2-2*r,  y1,      x2,     y1+2*r, start=0,   extent=90,  style="arc", **kw_b)
        self.create_arc(x2-2*r,  y2-2*r,  x2,     y2,     start=270, extent=90,  style="arc", **kw_b)
        self.create_arc(x1,      y2-2*r,  x1+2*r, y2,     start=180, extent=90,  style="arc", **kw_b)
        self.create_line(x1+r, y1, x2-r, y1, fill=border)
        self.create_line(x1+r, y2, x2-r, y2, fill=border)
        self.create_line(x1, y1+r, x1, y2-r, fill=border)
        self.create_line(x2, y1+r, x2, y2-r, fill=border)


tk.Canvas.create_rounded_bg = _canvas_rounded_bg  # type: ignore[attr-defined]


# ─── AnimatedButton ───────────────────────────────────────────────────────────

class AnimatedButton(tk.Canvas):
    """Płaski przycisk Canvas z płynną animacją koloru hover/press."""

    def __init__(
        self,
        parent,
        text: str = "",
        command=None,
        bg: str = C_ACCENT,
        bg_hover: str = C_ACCENT2,
        bg_press: str = C_ACCENT_DK,
        fg: str = C_WHITE,
        font=FONT_BODY,
        width: int = 160,
        height: int = 38,
        radius: int = 8,
        **kw,
    ) -> None:
        super().__init__(
            parent, width=width, height=height,
            bg=parent["bg"], bd=0, highlightthickness=0, **kw,
        )
        self._text       = text
        self._command    = command
        self._bg         = bg
        self._bg_hover   = bg_hover
        self._bg_press   = bg_press
        self._fg         = fg
        self._font       = font
        self._radius     = radius
        self._current_bg = bg

        self._draw(bg)
        self.bind("<Enter>",           self._on_enter)
        self.bind("<Leave>",           self._on_leave)
        self.bind("<ButtonPress-1>",   self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    # ── Colour helpers ────────────────────────────────────────────────────────

    @staticmethod
    def _hex_to_rgb(hex_col: str) -> tuple:
        h = hex_col.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def _rgb_to_hex(r, g, b) -> str:
        return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

    def _lerp_color(self, c1: str, c2: str, t: float) -> str:
        r1, g1, b1 = self._hex_to_rgb(c1)
        r2, g2, b2 = self._hex_to_rgb(c2)
        return self._rgb_to_hex(r1+(r2-r1)*t, g1+(g2-g1)*t, b1+(b2-b1)*t)

    # ── Drawing ───────────────────────────────────────────────────────────────

    def _draw(self, color: str) -> None:
        self.delete("all")
        w = int(self["width"]); h = int(self["height"]); r = self._radius
        self._draw_rounded_rect(0, 0, w-1, h-1, r, fill=color, outline="")
        self.create_text(w // 2, h // 2, text=self._text,
                         fill=self._fg, font=self._font, anchor="center")

    def _draw_rounded_rect(self, x1, y1, x2, y2, r, **kw) -> None:
        self.create_arc(x1,      y1,      x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kw)
        self.create_arc(x2-2*r,  y1,      x2,     y1+2*r, start=0,   extent=90,  style="pieslice", **kw)
        self.create_arc(x2-2*r,  y2-2*r,  x2,     y2,     start=270, extent=90,  style="pieslice", **kw)
        self.create_arc(x1,      y2-2*r,  x1+2*r, y2,     start=180, extent=90,  style="pieslice", **kw)
        self.create_rectangle(x1+r, y1, x2-r, y2, **kw)
        self.create_rectangle(x1, y1+r, x2, y2-r, **kw)

    # ── Animation ─────────────────────────────────────────────────────────────

    def _animate(self, from_c: str, to_c: str, steps: int = 8, step: int = 0) -> None:
        if step > steps:
            self._current_bg = to_c
            return
        self._draw(self._lerp_color(from_c, to_c, step / steps))
        self.after(12, lambda: self._animate(from_c, to_c, steps, step + 1))

    def _on_enter(self, _=None) -> None:
        self._animate(self._current_bg, self._bg_hover)

    def _on_leave(self, _=None) -> None:
        self._animate(self._current_bg, self._bg)

    def _on_press(self, _=None) -> None:
        self._draw(self._bg_press)
        self._current_bg = self._bg_press

    def _on_release(self, _=None) -> None:
        self._animate(self._current_bg, self._bg_hover)
        if self._command:
            self._command()

    # ── Public API ────────────────────────────────────────────────────────────

    def configure_text(self, text: str) -> None:
        """Zmienia etykietę przycisku bez resetu stanu animacji."""
        self._text = text
        self._draw(self._current_bg)

    def set_state(self, state: str, command=None) -> None:
        """Włącza lub wyłącza przycisk (``'normal'`` / ``'disabled'``)."""
        if state == "disabled":
            self._command    = None
            self._draw("#2D4A66")
            self._current_bg = "#2D4A66"
        else:
            if command is not None:
                self._command = command
            self._draw(self._bg)
            self._current_bg = self._bg


# ─── ModernCheckbox ───────────────────────────────────────────────────────────

class ModernCheckbox(tk.Frame):
    """Ciemny, animowany checkbox z etykietą tekstową."""

    def __init__(
        self,
        parent,
        text: str = "",
        variable: Optional[tk.BooleanVar] = None,
        fg: str = C_TEXT,
        font=FONT_BODY,
        wraplength: int = 0,
        **kw,
    ) -> None:
        super().__init__(parent, bg=parent["bg"], **kw)
        self._var  = variable if variable is not None else tk.BooleanVar(value=False)
        self._fg   = fg
        self._font = font

        self._canvas = tk.Canvas(
            self, width=20, height=20,
            bg=self["bg"], bd=0, highlightthickness=0,
        )
        self._canvas.pack(side="left", padx=(0, 8))

        self._label = tk.Label(
            self, text=text, bg=self["bg"],
            fg=fg, font=font, cursor="hand2",
            justify="left", anchor="w",
            **(dict(wraplength=wraplength) if wraplength else {}),
        )
        self._label.pack(side="left", fill="x", expand=True)

        if wraplength:
            self._cur_wl = wraplength
            self._label.bind("<Configure>", self._on_label_configure)

        self._draw()
        self._canvas.bind("<Button-1>", self._toggle)
        self._label.bind("<Button-1>",  self._toggle)
        self._var.trace_add("write", lambda *_: self._draw())

    def _draw(self) -> None:
        self._canvas.delete("all")
        r = 4
        if self._var.get():
            self._canvas.create_rounded_bg(1, 1, 19, 19, r, C_ACCENT)
            self._canvas.create_line(5, 10, 9, 14, fill=C_WHITE, width=2, capstyle="round")
            self._canvas.create_line(9, 14, 15,  6, fill=C_WHITE, width=2, capstyle="round")
        else:
            self._canvas.create_rounded_bg(1, 1, 19, 19, r, C_SURFACE2, border=C_BORDER)

    def _toggle(self, _=None) -> None:
        self._var.set(not self._var.get())
        self._animate_check()

    def _animate_check(self, step: int = 0, steps: int = 4) -> None:
        if step > steps:
            return
        self._draw()
        self.after(20, lambda: self._animate_check(step + 1, steps))

    def _on_label_configure(self, event) -> None:
        new_wl = max(1, event.width - 2)
        if self._cur_wl != new_wl:
            self._cur_wl = new_wl
            self._label.configure(wraplength=new_wl)

    @property
    def var(self) -> tk.BooleanVar:
        return self._var


# ─── ProgressBar ─────────────────────────────────────────────────────────────

class ProgressBar(tk.Canvas):
    """Animowany poziomy pasek postępu."""

    def __init__(self, parent, height: int = 6, **kw) -> None:
        super().__init__(
            parent, height=height,
            bg=parent["bg"], bd=0, highlightthickness=0, **kw,
        )
        self._h   = height
        self._pct = 0.0
        self.bind("<Configure>", lambda _: self._draw())

    def _draw(self) -> None:
        self.delete("all")
        w = self.winfo_width()
        if w < 2:
            return
        self.create_rectangle(0, 0, w, self._h, fill=C_SURFACE2, outline="")
        filled = int(w * self._pct)
        if filled > 0:
            self.create_rectangle(0, 0, filled, self._h, fill=C_ACCENT, outline="")

    def set_progress(self, pct: float) -> None:
        """Ustawia postęp od 0.0 do 1.0."""
        self._pct = max(0.0, min(1.0, pct))
        self._draw()

    def animate_to(self, target: float, steps: int = 20, step: int = 0) -> None:
        """Płynnie animuje pasek do wartości *target*."""
        start = self._pct
        if step > steps:
            self.set_progress(target)
            return
        self.set_progress(start + (target - start) * step / steps)
        self.after(15, lambda: self.animate_to(target, steps, step + 1))


# ─── PulsingDot ──────────────────────────────────────────────────────────────

class PulsingDot(tk.Canvas):
    """Mały pulsujący wskaźnik aktywności."""

    def __init__(self, parent, size: int = 10, **kw) -> None:
        super().__init__(
            parent, width=size, height=size,
            bg=parent["bg"], bd=0, highlightthickness=0, **kw,
        )
        self._size   = size
        self._active = False
        self._phase  = 0.0
        self._draw(C_SURFACE2)

    def _draw(self, color: str) -> None:
        self.delete("all")
        s = self._size
        self.create_oval(1, 1, s - 1, s - 1, fill=color, outline="")

    def start(self) -> None:
        self._active = True
        self._pulse()

    def stop(self) -> None:
        self._active = False
        self._draw(C_GREEN)

    def _pulse(self) -> None:
        if not self._active:
            return
        self._phase = (self._phase + 0.15) % (2 * math.pi)
        t = (math.sin(self._phase) + 1) / 2
        r = int(30 * (1 - t))
        g = int(136 + (200 - 136) * t)
        b = int(229 + (255 - 229) * t)
        self._draw(f"#{r:02x}{g:02x}{b:02x}")
        self.after(40, self._pulse)
