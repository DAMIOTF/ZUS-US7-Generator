# Generator ZUS US-7

Profesjonalna aplikacja do **masowego generowania** dokumentów ZUS na podstawie danych z pliku Excel.

## Obsługiwane dokumenty

| Dokument | Format | Opis |
|----------|--------|------|
| **ZUS US-7** | PDF | Wniosek o wydanie zaświadczenia / udostępnienie danych |
| **Załącznik nr 2** | DOCX | Oświadczenie uczestnika projektu |
| **Upoważnienie ZUS** | DOCX | Upoważnienie do odbioru zaświadczenia |
| **Załącznik nr 8** | PDF | Oświadczenie dotyczące miejsca zamieszkania |

## Funkcje

- Generowanie **4 typów dokumentów** — wybierasz które checkboxem
- Wypełnia szablony PDF (XFA) i DOCX danymi osobowymi z arkusza Excel
- **Elastyczne mapowanie komórek** — sam decydujesz, która kolumna Excel odpowiada jakiemu polu (np. B2 → Imię, C2 → Nazwisko)
- Dane czytane automatycznie w dół od podanej komórki aż do pierwszej pustej
- Automatyczna obsługa wsi — gdy poczta ≠ miejscowość, nazwa wsi trafia do pola ulicy
- Wyniki grupowane w **foldery per osoba** (`wyniki/Imię Nazwisko/`)
- Ciemny, nowoczesny interfejs GUI (tkinter)
- Wielowątkowe generowanie — GUI nie blokuje się podczas pracy
- Gotowy folder z `.exe` — bez instalacji Pythona
- Architektura przygotowana pod rozbudowę o kolejne typy dokumentów

## Jak to działa

1. Zaznacz typy dokumentów do wygenerowania (checkboxy na górze)
2. Wybierz plik Excel i arkusz
3. W sekcji **„Mapowanie komórek Excel"** wpisz komórkę startową dla każdego pola (np. `B2` dla imion, `C2` dla nazwisk, `E2` dla PESEL-i)
4. Ustaw datę wniosku, opcje formularza i folder wynikowy
5. Kliknij **Generuj dokumenty** — aplikacja utworzy folder dla każdej osoby z wybranymi dokumentami

> Pola bez przypisanej komórki zostaną puste. Jeśli nie podasz żadnego mapowania, generowanie się nie uruchomi.

## Mapowanie pól Excel

| Pole | Używane przez | Opis |
|------|---------------|------|
| Imię | wszystkie | Imię osoby |
| Nazwisko | wszystkie | Nazwisko osoby |
| PESEL | wszystkie | Numer PESEL |
| Ulica | US-7, Załącznik 2, Upoważnienie | Nazwa ulicy (lub wsi jeśli poczta ≠ miejscowość) |
| Nr domu | wszystkie | Numer domu |
| Nr lokalu | wszystkie | Numer lokalu |
| Kod pocztowy | wszystkie | Kod pocztowy |
| Miejscowość | wszystkie | Nazwa miejscowości |
| Telefon | US-7, Załącznik 2 | Numer telefonu |
| Województwo | Załącznik 8 | Województwo |
| Powiat | Załącznik 8 | Powiat |
| Gmina | Załącznik 8 | Gmina |
| Poczta | US-7, Załącznik 2, Upoważnienie, Załącznik 8 | Poczta (miasto nadrzędne dla wsi) |

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
├── main.py                       # punkt startowy GUI
├── app.py                        # interfejs CLI
├── gui.py                        # alias dla main.py (zgodność wsteczna)
├── zus_us7.spec                  # konfiguracja PyInstaller (onedir)
├── szablon.pdf                   # szablon ZUS US-7 (XFA)
├── UPOWAŻNIENIE ZUS.docx         # szablon Upoważnienia ZUS
├── Zalacznik NR 8.pdf            # szablon Załącznika nr 8
├── ICO.ico                       # ikona aplikacji
├── requirements.txt
├── .gitignore
├── zalacznik2/
│   └── szablon_pusty.docx        # szablon Załącznika nr 2
└── generator/
    ├── __init__.py               # publiczne API + rejestracja dokumentów
    ├── constants.py              # kolory, czcionki, ścieżki
    ├── doc_types.py              # rejestr typów dokumentów
    ├── pdf_engine.py             # silnik ZUS US-7 (PDF XFA)
    ├── zalacznik2_engine.py      # silnik Załącznika nr 2 (DOCX)
    ├── upowaznienie_engine.py    # silnik Upoważnienia ZUS (DOCX)
    ├── zalacznik8_engine.py      # silnik Załącznika nr 8 (PDF overlay)
    ├── excel_loader.py           # mapowanie komórek i wczytywanie danych
    ├── widgets.py                # niestandardowe widgety tkinter
    ├── app_window.py             # główne okno aplikacji (init, layout)
    ├── sections.py               # budowa sekcji formularza (mixin)
    └── handlers.py               # logika zdarzeń i generowanie (mixin)
```


## Autor

**Damian Marciniak** · [github.com/DAMIOTF](https://github.com/DAMIOTF)
**Kontakt:** · kontakt@dmtf.ovh




**Wszelkie prawa zastrzeżone © 2026 Damian Marciniak.**

Program jest objęty restrykcyjną licencją — zabrania się rozpowszechniania, sprzedaży, modyfikacji w celu redystrybucji oraz publikowania kodu źródłowego bez pisemnej zgody autora. Szczegóły w pliku [LICENSE](LICENSE).

