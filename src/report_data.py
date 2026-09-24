"""Připraví data pro dashboard."""

import csv
from collections import defaultdict

from src.nacti_polozky import nacti_polozky


def nacti_historii(cesta="data/monitoringcen.csv"):
    """Načte CSV (datum,nazev,cena) a vrátí {nazev: [(datum, cena), ...]}, seřazené podle data.

    Do výsledku pustí jen produkty, které jsou aktuálně v polozky.yaml.
    Historie vyřazených produktů v CSV zůstává, jen se nezobrazí.
    """
    sledovane_nazvy = set()                              # množina názvů, které se mají zobrazit
    for polozka in nacti_polozky():
        sledovane_nazvy.add(polozka["nazev"])

    historie = defaultdict(list)
    with open(cesta, newline="", encoding="utf-8-sig") as soubor:
        ctecka = csv.DictReader(soubor)
        for radek in ctecka:
            if radek["nazev"] not in sledovane_nazvy:   # produkt už se nesleduje
                continue                                # přeskoč řádek, jdi na další
            historie[radek["nazev"]].append((radek["datum"], float(radek["cena"])))
    for nazev in historie:
        historie[nazev].sort(key=lambda zaznam: zaznam[0])
    return historie


def sestav_souhrn(historie):
    """Pro každý produkt spočítá aktuální cenu, historické minimum a rozdíl v %."""
    souhrn = []
    for nazev, zaznamy in historie.items():
        aktualni_cena = zaznamy[-1][1]
        minimalni_cena = min(cena for _, cena in zaznamy)
        rozdil_procent = round((aktualni_cena - minimalni_cena) / minimalni_cena * 100, 1)
        souhrn.append({
            "nazev": nazev,
            "aktualni_cena": aktualni_cena,
            "minimalni_cena": minimalni_cena,
            "rozdil_procent": rozdil_procent,
        })
    return souhrn
