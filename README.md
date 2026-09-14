# Alza Scanner

Osobní nástroj pro sledování cen vybraných produktů na Alza.cz — hlídá historické minimum a pošle e-mailový alert, když cena klesne pod obvyklou hranici.

![Architektura Alza Scanneru](schema.png)

## Motivace

Chtěl jsem vytvořit něco, co pro mě bude užitečné v praxi. Nejdřív jsem uvažoval nad scraperem obsahu Českého rozhlasu, ale postupně mi došlo, že bych ho stejně nevyužíval. Sledování vývoje cen u produktů, který si časem plánuji koupit, mi přišlo jako mnohem praktičtější nápad — do projektu si teď můžu přidat jakýkoliv produkt a sledovat jeho cenu, dokud se nerozhodnu koupit.

Vím, že podobná řešení už existují a možná i lepší než to moje, ale bavilo mě zkusit si to postavit od nuly. Překvapilo mě, jak i na první pohled malý projekt je ve skutečnosti komplexní a kolik různých problémů se během vývoje objeví — třeba jsem musel vyzkoušet víc postupů, než se mi podařilo obejít zabezpečení stránek Alzy a spolehlivě načíst aktuální cenu.

## Tech stack

- **Python 3** — hlavní jazyk projektu
- **Playwright** — scraping cen z Alza.cz (headless=False kvůli obejití Cloudflare ochrany)
- **PyYAML** — konfigurace sledovaných produktů (`polozky.yaml`)
- **csv** / **datetime** — ukládání a práce s historií cen
- **smtplib** — odesílání e-mailových alertů
- **python-dotenv** — správa citlivých údajů (přihlašovací údaje k e-mailu) mimo kód
- **matplotlib** — grafy vývoje cen v dashboardu
- **pytest** — automatizované testy
- **flake8** — kontrola stylu kódu

## Jak to funguje

Projekt má tři hlavní části:

1. **Sběr a ukládání cen** — `scraper.py` načte aktuální ceny sledovaných produktů (definovaných v `polozky.yaml`), `ulozeni_ceny.py` je uloží do `monitoringcen.csv`
2. **Kontrola a alerty** — `kontrola_ceny.py` porovná aktuální cenu s historickým minimem za posledních 6 měsíců (`historie_cen.py`, `posouzeni_ceny.py`) a při výhodné ceně pošle e-mailový alert (`alerty.py`, `odeslani_emailu.py`), s deduplikací přes 30denní cooldown
3. **Dashboard** — `vytvor_report.py` sestaví HTML přehled s grafy vývoje cen (`report_data.py`, `grafy_cen.py`, `report_html.py`)

Podrobné schéma toků mezi jednotlivými soubory je výše.

## Instalace a spuštění

1. Naklonuj repozitář:
   ```
   git clone <URL repozitáře>
   cd alza-scanner
   ```

2. Vytvoř a aktivuj virtuální prostředí:
   ```
   python -m venv .venv
   ```
   Aktivace (podle systému):
   ```
   source .venv/bin/activate      # Linux/WSL/Mac
   .venv\Scripts\activate         # Windows
   ```

3. Nainstaluj závislosti:
   ```
   pip install -r requirements.txt
   playwright install
   ```

4. Nastav sledované produkty v `polozky.yaml` podle existujícího vzoru.

5. Vytvoř soubor `.env` v kořeni projektu s vlastními přihlašovacími údaji k e-mailu (viz sekce Proměnné prostředí níže).

6. Spusť ruční test:
   ```
   python ulozeni_ceny.py
   ```
   Zkontroluj, že se cena uložila do `data/monitoringcen.csv`, a pak:
   ```
   python kontrola_ceny.py
   ```

7. Pro pravidelné automatické spouštění (např. jednou denně) nastav podle svého prostředí Windows Task Scheduler nebo cron.

## Proměnné prostředí

Projekt potřebuje soubor `.env` v kořeni projektu (nikdy se necommituje do gitu — je v `.gitignore`) s těmito proměnnými:

```
odesilatel=tvuj_email@gmail.com
heslo=tvoje_app_password
prijemce=email_kam_chodi_alerty@example.com
```

**Poznámka:** `heslo` musí být Gmail App Password (vygenerovaný v nastavení Google účtu), ne běžné heslo k účtu — Gmail SMTP s normálním heslem odmítne přihlášení.

## Testování

Projekt má jednotkové testy (`pytest`) pro čisté funkce (`posouzeni_ceny()`, `najdi_minimum()`) a je průběžně kontrolovaný linterem `flake8`.

```
pytest
flake8 .
```

## Etická poznámka ke scrapingu

Před spuštěním jsem se přes sociální sítě zeptal na proveditelnost a etickou stránku scrapingu. Oficiální účet Alza.cz mi na dotaz ohledně osobního, nízkoobjemového monitoringu cen odpověděl, že v takhle malém rozsahu nemají námitky.

## Použití AI

Většinu projektu (scraper, ukládání a kontrola cen, alerty, testy) jsem psal sám s pomocí AI asistenta, který mě vedl a opravoval chyby, ale kód psal vždy já. Výjimkou je sekce dashboardu — `report_data.py`, `grafy_cen.py` a `report_html.py` — kterou navrhla a napsala přímo AI. Sestavování grafů a HTML reportu mě nebavilo, ale zároveň jsem chtěl mít v projektu hezký přehledový dashboard, takže jsem se rozhodl tuhle část nechat na AI.
