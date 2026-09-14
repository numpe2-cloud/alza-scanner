"""Připraví html stránku pro dashboard."""

PRAH_NAD_MINIMEM = 0  # nad tuto hodnotu (v %) je cena "dražší než minimum" = červená


def sestav_html(souhrn, grafy):
    """Sestaví kompletní HTML stránku dashboardu ze souhrnu cen a base64 grafů, vrátí ji jako text."""
    radky_tabulky = ""
    for polozka in souhrn:
        if polozka["rozdil_procent"] > PRAH_NAD_MINIMEM:
            trida_barvy = "draha-cena"
        elif polozka["rozdil_procent"] < PRAH_NAD_MINIMEM:
            trida_barvy = "dobra-cena"
        else:
            trida_barvy = ""
        znamenko = "+" if polozka["rozdil_procent"] >= PRAH_NAD_MINIMEM else ""
        radky_tabulky += f"""
        <tr>
          <td>{polozka['nazev']}</td>
          <td>{polozka['aktualni_cena']:.0f} Kč</td>
          <td>{polozka['minimalni_cena']:.0f} Kč</td>
          <td class="{trida_barvy}">{znamenko}{polozka['rozdil_procent']}%</td>
        </tr>"""

    sekce_grafu = ""
    for nazev, obrazek_base64 in grafy.items():
        sekce_grafu += f"""
        <div class="graf-karta">
          <h3>{nazev}</h3>
          <img src="data:image/png;base64,{obrazek_base64}" alt="Vývoj ceny — {nazev}">
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<title>Přehled cen</title>
<style>
  body {{ font-family: -apple-system, Arial, sans-serif; background: #1c100a; color: #f3e9e0; margin: 0; padding: 2rem; }}
  h1 {{ display: inline-block; font-size: 26px; font-weight: 500; margin: 0; border-bottom: 2px solid #d85a30; padding-bottom: 8px; }}
  table {{ width: 70%; max-width: 640px; margin: 0 auto 2.5rem; border-collapse: collapse; background: #26160e; border-radius: 8px; overflow: hidden; }}
  th, td {{ text-align: center; padding: 8px 12px; border-bottom: 1px solid #3a2418; font-size: 14px; }}
  th {{ background: #301c11; font-weight: 500; font-size: 12px; color: #c99a80; }}
  td {{ color: #f3e9e0; }}
  td.dobra-cena {{ background: #173404; color: #97c459; font-weight: 500; }}
  td.draha-cena {{ background: #501313; color: #f09595; font-weight: 500; }}
  .grafy {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; max-width: 640px; margin: 0 auto; }}
  .graf-karta {{ background: #26160e; border-radius: 8px; padding: 1rem; }}
  .graf-karta h3 {{ margin: 0 0 0.5rem; font-size: 15px; font-weight: 500; text-align: center; color: #f8e6d3; }}
  .graf-karta img {{ width: 100%; height: auto; display: block; }}
</style>
</head>
<body>
  <div style="text-align: center; margin-bottom: 1.75rem;">
    <h1>Přehled cen</h1>
  </div>
  <table>
    <thead>
      <tr><th>Produkt</th><th>Aktuální cena</th><th>Minimum</th><th>Rozdíl od minima</th></tr>
    </thead>
    <tbody>{radky_tabulky}
    </tbody>
  </table>
  <div class="grafy">{sekce_grafu}
  </div>
</body>
</html>"""
