"""Vyhodnotí, zda poslat alert.

Zjistí pomocí uložených alertů, zda daný alert už nebyl poslán
a případně před jakou dobou, byl poslán.
Pokud alert nebyl poslán, tak vyhodnotí jako pošli alert.
Pokud je alert v seznamu a jeho datum, je nižší než 30 dní, tak ho nepošle.
Pokud starší než 30 dní, tak ho pošle.
Na konci procesu přepíše soubor seznam_alertu.csv.
To má zabránit, aby do emailu chodilo více alertů, odkazující ke stejné slevě."""

import csv
import os
from datetime import datetime, timedelta
from src.odeslani_emailu import posli_email

existuje = os.path.exists("data/seznam_alertu.csv")
if not existuje:
    with open("data/seznam_alertu.csv", "w", encoding="utf-8-sig", newline="") as soubor:
        writer = csv.writer(soubor)
        writer.writerow(["datum", "nazev"])


def kontrola_alertu(nazev, cena, url):
    with open("data/seznam_alertu.csv", "r", encoding="utf-8-sig", newline="") as soubor:
        reader = csv.DictReader(soubor)
        seznam_alertu = list(reader)
        nalezeno = False
        for radek in seznam_alertu:
            if radek["nazev"] == nazev:
                nalezeno = True
                datum_alertu = datetime.strptime(radek["datum"], "%Y-%m-%d")
                dnesni_datum = datetime.now()
                dnesni_datum_text = datetime.now().strftime("%Y-%m-%d")
                rozdil = (dnesni_datum - datum_alertu)
                if rozdil >= timedelta(days=30):
                    radek["datum"] = dnesni_datum_text
                    posli_email(nazev, cena, url)
        if not nalezeno:
            seznam_alertu.append({"datum": datetime.now().strftime("%Y-%m-%d"), "nazev": nazev})
            posli_email(nazev, cena, url)
        with open("data/seznam_alertu.csv", "w", encoding="utf-8-sig", newline="") as soubor:
            writer = csv.DictWriter(soubor, fieldnames=["datum", "nazev"])
            writer.writeheader()
            for radek in seznam_alertu:
                writer.writerow(radek)
