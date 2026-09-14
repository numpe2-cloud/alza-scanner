"""Najde nejnižší cenu.

Vezme ceny ze souboru monitoringcen.csv a najde v nich nejnižší cenu
a to max za posledních 6 měsíců."""

import csv
from datetime import datetime, timedelta


def najdi_minimum(nazev_produktu, cesta_k_souboru="data/monitoringcen.csv"):
    dnesni_datum = datetime.now()
    cutoff_datum = dnesni_datum - timedelta(days=182)

    with open(cesta_k_souboru, "r", encoding="utf-8-sig", newline="") as soubor:
        reader = csv.DictReader(soubor)
        ceny = []
        for radek in reader:
            if radek["nazev"] != nazev_produktu:
                continue
            datum_zaznamu = datetime.strptime(radek["datum"], "%Y-%m-%d")
            if datum_zaznamu < cutoff_datum:
                continue
            ceny.append(float(radek["cena"]))

    if not ceny:
        return None

    return min(ceny)
