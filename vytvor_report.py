"""Vytvoří dashboard v html.

Vezme historickÉ ceny a údaje k vykreslení grafů a vytvoří dashboard v HTML.
Skript se spouští ručně, když chce uživatel vidět výsledky v grafické podobě."""
from src.report_data import nacti_historii, sestav_souhrn
from src.grafy_cen import vykresli_graf
from src.report_html import sestav_html


def main():
    historie = nacti_historii("data/monitoringcen.csv")
    souhrn = sestav_souhrn(historie)

    grafy = {}
    for nazev, zaznamy in historie.items():
        grafy[nazev] = vykresli_graf(zaznamy)

    html = sestav_html(souhrn, grafy)

    with open("report.html", "w", encoding="utf-8") as soubor:
        soubor.write(html)

    print("Report vygenerován: report.html")


if __name__ == "__main__":
    main()
