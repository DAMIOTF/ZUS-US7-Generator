"""
Wczytywanie danych osobowych z arkusza Excel.

Oczekiwany układ kolumn (od kolumny A):
    lp | imię | nazwisko | data_ur | PESEL | powiat | gmina |
    miejscowość | kod_pocztowy | ulica | nr_domu | nr_lokalu |
    poczta | telefon | szkoła
"""
from __future__ import annotations


def load_sheet_data(wb, sheet_name: str) -> list[dict]:
    """Zwraca listę słowników z danymi osobowymi z arkusza *sheet_name*.

    Obsługuje regułę wiejską: gdy brak ulicy, jako ulicę przyjmuje
    się nazwę miejscowości, a jako miasto — pocztę.
    """
    ws = wb[sheet_name]
    rows: list[dict] = []

    for row in ws.iter_rows(min_row=2, values_only=True):
        if len(row) < 15:
            continue
        (lp, imie, nazwisko, data_ur, pesel, powiat, gmina,
         miejscowosc, kod_poczt, ulica, nr_domu, nr_lokalu,
         poczta, telefon, szkola) = row[:15]

        if not pesel:
            continue

        if not ulica:
            ulica_val  = str(miejscowosc).strip() if miejscowosc else ""
            miasto_val = str(poczta).strip()       if poczta      else ""
        else:
            ulica_val  = str(ulica).strip()
            miasto_val = str(miejscowosc).strip()  if miejscowosc else ""

        rows.append({
            "imie":         str(imie).strip()       if imie       else "",
            "nazwisko":     str(nazwisko).strip()   if nazwisko   else "",
            "pesel":        str(pesel).strip()       if pesel      else "",
            "ulica":        ulica_val,
            "nr_domu":      str(nr_domu).strip()    if nr_domu    else "",
            "nr_lokalu":    str(nr_lokalu).strip()  if nr_lokalu  else "",
            "kod_pocztowy": str(kod_poczt).strip()  if kod_poczt  else "",
            "miejscowosc":  miasto_val,
            "telefon":      str(telefon).strip()    if telefon    else "",
        })

    return rows
