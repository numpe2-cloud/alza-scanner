"""Uloží aktuální ceny do historie.

Na windows je spouštěn pomocí plánovače úloh každých 14 dní
V linuxu pomocí cronu"""

import logging
from src.scraper import ziskej_ceny_vsech_produktu
from src.uloz_cenu import uloz_cenu

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
