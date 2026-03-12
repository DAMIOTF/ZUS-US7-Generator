# -*- coding: utf-8 -*-
"""
Rejestr typów dokumentów do generowania.

Aby dodać nowy typ dokumentu:
    1. Utwórz moduł z funkcją: generate(person, date_str, options) -> bytes
    2. Zarejestruj go wywołując ``register()``.
    3. Checkbox pojawi się automatycznie w GUI.
"""
from typing import Callable, Dict, List, Optional


# Lista zarejestrowanych typów dokumentów
DOC_TYPES: List[dict] = []


def register(
    doc_id: str,
    label: str,
    extension: str,
    filename_tpl: str,
    generate_fn: Callable[[dict, str, dict], bytes],
) -> None:
    """Rejestruje nowy typ dokumentu.

    Parametry:
        doc_id       – unikalny identyfikator (np. ``"us7"``)
        label        – etykieta do wyświetlenia (np. ``"ZUS US-7"``)
        extension    – rozszerzenie pliku (np. ``".pdf"``)
        filename_tpl – szablon nazwy pliku z placeholderami ``{imie}``,
                       ``{nazwisko}`` (np. ``"ZUS US-7 {imie} {nazwisko}"``)
        generate_fn  – funkcja ``(person, date_str, options) -> bytes``
    """
    DOC_TYPES.append({
        "id": doc_id,
        "label": label,
        "extension": extension,
        "filename_tpl": filename_tpl,
        "generate": generate_fn,
    })


def get_all() -> List[dict]:
    """Zwraca listę wszystkich zarejestrowanych typów dokumentów."""
    return list(DOC_TYPES)


def get_by_id(doc_id: str) -> Optional[dict]:
    """Zwraca typ dokumentu o podanym ``doc_id`` lub ``None``."""
    for d in DOC_TYPES:
        if d["id"] == doc_id:
            return d
    return None
