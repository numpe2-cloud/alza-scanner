"""Posouzení zda je sleva dostatečná.

Dostatečná sleva je ta, která je o 10% nižší než je minimální cena za max posledních 6 měsíců.
Vrátí False ,pokud cena produktu ještě není uložena (minimalni_cena = None)"""


def posouzeni_ceny(aktualni_cena, minimalni_cena, prah=0.9):
    if minimalni_cena is None:
        return False
    hranicni_cena = minimalni_cena * prah
    return aktualni_cena <= hranicni_cena
