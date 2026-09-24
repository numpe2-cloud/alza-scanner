"""Uloží aktuální ceny do historie.

Na Windows je spouštěn pomocí plánovače úloh každých 14 dní.
V Linuxu pomocí Dockeru ručně."""

import logging
import os
from src.scraper import ziskej_ceny_vsech_produktu
from src.uloz_cenu import uloz_cenu
from src.historie_cen import najdi_minimum
from src.posouzeni_ceny import je_podezrela_cena

os.makedirs("data", exist_ok=True)

logging.basicConfig(
    filename="data/ulozeni_ceny.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

try:
    vysledky = ziskej_ceny_vsech_produktu()
except Exception as e:
    logging.error(f"Scraping selhal: {e}")
    vysledky = []

for polozka in vysledky:
    if polozka["cena"] is None:
        logging.warning(f"Položka {polozka['nazev']}: cena se nenačetla, neukládám")
        continue
    try:
        if je_podezrela_cena(polozka["cena"], najdi_minimum(polozka["nazev"])):
            logging.warning(
                f"Položka {polozka['nazev']}: cena {polozka['cena']} je podezřelá, neukládám"
            )
            continue
        uloz_cenu(polozka["nazev"], polozka["cena"])
        logging.info(f"Položka {polozka['nazev']}, cena uložena")
    except Exception as e:
        logging.error(f"Položka {polozka['nazev']}: uložení selhalo: {e}")
