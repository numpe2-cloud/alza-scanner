from src.uloz_cenu import uloz_cenu


def test_novy_soubor_ma_hlavicku(tmp_path):
    cesta = tmp_path / "monitoringcen.csv"
    uloz_cenu("tv", 1000.0, cesta)
    radky = cesta.read_text(encoding="utf-8-sig").splitlines()
    assert radky[0] == "datum,nazev,cena"
    assert radky[1].endswith(",tv,1000.0")


def test_druhe_ulozeni_neprida_hlavicku(tmp_path):
    cesta = tmp_path / "monitoringcen.csv"
    uloz_cenu("tv", 1000.0, cesta)
    uloz_cenu("tv", 900.0, cesta)
    radky = cesta.read_text(encoding="utf-8-sig").splitlines()
    assert len(radky) == 3
