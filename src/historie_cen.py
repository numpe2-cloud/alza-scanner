"""Najde nejnižší cenu.

Vezme ceny ze souboru monitoringcen.csv a najde v nich nejnižší cenu
a to max za posledních 6 měsíců.
Pokud soubor monitoringcen.csv neexistuje, tak vrátí None."""

import csv
import os
from datetime import datetime, timedelta

POCET_DNI = 182


def najdi_minimum(nazev_produktu, cesta_k_souboru="data/monitoringcen.csv"):
    if not os.path.exists(cesta_k_souboru):
        return None
    dnesni_datum = datetime.now()
    hranicni_datum = dnesni_datum - timedelta(days=POCET_DNI)

    with open(cesta_k_souboru, "r", encoding="utf-8-sig", newline="") as soubor:
        reader = csv.DictReader(soubor)
        ceny = []
        for radek in reader:
            if radek["nazev"] != nazev_produktu:
                continue
            datum_zaznamu = datetime.strptime(radek["datum"], "%Y-%m-%d")
            if datum_zaznamu < hranicni_datum:
                continue
            ceny.append(float(radek["cena"]))

    if not ceny:
        return None

    return min(ceny)
