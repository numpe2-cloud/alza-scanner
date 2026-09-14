"""Získá aktuální ceny produktů.

Otevře si v prohlížeči web a scrapuje aktuální ceny všech položek a pak ho zavře."""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from src.nacti_polozky import nacti_polozky


def ziskej_ceny_vsech_produktu():
    list_polozek = nacti_polozky()
    vysledky = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:153.0) "
            "Gecko/20100101 Firefox/153.0"
        )

        def ziskej_cenu(page, url):
            page.goto(url, wait_until="domcontentloaded")

            # Počkáme, až se objeví cena
            page.wait_for_selector(".js-price-box__primary-price__value")

            # Vezmeme aktuální HTML
            html = page.content()

            # BeautifulSoup
            strom = BeautifulSoup(html, "html.parser")
            stranka = strom.find(
                "span",
                class_="js-price-box__primary-price__value"
            )

            text = stranka.get_text(strip=True)
            text1 = text.replace("\xa0", "")
            text2 = text1.replace("-", "")
            text3 = text2.replace(",", "")
            cena_z_html = float(text3)
            return cena_z_html

        for polozka in list_polozek:
            cena = ziskej_cenu(page, polozka["url"])
            vysledky.append({"nazev": polozka["nazev"], "url": polozka["url"], "cena": cena})
        browser.close()
    return vysledky
