# Generator ZUS US-7

Profesjonalna aplikacja do **masowego generowania** wypełnionych formularzy ZUS US-7 na podstawie danych z pliku Excel.

## Funkcje

- Wypełnia szablon PDF (XFA) danymi osobowymi z arkusza Excel
- Ciemny, nowoczesny interfejs GUI (tkinter)
- Wielowątkowe generowanie — GUI nie blokuje się podczas pracy
- Gotowy plik `.exe` — bez instalacji Pythona

<img width="874" height="974" alt="obraz" src="https://github.com/user-attachments/assets/28b47309-9e6b-48f4-94eb-dac4e1e48e66" />

## struktura pliku .xlsx

| Lp | Imię  | Nazwisko   | Data urodzenia | PESEL       | Powiat   | Gmina               | Miejscowość | Kod pocztowy | Ulica         | Nr domu | Nr lokalu | Poczta              | Telefon   |
| -- | ----- | ---------- | -------------- | ----------- | -------- | ------------------- | ----------- | ------------ | ------------- | ------- | --------- | ------------------- | --------- |
| 1  | Jan   | Kowalski   | 1990-05-15     | 90051512345 | Warszawa | Warszawa            | Warszawa    | 00-001       | Marszałkowska | 10      | 5         | Warszawa            | 500100200 |
| 2  | Anna  | Nowak      | 1985-11-20     | 85112067890 | bialski  | Międzyrzec Podlaski | Rogoźnica   | 21-560       |               | 42      |           | Międzyrzec Podlaski | 600300400 |
| 3  | Piotr | Wiśniewski |                | 95030198765 |          |                     | Kraków      | 30-001       | Długa         | 5       |           | Kraków              |           |


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
