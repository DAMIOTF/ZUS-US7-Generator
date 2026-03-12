"""
generator — silnik i interfejs graficzny aplikacji Generator ZUS US-7.

Publiczne API pakietu:
    fill_pdf(person, date_str, options) -> bytes
    fill_zalacznik2(person, date_str, options) -> bytes
    load_sheet_data_mapped(wb, sheet_name, cell_mapping) -> list[dict]
    resource_path(name)                 -> str
    doc_types                           -> rejestr dokumentów
"""
from .pdf_engine import fill_pdf
from .zalacznik2_engine import fill_zalacznik2
from .upowaznienie_engine import fill_upowaznienie
from .zalacznik8_engine import fill_zalacznik8
from .excel_loader import load_sheet_data_mapped
from .constants import resource_path
from . import doc_types

# ── Rejestracja typów dokumentów ──────────────────────────────────────────────
doc_types.register(
    doc_id="us7",
    label="ZUS US-7",
    extension=".pdf",
    filename_tpl="ZUS US-7 {imie} {nazwisko}",
    generate_fn=fill_pdf,
)

doc_types.register(
    doc_id="zalacznik2",
    label="Załącznik nr 2",
    extension=".docx",
    filename_tpl="Załącznik 2 {imie} {nazwisko}",
    generate_fn=fill_zalacznik2,
)

doc_types.register(
    doc_id="upowaznienie",
    label="Upoważnienie ZUS",
    extension=".docx",
    filename_tpl="Upoważnienie ZUS {imie} {nazwisko}",
    generate_fn=fill_upowaznienie,
)

doc_types.register(
    doc_id="zalacznik8",
    label="Załącznik nr 8",
    extension=".pdf",
    filename_tpl="Załącznik 8 {imie} {nazwisko}",
    generate_fn=fill_zalacznik8,
)

__all__ = [
    "fill_pdf", "fill_zalacznik2", "fill_upowaznienie", "fill_zalacznik8",
    "load_sheet_data_mapped", "resource_path",
    "doc_types",
]
