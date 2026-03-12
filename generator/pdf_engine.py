# -*- coding: utf-8 -*-
"""
Silnik PDF — wypełnianie szablonu ZUS US-7 przez manipulację strumieniem XFA.

Publiczne API:
    fill_pdf(person, date_str, options) -> bytes
"""
import re

import fitz  # PyMuPDF

from .constants import DATASETS_XREF, TEMPLATE_PDF


# ─── XML helpers ─────────────────────────────────────────────────────────────

def _xml_escape(value: str) -> str:
    """Zamienia znaki specjalne XML na encje."""
    return (
        value
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def set_xfa_field(xml: str, field: str, value: str) -> str:
    """Zastępuje pierwsze wystąpienie pola XFA *field* wartością *value*."""
    val_esc = _xml_escape(value)
    repl    = f"<{field}>{val_esc}</{field}>"
    pat_cnt = re.compile(
        r"<" + re.escape(field) + r">[^<]*</" + re.escape(field) + r">",
        re.DOTALL,
    )
    pat_sc = re.compile(r"<" + re.escape(field) + r"\s*/>", re.DOTALL)
    if pat_cnt.search(xml):
        return pat_cnt.sub(repl, xml, count=1)
    if pat_sc.search(xml):
        return pat_sc.sub(repl, xml, count=1)
    return xml


# ─── PDF generator ───────────────────────────────────────────────────────────

def fill_pdf(person: dict, date_str: str, options: dict) -> bytes:
    """Wypełnia szablon ZUS US-7 i zwraca bajty gotowego pliku PDF.

    Parametry ``options``:

    +-----------------------+------------------------------------------------+
    | Klucz                 | Opis                                           |
    +=======================+================================================+
    | radio_type            | "1" = ZAŚWIADCZENIA, "2" = INFORMACJI          |
    | cb_ubezpieczenia      | pkt 3 / CheckBox1 (1) — ubezpieczenia społ.    |
    | cb_przerwy            | pkt 3 / CheckBox2 (1) — przerwy w składkach    |
    | cb_podstawy           | pkt 3 / CheckBox3 (1) — podstawy wymiaru       |
    | cb_warunki            | pkt 3 / CheckBox4 (1) — szczególne warunki     |
    | cb_ofe_czlonek        | pkt 3 / CheckBox3 (2) — członkostwo OFE        |
    | cb_ofe_skladki        | pkt 3 / CheckBox1 (2) — składki OFE            |
    | delivery_placowka     | pkt 5 — odbiór w placówce ZUS                  |
    | delivery_poczta       | pkt 5 — odbiór pocztą                          |
    | delivery_pue          | pkt 5 — odbiór na koncie PUE                   |
    | uzasadnienie          | treść uzasadnienia (pkt 4)                     |
    +-----------------------+------------------------------------------------+
    """
    doc = fitz.open(TEMPLATE_PDF)
    raw = doc.xref_stream(DATASETS_XREF)
    xml = raw.decode("utf-8")

    # ── Dane osobowe (pkt 1) ──────────────────────────────────────────────────
    xml = set_xfa_field(xml, "Imie",          person["imie"])
    xml = set_xfa_field(xml, "Nazwisko",       person["nazwisko"])
    xml = set_xfa_field(xml, "Numer_PESEL",    person["pesel"])

    # Rozpoznanie wsi: gdy poczta != miejscowosc, miejscowosc to wioska → ulica
    ulica       = person["ulica"].strip()
    miejscowosc = person["miejscowosc"].strip()
    poczta      = person.get("poczta", "").strip()
    if poczta and poczta != miejscowosc and not ulica:
        ulica = miejscowosc
    if poczta:
        miejscowosc = poczta

    xml = set_xfa_field(xml, "Ulica",          ulica)
    xml = set_xfa_field(xml, "Numer_domu",     person["nr_domu"])
    xml = set_xfa_field(xml, "Numer_lokalu",   person["nr_lokalu"])
    xml = set_xfa_field(xml, "kod_pocztowy",   person["kod_pocztowy"])
    xml = set_xfa_field(xml, "Miejscowosc",    miejscowosc)
    xml = set_xfa_field(xml, "Numer_telefonu", person["telefon"])
    xml = set_xfa_field(xml, "Data",           date_str)

    # ── Rodzaj dokumentu (pkt 2) ──────────────────────────────────────────────
    radio_val = options.get("radio_type", "1")
    xml = re.sub(
        r"<RadioButtonList(?:\s*/|>[^<]*</RadioButtonList)>",
        f"<RadioButtonList>{radio_val}</RadioButtonList>",
        xml, count=1,
    )

    # ── Checkboxy (pkt 3) ─────────────────────────────────────────────────────
    # CheckBox1 (1. wystąpienie) = o zgłoszeniu i okresach podlegania ubezpieczeniom
    xml = set_xfa_field(xml, "CheckBox1", "1" if options.get("cb_ubezpieczenia", True)  else "0")
    # CheckBox2 (1.) = o przerwach w opłacaniu składek
    xml = set_xfa_field(xml, "CheckBox2", "1" if options.get("cb_przerwy",        False) else "0")
    # CheckBox3 (1.) = o podstawach wymiaru składek
    xml = set_xfa_field(xml, "CheckBox3", "1" if options.get("cb_podstawy",       False) else "0")
    # CheckBox4 (1.) = o zgłoszeniu przez pracodawcę (szczególne warunki)
    xml = set_xfa_field(xml, "CheckBox4", "1" if options.get("cb_warunki",        False) else "0")

    # CheckBox3 (2. wystąpienie) = dane o członkostwie w OFE
    czl_val     = "1" if options.get("cb_ofe_czlonek", False) else "0"
    cb3_matches = list(re.compile(r"<CheckBox3>([^<]*)</CheckBox3>").finditer(xml))
    if len(cb3_matches) >= 2:
        m   = cb3_matches[1]
        xml = xml[: m.start()] + f"<CheckBox3>{czl_val}</CheckBox3>" + xml[m.end() :]

    # CheckBox1 (2. wystąpienie) = składki przekazane do OFE
    ofe_val     = "1" if options.get("cb_ofe_skladki", False) else "0"
    cb1_matches = list(re.compile(r"<CheckBox1>([^<]*)</CheckBox1>").finditer(xml))
    if len(cb1_matches) >= 2:
        m   = cb1_matches[1]
        xml = xml[: m.start()] + f"<CheckBox1>{ofe_val}</CheckBox1>" + xml[m.end() :]

    # ── Uzasadnienie (pkt 4) ──────────────────────────────────────────────────
    xml = set_xfa_field(xml, "Uzasadnienie_wniosku", options.get("uzasadnienie", ""))

    # ── Sposób odbioru (pkt 5) ────────────────────────────────────────────────
    xml = set_xfa_field(xml, "w_placówce_ZUS", "1" if options.get("delivery_placowka", True)  else "0")
    xml = set_xfa_field(xml, "pocztą",          "1" if options.get("delivery_poczta",   False) else "0")
    xml = set_xfa_field(xml, "na_koncie_PUE",   "1" if options.get("delivery_pue",      False) else "0")

    doc.update_stream(DATASETS_XREF, xml.encode("utf-8"))
    output = doc.tobytes(garbage=4, deflate=True)
    doc.close()
    return output
