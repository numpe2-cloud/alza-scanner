"""Vyhodnotí, zda poslat alert.

Zjistí pomocí uložených alertů, zda daný alert už nebyl poslán
a případně před jakou dobou, byl poslán.
Pokud alert nebyl poslán, tak vyhodnotí jako pošli alert.
Pokud je alert v seznamu a jeho datum, je nižší než časový úsek, tak ho nepošle.
Pokud starší než časový úsek, tak ho pošle.
Na konci procesu přepíše soubor seznam_alertu.csv.
To má zabránit, aby do emailu chodilo více alertů, odkazující ke stejné slevě."""

import csv
import os
from datetime import datetime, timedelta
from src.odeslani_emailu import posli_email

CASOVY_USEK = 30
CESTA_K_SOUBORU = "data/seznam_alertu.csv"


def priprav_soubor(cesta_k_souboru):
    slozka = os.path.dirname(cesta_k_souboru)
    if slozka:
        os.makedirs(slozka, exist_ok=True)
    if not os.path.exists(cesta_k_souboru):
        with open(cesta_k_souboru, "w", encoding="utf-8-sig", newline="") as soubor:
            writer = csv.writer(soubor)
            writer.writerow(["datum", "nazev"])


def kontrola_alertu(nazev, cena, url, cesta_k_souboru=CESTA_K_SOUBORU, podezrela=False):
    priprav_soubor(cesta_k_souboru)

    with open(cesta_k_souboru, "r", encoding="utf-8-sig", newline="") as soubor:
        reader = csv.DictReader(soubor)
        seznam_alertu = list(reader)

    dnesni_datum = datetime.now()
    dnesni_datum_text = dnesni_datum.strftime("%Y-%m-%d")
    nalezeno = False
    for radek in seznam_alertu:
        if radek["nazev"] == nazev:
            nalezeno = True
            datum_alertu = datetime.strptime(radek["datum"], "%Y-%m-%d")
            rozdil = dnesni_datum - datum_alertu
            if rozdil >= timedelta(days=CASOVY_USEK):
                if posli_email(nazev, cena, url, podezrela):
                    radek["datum"] = dnesni_datum_text
    if not nalezeno:
        if posli_email(nazev, cena, url, podezrela):
            seznam_alertu.append({"datum": dnesni_datum_text, "nazev": nazev})

    with open(cesta_k_souboru, "w", encoding="utf-8-sig", newline="") as soubor:
        writer = csv.DictWriter(soubor, fieldnames=["datum", "nazev"])
        writer.writeheader()
        for radek in seznam_alertu:
            writer.writerow(radek)
