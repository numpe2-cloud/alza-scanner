"""Posouzení zda je sleva dostatečná.

Dostatečná sleva je ta, která je o 10% nižší než je minimální cena za max posledních 6 měsíců.
Vrátí False, pokud minimální cena ještě není uložena (minimalni_cena = None)
nebo pokud se aktuální cenu nepodařilo zjistit (aktualni_cena = None)."""

PRAH = 0.9
SPODNI_HRANICE = 0.3


def posouzeni_ceny(aktualni_cena, minimalni_cena, prah=PRAH):
    if minimalni_cena is None or aktualni_cena is None:
        return False
    hranicni_cena = minimalni_cena * prah
    return aktualni_cena <= hranicni_cena


def je_podezrela_cena(aktualni_cena, minimalni_cena, spodni_hranice=SPODNI_HRANICE):
    if minimalni_cena is None or aktualni_cena is None:
        return False
    return aktualni_cena < minimalni_cena * spodni_hranice
