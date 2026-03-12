# -*- coding: utf-8 -*-
"""
Silnik generowania Załącznika nr 8 — oświadczenie o miejscu zamieszkania (PDF).

Szablon jest nieedytowalnym PDF-em, więc tekst jest nakładany bezpośrednio
na stronę za pomocą PyMuPDF (fitz).

Publiczne API:
    fill_zalacznik8(person, date_str, options) -> bytes
"""
import os

import fitz  # PyMuPDF

from .constants import resource_path

TEMPLATE_PDF = resource_path("Zalacznik NR 8.pdf")

# ── Stałe pozycji na stronie (ustalone z analizy szablonu) ────────────────────
_VAL_X = 212.0
_FONT_SIZE = 11.0

# Czcionka Arial z systemu Windows — obsługuje polskie znaki (ąćęłńóśźż)
_ARIAL_TTF = os.path.join(os.environ.get("WINDIR", r"C:\Windows"),
                          "Fonts", "arial.ttf")


def fill_zalacznik8(person: dict, date_str: str, options: dict) -> bytes:
    """Wypełnia szablon Załącznika nr 8 i zwraca bajty gotowego pliku PDF."""
    imie = person.get("imie", "")
    nazwisko = person.get("nazwisko", "")
    pesel = person.get("pesel", "")

    if pesel.isdigit() and len(pesel) < 11:
        pesel = pesel.zfill(11)

    doc = fitz.open(TEMPLATE_PDF)
    page = doc[0]

    # Rejestracja czcionki Arial (TrueType) z polskimi znakami
    page.insert_font(fontname="arial", fontfile=_ARIAL_TTF)

    color = (0, 0, 0)  # czarny

    def _put(pos, text):
        page.insert_text(
            pos, text,
            fontname="arial", fontfile=_ARIAL_TTF,
            fontsize=_FONT_SIZE, color=color,
        )

    # ── Imię i nazwisko (linia „Ja niżej podpisany/a", y ≈ 145.6) ────────────
    _put((240, 145.6), f"{imie} {nazwisko}")

    # ── PESEL (linia „Numer PESEL)", y ≈ 166.3) ──────────────────────────────
    _put((160, 166.3), pesel)

    # ── Tabela adresowa ───────────────────────────────────────────────────────
    # Wpisujemy dosłownie miejscowość z Excela, ulica z Excela (bez logiki wsi)
    addr_fields = [
        (291.0, person.get("wojewodztwo", "")),
        (312.2, person.get("powiat", "")),
        (333.4, person.get("gmina", "")),
        (354.6, person.get("miejscowosc", "")),
        (375.8, person.get("ulica", "")),
        (397.0, _nr_domu_mieszkania(person)),
        (418.2, person.get("kod_pocztowy", "")),
        (439.4, person.get("poczta", "")),
    ]

    for y, value in addr_fields:
        val = str(value).strip()
        if val:
            _put((_VAL_X, y), val)

    out = doc.tobytes(garbage=4, deflate=True)
    doc.close()
    return out


def _nr_domu_mieszkania(person: dict) -> str:
    """Łączy nr domu i nr lokalu w jeden ciąg."""
    nr_domu = person.get("nr_domu", "").strip()
    nr_lokalu = person.get("nr_lokalu", "").strip()
    if nr_domu and nr_lokalu:
        return f"{nr_domu}/{nr_lokalu}"
    return nr_domu or nr_lokalu
