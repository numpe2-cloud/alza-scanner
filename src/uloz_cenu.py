"""Uloží cenu do souboru monitoringcen.csv."""

import csv
import datetime
import os


def uloz_cenu(nazev, cena):
    datum = datetime.datetime.now()
    datum_cisty = datum.strftime("%Y-%m-%d")
    existuje = os.path.exists("data/monitoringcen.csv")
    with open("data/monitoringcen.csv", "a", encoding="utf-8-sig", newline="") as soubor:
        writer = csv.writer(soubor)
        if not existuje:
            writer.writerow(["datum", "nazev", "cena"])
        writer.writerow([datum_cisty, nazev, cena])
