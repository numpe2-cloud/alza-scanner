"""Uloží cenu do souboru monitoringcen.csv."""

import csv
import datetime
import os

VYSTUP = "data/monitoringcen.csv"


def uloz_cenu(nazev, cena):
    datum = datetime.datetime.now()
    datum_cisty = datum.strftime("%Y-%m-%d")
    existuje = os.path.exists(VYSTUP)
    with open(VYSTUP, "a", encoding="utf-8-sig", newline="") as soubor:
        writer = csv.writer(soubor)
        if not existuje:
            writer.writerow(["datum", "nazev", "cena"])
        writer.writerow([datum_cisty, nazev, cena])
