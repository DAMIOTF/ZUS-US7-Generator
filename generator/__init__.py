"""
generator — silnik i interfejs graficzny aplikacji Generator ZUS US-7.

Publiczne API pakietu:
    fill_pdf(person, date_str, options) -> bytes
    load_sheet_data(wb, sheet_name)     -> list[dict]
    resource_path(name)                 -> str
"""
from .pdf_engine import fill_pdf
from .excel_loader import load_sheet_data
from .constants import resource_path

__all__ = ["fill_pdf", "load_sheet_data", "resource_path"]
