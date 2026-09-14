"""Vytvoří seznam položek ze souboru polozky.yaml."""

import yaml

VSTUP = "config/polozky.yaml"


def nacti_polozky():
    with open(VSTUP, "r", encoding="utf-8-sig") as soubor:
        list_polozek = yaml.safe_load(soubor)
        return list_polozek
