"""
app.py - interfejs wiersza polecen (CLI) generatora ZUS US-7.

Wymaga pliku tabela.xlsx w katalogu roboczym.
Wynikowe pliki zapisuje do folderu wyniki/ (podfoldery per osoba).

Uzycie:
    python app.py
"""
import os
import openpyxl

from generator.excel_loader import load_sheet_data_mapped
from generator import doc_types  # rejestracja typów następuje przy imporcie

EXCEL_FILE = "tabela.xlsx"
SHEET_NAME = None          # None = pierwszy arkusz
OUTPUT_DIR = "wyniki"
DATE       = "10.03.2026"

# Które dokumenty generować (id z rejestru doc_types)
SELECTED_DOCS = ["us7", "zalacznik2"]

# Mapowanie komórek: pole -> komórka startowa (czyta w dół)
DEFAULT_CELL_MAPPING = {
    "imie":         "B2",
    "nazwisko":     "C2",
    "pesel":        "E2",
    "ulica":        "J2",
    "nr_domu":      "K2",
    "nr_lokalu":    "L2",
    "kod_pocztowy": "I2",
    "miejscowosc":  "H2",
    "telefon":      "N2",
}

DEFAULT_OPTIONS = {
    "radio_type":        "1",
    "cb_ubezpieczenia":  True,
    "cb_przerwy":        False,
    "cb_podstawy":       False,
    "cb_warunki":        False,
    "cb_ofe_czlonek":    False,
    "cb_ofe_skladki":    False,
    "delivery_placowka": True,
    "delivery_poczta":   False,
    "delivery_pue":      False,
    "uzasadnienie": (
        "W zwiazku z ubieganiem sie o wsparcie w projekcie "
        "wspolfinansowanym ze srodkow EFS"
    ),
}


def main() -> None:
    wb         = openpyxl.load_workbook(EXCEL_FILE, read_only=False, data_only=True)
    sheet_name = SHEET_NAME or wb.sheetnames[0]
    people     = load_sheet_data_mapped(wb, sheet_name, DEFAULT_CELL_MAPPING)
    wb.close()

    # Zbierz wybrane typy dokumentów
    selected = [dt for dt in doc_types.get_all() if dt["id"] in SELECTED_DOCS]
    doc_names = ", ".join(d["label"] for d in selected)

    print(f"Znaleziono {len(people)} rekordow w arkuszu '{sheet_name}'.")
    print(f"Dokumenty: {doc_names}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ok = err = 0
    for person in people:
        first = person["imie"].split()[0] if person["imie"] else "brak"
        folder_name = f"{first} {person['nazwisko']}"
        person_dir = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(person_dir, exist_ok=True)

        for dt in selected:
            try:
                fname = dt["filename_tpl"].format(
                    imie=first,
                    nazwisko=person["nazwisko"],
                ) + dt["extension"]
                out_path = os.path.join(person_dir, fname)
                data = dt["generate"](person, DATE, DEFAULT_OPTIONS)
                with open(out_path, "wb") as fh:
                    fh.write(data)
                ok += 1
                print(f"  [OK] {folder_name}/{fname}")
            except Exception as exc:
                err += 1
                print(f"  [ERR] {person.get('imie','')} {person.get('nazwisko','')} [{dt['label']}]: {exc}")

    print(f"\nGotowe  {ok} wygenerowanych, {err} bledow.")
    print(f"Folder: {os.path.abspath(OUTPUT_DIR)}")


if __name__ == "__main__":
    main()
