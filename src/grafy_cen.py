"""Skript co připraví grafy pro vložení dat, která pocházejí ze souboru monitoringcen.csv."""

import io
import base64
from matplotlib import pyplot as plt

BARVA_POZADI = "#1c100a"
BARVA_CARY = "#d85a30"
BARVA_POPISKU = "#c99a80"
OKRAJ_GRAFU = 0.15


def vykresli_graf(zaznamy):
    """Nakreslí vývoj ceny pro jeden produkt a vrátí ho jako base64 text."""
    datumy = [datum for datum, _ in zaznamy]
    ceny = [cena for _, cena in zaznamy]

    fig, ax = plt.subplots(figsize=(6, 3))
    fig.patch.set_facecolor(BARVA_POZADI)
    ax.set_facecolor(BARVA_POZADI)

    ax.plot(datumy, ceny, marker="o", color=BARVA_CARY)

    # osy podle skutečného rozsahu cen, ne od nuly
    cena_min, cena_max = min(ceny), max(ceny)
    rozsah = cena_max - cena_min or cena_max * 0.05
    ax.set_ylim(cena_min - rozsah * OKRAJ_GRAFU, cena_max + rozsah * OKRAJ_GRAFU)

    ax.tick_params(axis="x", colors=BARVA_POPISKU, rotation=45)
    ax.tick_params(axis="y", colors=BARVA_POPISKU)
    for strana in ax.spines.values():
        strana.set_color("#3a2418")

    plt.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")
