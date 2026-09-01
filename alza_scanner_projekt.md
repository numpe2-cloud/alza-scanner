# Alza Scanner – definice projektu

## Cíl projektu
Nástroj, který sleduje vlastní, ručně vybraný seznam produktů na Alze (ne celý katalog) a upozorní e-mailem, když cena produktu klesne výrazně pod jeho historické minimum. Osobní, personalizovaný nástroj, ne obecný "hlídač slev".

## Rozsah první verze (MVP)
- Jeden e-shop: Alza.cz
- Malý, ručně spravovaný seznam produktů (řádově desítky, ne stovky/tisíce)
- Sledování stránky **jednotlivého produktu** (ne kategoriových výpisů) — díky malému počtu produktů je to objemově v pohodě
- Referenční hodnota = **minimum z posledních ~6 měsíčních záznamů ceny** (ne průměr, ne cizí "nejnižší cena za 30 dní" — to pole Alza nezobrazuje)
- Alert e-mailem při výrazném poklesu ceny
- Žádné kupování, žádná automatizace nákupu — nástroj jen informuje

## Vědomé limitace (ne přehlédnuté chyby)
- Kódové slevy typu ALZADNY se zobrazují nekonzistentně (ověřeno přímým pozorováním) — scanner na ně nemusí spolehlivě reagovat.
- Historie kratší než ~3 měsíce nebude použitelná pro rozhodování — první měsíce běhu jsou "rozjezdové", ne ostré vyhodnocování.
- Sledují se jen produkty, které si sám vybereš — scanner nehlídá nic mimo tento seznam.

## Klíčová architektonická rozhodnutí (shrnutí z rozhovoru)
| Otázka | Rozhodnutí |
|---|---|
| Seznam produktů | Samostatný soubor `polozky.yaml`, ne natvrdo v kódu |
| Kolik produktů | Neomezeno kódem, `for` cyklus projde vše, co je v souboru |
| Zdroj ceny | Stránka jednotlivého produktu (aktuální cena vs. přeškrtnutá cena) |
| Referenční hodnota | Minimum z uložené historie (ne průměr, ne cizí pole) |
| Ukládání historie | Samostatný soubor `monitoringcen.csv`, zápis 1× měsíčně |
| Kontrola/alert | Časté spouštění (např. 1× hodinu), porovnává aktuální cenu s uloženým minimem |
| Deduplikace alertů | Jednoduchý seznam "už nahlášeno", aby nechodil opakovaný e-mail na stejnou slevu |
| Rychlost scrapování | Slušné rozestupy mezi requesty (řádově sekundy); objem je malý, není to kritické |

## Fáze projektu

**Fáze 1 – Kostra a konfigurace**
- `polozky.yaml` se seznamem sledovaných produktů (URL + popisek)
- Skript, co soubor načte a projde ho

**Fáze 2 – Scraping jednoho produktu**
- Stažení stránky produktu, vytažení aktuální ceny (a přeškrtnuté ceny, pokud je)
- Ověření na 2-3 reálných produktech, že parsování funguje spolehlivě

**Fáze 3 – Historie cen**
- `monitoringcen.csv` – měsíční zápis ceny pro každý sledovaný produkt
- Logika pro čtení historie a výpočet minima

**Fáze 4 – Vyhodnocení a alert**
- Porovnání aktuální ceny s historickým minimem
- Práh pro "podezřele nízká cena" (např. 50 %)
- Odeslání e-mailu při překročení prahu
- Seznam "už nahlášeno" proti opakovaným alertům

**Fáze 5 – Automatizace a nasazení**
- Plánování běhu (měsíční záznam vs. hodinová kontrola)
- Kontejnerizace a nasazení na homelab (stejně jako god-not-responding)
- Základní logování/monitoring, že scanner reálně běží

**Fáze 6 – Testování bez čekání na skutečnou událost**
- Mock/testovací data místo skutečného stažení stránky, pro ověření, že alert funguje

## Otevřené otázky k doladění (řešit průběžně, ne teď)
- Přesný formát `polozky.yaml` (jaká pole u každého produktu)
- Přesná struktura sloupců v `monitoringcen.csv`
- Přesný práh pro alert (% pokles)
