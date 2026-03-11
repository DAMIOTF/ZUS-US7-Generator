# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec — Generator ZUS US-7
# Tryb: --onedir  (folder z exe + DLL-ami, lżejszy dla RAM niż --onefile)
#
# WAŻNE: ścieżka projektu zawiera spację ("ZUS US7"), przez co PyInstaller 6.x
# nie może zapisać plików do katalogu build/dist.
# Zawsze buduj z --workpath i --distpath wskazującymi na ścieżkę BEZ spacji:
#
#   py -3.8 -m PyInstaller zus_us7.spec --clean --workpath C:\Temp\zus_build --distpath C:\Temp\zus_dist
#
# Gotowy folder dist\GeneratorZUS_US7 przenieś ręcznie do projektu.

from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

# --- PyMuPDF 1.24+ używa pakietu "pymupdf" (fitz jest tylko aliasem) ----------
pymupdf_datas, pymupdf_bins, pymupdf_hidden = collect_all("pymupdf")
fitz_datas,    fitz_bins,    fitz_hidden    = collect_all("fitz")

# --- openpyxl: dane (szablony XML/xlsl) + ukryte importy ----------------------
openpyxl_datas  = collect_data_files("openpyxl")
openpyxl_hidden = collect_submodules("openpyxl")

datas = (
    pymupdf_datas
    + fitz_datas
    + openpyxl_datas
    + [
        ("szablon.pdf", "."),   # szablon ZUS US-7
        ("ICO.ico",     "."),   # ikona aplikacji
    ]
)

binaries = pymupdf_bins + fitz_bins

hidden = pymupdf_hidden + fitz_hidden + openpyxl_hidden

# --- Moduły do wykluczenia (zmniejszenie rozmiaru / RAM) ----------------------
excludes = [
    # Naukowe / analityczne — nieużywane
    "numpy", "pandas", "scipy", "matplotlib", "sklearn",
    "sympy", "statsmodels", "seaborn", "plotly",
    # Jupyter / IPython
    "IPython", "jupyter", "notebook", "nbformat", "nbconvert",
    "ipykernel", "ipywidgets",
    # Pillow — nieużywane w kodzie
    "PIL",
    # Testowe / diagnostyczne
    "unittest", "doctest", "pydoc",
    "pytest", "_pytest",
    # Sieciowe — nieużywane
    "urllib3", "requests", "http.server", "xmlrpc",
    "ftplib", "smtplib", "imaplib", "poplib", "telnetlib",
    "socketserver",
    # Inne zbędne
    "tkinter.test", "lib2to3",
    "curses", "readline",
    "sqlite3", "_sqlite3",
    "crypt",
]

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=True,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],                      # puste = onedir (NIE onefile)
    exclude_binaries=True,   # biblioteki DLL zostają jako osobne pliki
    name="GeneratorZUS_US7",
    debug=False,
    strip=False,
    upx=False,               # UPX wyłączony — wolny start na słabym PC
    console=False,           # brak okna konsoli
    icon="ICO.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="GeneratorZUS_US7",
)

