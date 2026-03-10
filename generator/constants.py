"""
Stałe aplikacji: kolory, czcionki, ścieżki, URL-e.
"""
from __future__ import annotations

import os
import sys


def resource_path(name: str) -> str:
    """Zwraca ścieżkę do pliku zasobu.

    Działa zarówno przy uruchomieniu ze źródeł, jak i po spakowaniu
    przez PyInstaller (sys._MEIPASS).
    """
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS  # type: ignore[attr-defined]
    else:
        # generator/ leży jeden poziom niżej niż katalog projektu
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


TEMPLATE_PDF  = resource_path("szablon.pdf")
DATASETS_XREF = 63
GITHUB_URL    = "https://github.com/DAMIOTF"

# ─── Paleta kolorów ───────────────────────────────────────────────────────────
C_BG        = "#0D1B2A"   # granatowy — główne tło
C_SURFACE   = "#1A2B3C"   # nieco jaśniejsze karty
C_SURFACE2  = "#223344"   # drugorzędne powierzchnie
C_ACCENT    = "#1E88E5"   # niebieski akcent
C_ACCENT2   = "#42A5F5"   # jaśniejszy niebieski (hover)
C_ACCENT_DK = "#1565C0"   # ciemniejszy niebieski (wciśnięty)
C_GREEN     = "#00C853"   # sukces
C_RED       = "#FF5252"   # błąd
C_YELLOW    = "#FFD740"   # ostrzeżenie
C_TEXT      = "#E8EDF2"   # tekst główny
C_SUBTEXT   = "#7B9BB8"   # tekst drugorzędny
C_BORDER    = "#2D4A66"   # subtelna ramka
C_WHITE     = "#FFFFFF"
C_SELECT    = "#2196F3"   # podświetlenie zaznaczenia

# ─── Czcionki ────────────────────────────────────────────────────────────────
FONT_H1   = ("Segoe UI", 18, "bold")
FONT_H2   = ("Segoe UI", 13, "bold")
FONT_H3   = ("Segoe UI", 10, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SM   = ("Segoe UI",  9)
FONT_LOG  = ("Consolas",  9)
