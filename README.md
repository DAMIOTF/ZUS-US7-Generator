# Generator ZUS US-7

Profesjonalna aplikacja do **masowego generowania** wypełnionych formularzy ZUS US-7 (wniosek o zaświadczenie / informację) na podstawie danych z pliku Excel.

## Funkcje

- Wypełnia szablon PDF (XFA) danymi osobowymi z arkusza Excel
- Obsługuje wszystkie 6 checkboxów pkt 3 formularza (w tym OFE)
- Ciemny, nowoczesny interfejs GUI (tkinter)
- Animowane przyciski i wskaźnik postępu
- Wielowątkowe generowanie — GUI nie blokuje się podczas pracy
- Dziennik operacji z kolorowymi statusami
- Gotowy plik `.exe` — bez instalacji Pythona

## Szybki start (EXE)

Pobierz `Generator_ZUS_US7.exe` z zakładki [Releases](https://github.com/DAMIOTF/ZUS-US7-Generator/releases) i uruchom — szablon PDF jest wbudowany, nie potrzebujesz nic więcej.

## Uruchomienie ze źródeł

### Wymagania

```
Python 3.10+
```

Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

### GUI (zalecane)

```bash
python main.py
```

### CLI (wiersz poleceń)

Uzupełnij stałe w `app.py` (`EXCEL_FILE`, `DATE`, `DEFAULT_OPTIONS`), następnie:

```bash
python app.py
```

## Kompilacja do EXE

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "Generator_ZUS_US7" --icon "ICO.ico" --add-data "szablon.pdf;." --add-data "ICO.ico;." main.py
```

Wynikowy plik: `dist/Generator_ZUS_US7.exe`

## Struktura projektu

```
├── main.py               # punkt startowy GUI
├── app.py                # interfejs CLI
├── gui.py                # alias dla main.py (zgodność wsteczna)
├── szablon.pdf           # szablon formularza ZUS US-7 (XFA)
├── ICO.ico               # ikona aplikacji
├── requirements.txt
├── .gitignore
└── generator/
    ├── __init__.py       # publiczne API pakietu
    ├── constants.py      # kolory, czcionki, ścieżki
    ├── pdf_engine.py     # silnik wypełniania PDF (XFA)
    ├── excel_loader.py   # wczytywanie danych z Excel
    ├── widgets.py        # niestandardowe widgety tkinter
    ├── app_window.py     # główne okno aplikacji (init, layout)
    ├── sections.py       # budowa sekcji formularza (mixin)
    └── handlers.py       # logika zdarzeń i generowanie PDF (mixin)
```

## Autor

**Damian Marciniak** · [github.com/DAMIOTF](https://github.com/DAMIOTF)
