"""
app.py - interfejs wiersza polecen (CLI) generatora ZUS US-7.

Wymaga pliku tabela.xlsx w katalogu roboczym.
Wynikowe pliki PDF zapisuje do folderu wyniki/.

Uzycie:
    python app.py
"""
import os
import openpyxl

from generator.pdf_engine import fill_pdf
from generator.excel_loader import load_sheet_data

EXCEL_FILE = "tabela.xlsx"
SHEET_NAME = None          # None = pierwszy arkusz
OUTPUT_DIR = "wyniki"
DATE       = "10.03.2026"

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
    wb         = openpyxl.load_workbook(EXCEL_FILE, read_only=True, data_only=True)
    sheet_name = SHEET_NAME or wb.sheetnames[0]
    people     = load_sheet_data(wb, sheet_name)
    wb.close()

    print(f"Znaleziono {len(people)} rekordow w arkuszu '{sheet_name}'.")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ok = err = 0
    for person in people:
        try:
            first    = person["imie"].split()[0] if person["imie"] else "brak"
            filename = f"ZUS {first} {person['nazwisko']}.pdf"
            out_path = os.path.join(OUTPUT_DIR, filename)
            with open(out_path, "wb") as fh:
                fh.write(fill_pdf(person, DATE, DEFAULT_OPTIONS))
            ok += 1
            print(f"  [OK] {filename}")
        except Exception as exc:
            err += 1
            print(f"  [ERR] {person.get('imie','')} {person.get('nazwisko','')}: {exc}")

    print(f"\nGotowe  {ok} wygenerowanych, {err} bledow.")
    print(f"Folder: {os.path.abspath(OUTPUT_DIR)}")


if __name__ == "__main__":
    main()
