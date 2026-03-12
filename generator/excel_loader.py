# -*- coding: utf-8 -*-
"""
Wczytywanie danych osobowych z arkusza Excel.

Tryb mapowania komórek:
    Użytkownik podaje początkową komórkę (np. „B2") dla każdego pola.
    Dane są czytane w dół kolumny aż do pierwszej pustej komórki.
"""
import re
from typing import Dict, List, Tuple

from openpyxl.utils import column_index_from_string


def _parse_cell_ref(ref: str) -> Tuple[int, int]:
    """Parsuje referencję komórki (np. 'B2') na (kolumna, wiersz) jako int.

    Zwraca krotkę (col_index, row_index) — oba 1-based.
    Rzuca ValueError jeśli format jest nieprawidłowy.
    """
    ref = ref.strip().upper()
    m = re.fullmatch(r"([A-Z]+)(\d+)", ref)
    if not m:
        raise ValueError(f"Nieprawidłowy format komórki: {ref!r}")
    col = column_index_from_string(m.group(1))
    row = int(m.group(2))
    if row < 1:
        raise ValueError(f"Numer wiersza musi być >= 1: {ref!r}")
    return col, row


def _read_column_down(ws, col: int, start_row: int) -> List[str]:
    """Czyta wartości z kolumny *col* od wiersza *start_row* w dół.

    Kończy na pierwszej pustej komórce.
    """
    values = []  # type: List[str]
    row = start_row
    while True:
        cell = ws.cell(row=row, column=col)
        if cell.value is None or str(cell.value).strip() == "":
            break
        values.append(str(cell.value).strip())
        row += 1
    return values


# Nazwy pól i ich kolejność (klucze słownika person)
FIELD_KEYS = [
    "imie", "nazwisko", "pesel",
    "ulica", "nr_domu", "nr_lokalu",
    "kod_pocztowy", "miejscowosc", "telefon",
    "wojewodztwo", "powiat", "gmina", "poczta",
]


def load_sheet_data_mapped(
    wb, sheet_name: str, cell_mapping: Dict[str, str],
) -> List[dict]:
    """Wczytuje dane z arkusza na podstawie mapowania komórek.

    ``cell_mapping`` to słownik ``{nazwa_pola: ref_komórki}``,
    np. ``{"imie": "B2", "nazwisko": "C2", "pesel": "E2"}``.
    Pola bez mapowania zostają puste.

    Liczba rekordów = najdłuższa kolumna z podanych mapowań.
    """
    ws = wb[sheet_name]

    # Wczytaj kolumny dla pól, które mają przypisaną komórkę
    columns = {}  # type: Dict[str, List[str]]
    for field, ref in cell_mapping.items():
        if not ref or not ref.strip():
            continue
        col, start_row = _parse_cell_ref(ref)
        columns[field] = _read_column_down(ws, col, start_row)

    if not columns:
        return []

    n = max(len(v) for v in columns.values())
    if n == 0:
        return []

    rows = []  # type: List[dict]
    for i in range(n):
        person = {}  # type: Dict[str, str]
        for key in FIELD_KEYS:
            vals = columns.get(key, [])
            person[key] = vals[i] if i < len(vals) else ""
        rows.append(person)

    return rows
