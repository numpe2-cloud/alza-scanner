"""Zkontroluje aktuální cenu.

Porovná aktuální ceny s historickými cenami a pokud cena vyjde nižší než prah, tak pošle alert.
Na Windows je spouštěn pomocí plánovače úloh každý den.
V Linuxu pomocí Dockeru ručně."""

import logging
import os
from src.scraper import ziskej_ceny_vsech_produktu
from src.historie_cen import najdi_minimum
from src.posouzeni_ceny import posouzeni_ceny, je_podezrela_cena
from src.alerty import kontrola_alertu

os.makedirs("data", exist_ok=True)

logging.basicConfig(
    filename="data/kontrola_ceny.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("Spouštím kontrolu ceny")

try:
    vysledky = ziskej_ceny_vsech_produktu()
except Exception as e:
    logging.error(f"Scraping selhal: {e}")
    vysledky = []

for polozka in vysledky:
    try:
        minimum = najdi_minimum(polozka["nazev"])
        podezrela = je_podezrela_cena(polozka["cena"], minimum)
        if podezrela:
            logging.warning(
                f"Položka {polozka['nazev']}: cena {polozka['cena']} je podezřele nízká "
                f"proti minimu {minimum}, posílám alert s upozorněním"
            )
        je_nizka = posouzeni_ceny(polozka["cena"], minimum)
        logging.info(f"Položka {polozka['nazev']}, nízká cena: {je_nizka}")
        if je_nizka:
            kontrola_alertu(polozka["nazev"], polozka["cena"], polozka["url"], podezrela=podezrela)
    except Exception as e:
        logging.error(f"Položka {polozka['nazev']}: kontrola selhala: {e}")
