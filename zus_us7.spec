# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec — Generator ZUS US-7
# Tryb: --onedir  (folder z exe + DLL-ami, lżejszy dla RAM niż --onefile)
#
# Budowanie:
#   python -m PyInstaller zus_us7.spec --clean
#
# Wynik: dist/GeneratorZUS_US7/

from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules
import os

SPEC_DIR = os.path.dirname(os.path.abspath(SPEC))

# --- PyMuPDF 1.18.x — moduł "fitz" ------------------------------------------
fitz_datas, fitz_bins, fitz_hidden = collect_all("fitz")

# --- openpyxl: dane (szablony XML/xlsl) + ukryte importy ----------------------
openpyxl_datas  = collect_data_files("openpyxl")
openpyxl_hidden = collect_submodules("openpyxl")

# --- python-docx (docx): dane + ukryte importy --------------------------------
docx_datas  = collect_data_files("docx")
docx_hidden = collect_submodules("docx")

# --- lxml: ukryte importy ------------------------------------------------------
lxml_hidden = collect_submodules("lxml")

datas = (
    fitz_datas
    + openpyxl_datas
    + docx_datas
    + [
        (os.path.join(SPEC_DIR, "szablon.pdf"), "."),
        (os.path.join(SPEC_DIR, "zalacznik2", "szablon_pusty.docx"), "zalacznik2"),
        (os.path.join(SPEC_DIR, u"UPOWA\u017bNIENIE ZUS.docx"), "."),
        (os.path.join(SPEC_DIR, "Zalacznik NR 8.pdf"), "."),
        (os.path.join(SPEC_DIR, "ICO.ico"), "."),
    ]
)

binaries = fitz_bins

hidden = fitz_hidden + openpyxl_hidden + docx_hidden + lxml_hidden

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

