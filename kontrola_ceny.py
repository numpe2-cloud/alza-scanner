"""Zkontroluje aktuální cenu.

Porovná aktuální ceny s historickými cenami a pokud cena výjde nižší než prah, tak pošle alert.
Na windows je spouštěn pomocí plánovače úloh každý den.
V Linuxu pomocí cronu."""

import logging
from src.scraper import ziskej_ceny_vsech_produktu
from src.historie_cen import najdi_minimum
from src.posouzeni_ceny import posouzeni_ceny
from src.alerty import kontrola_alertu


logging.basicConfig(
    filename="data/kontrola_ceny.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("Spouštím kontrolu ceny")

try:
    vysledky = ziskej_ceny_vsech_produktu()
    for polozka in vysledky:
        minimum = najdi_minimum(polozka["nazev"])
        je_nizka = posouzeni_ceny(polozka["cena"], minimum, prah=0.9)
        logging.info(f"Položka {polozka["nazev"]}, nízká cena: {je_nizka}")
        if je_nizka:
            kontrola_alertu(polozka["nazev"], polozka["cena"], polozka["url"])

except Exception as e:
    logging.error(f"Skript kontrola_ceny hlásí: {e}")
