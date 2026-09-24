"""Uloží aktuální ceny do historie.

Na Windows je spouštěn pomocí plánovače úloh každých 14 dní.
V Linuxu pomocí Dockeru ručně."""

import logging
import os
from src.scraper import ziskej_ceny_vsech_produktu
from src.uloz_cenu import uloz_cenu

os.makedirs("data", exist_ok=True)

logging.basicConfig(
    filename="data/ulozeni_ceny.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

try:
    vysledky = ziskej_ceny_vsech_produktu()
    for polozka in vysledky:
        uloz_cenu(polozka["nazev"], polozka["cena"])
        logging.info(f"Položka {polozka["nazev"]}, cena uložena")
except Exception as e:
    logging.error(f"Skript ulozeni_ceny hlásí: {e}")
