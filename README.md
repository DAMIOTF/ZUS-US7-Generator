# Generator ZUS US-7

Profesjonalna aplikacja do **masowego generowania** wypełnionych formularzy ZUS US-7 na podstawie danych z pliku Excel.

## Funkcje

- Wypełnia szablon PDF (XFA) danymi osobowymi z arkusza Excel
- **Elastyczne mapowanie komórek** — sam decydujesz, która kolumna Excel odpowiada jakiemu polu (np. B2 → Imię, C2 → Nazwisko)
- Dane czytane automatycznie w dół od podanej komórki aż do pierwszej pustej
- Ciemny, nowoczesny interfejs GUI (tkinter)
- Wielowątkowe generowanie — GUI nie blokuje się podczas pracy
- Gotowy folder z `.exe` — bez instalacji Pythona
<img width="777" height="222" alt="image" src="https://github.com/user-attachments/assets/f4a53cf6-ce58-4446-bd68-a1998fec31d6" />


## Jak to działa

1. Wybierz plik Excel i arkusz
2. W sekcji **„Mapowanie komórek Excel"** wpisz komórkę startową dla każdego pola (np. `B2` dla imion, `C2` dla nazwisk, `E2` dla PESEL-i)
3. Ustaw datę wniosku, opcje formularza i folder wynikowy
4. Kliknij **Generuj PDF** — aplikacja utworzy osobny plik PDF dla każdego wiersza danych

<img width="783" height="568" alt="image" src="https://github.com/user-attachments/assets/694d7da4-44c0-4bbe-971e-df1fd71a961c" />


> Pola bez przypisanej komórki zostaną puste w PDF. Jeśli nie podasz żadnego mapowania, generowanie się nie uruchomi.

<img width="791" height="494" alt="image" src="https://github.com/user-attachments/assets/c4c86c2e-0a06-4487-b754-1749b3420c83" />


## Szybki start (EXE)

Pobierz folder `GeneratorZUS_US7` z zakładki [Releases](https://github.com/DAMIOTF/ZUS-US7-Generator/releases), rozpakuj i uruchom `GeneratorZUS_US7.exe` — szablon PDF jest wbudowany, nie potrzebujesz nic więcej.

## Uruchomienie ze źródeł

### Wymagania

```
Python 3.8+
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

Uzupełnij stałe w `app.py` (`EXCEL_FILE`, `DATE`, `DEFAULT_CELL_MAPPING`, `DEFAULT_OPTIONS`), następnie:

```bash
python app.py
```

## Kompilacja do EXE

Projekt korzysta z trybu `--onedir` (folder z exe + DLL-ami) — lżejszy dla RAM niż `--onefile`:

```bash
pip install pyinstaller
py -3.8 -m PyInstaller zus_us7.spec --clean --workpath C:\Temp\zus_build --distpath C:\Temp\zus_dist
```

Wynikowy folder: `C:\Temp\zus_dist\GeneratorZUS_US7\`

> **Uwaga:** ścieżka projektu zawiera spację (`ZUS US7`), dlatego build/dist muszą wskazywać na ścieżkę bez spacji.

## Struktura projektu

```
├── main.py               # punkt startowy GUI
├── app.py                # interfejs CLI
├── gui.py                # alias dla main.py (zgodność wsteczna)
├── zus_us7.spec          # konfiguracja PyInstaller (onedir)
├── szablon.pdf           # szablon formularza ZUS US-7 (XFA)
├── ICO.ico               # ikona aplikacji
├── requirements.txt
├── .gitignore
└── generator/
    ├── __init__.py       # publiczne API pakietu
    ├── constants.py      # kolory, czcionki, ścieżki
    ├── pdf_engine.py     # silnik wypełniania PDF (XFA)
    ├── excel_loader.py   # mapowanie komórek i wczytywanie danych
    ├── widgets.py        # niestandardowe widgety tkinter
    ├── app_window.py     # główne okno aplikacji (init, layout)
    ├── sections.py       # budowa sekcji formularza (mixin)
    └── handlers.py       # logika zdarzeń i generowanie PDF (mixin)
```


## Autor

**Damian Marciniak** · [github.com/DAMIOTF](https://github.com/DAMIOTF)
**Kontakt:** · kontakt@dmtf.ovh




**Wszelkie prawa zastrzeżone © 2026 Damian Marciniak.**

Program jest objęty restrykcyjną licencją — zabrania się rozpowszechniania, sprzedaży, modyfikacji w celu redystrybucji oraz publikowania kodu źródłowego bez pisemnej zgody autora. Szczegóły w pliku [LICENSE](LICENSE).

