from src.historie_cen import najdi_minimum
from datetime import datetime, timedelta


def test_najdi_minimum_zaklad(tmp_path):
    # Arrange – připravím si vstupy
    datum_pred_10_dny = datetime.now() - timedelta(days=10)
    datum_text = datum_pred_10_dny.strftime("%Y-%m-%d")
    obsah_csv = "nazev,datum,cena\n" \
                f"tv,{datum_text},1000\n" \
                f"tv,{datum_text},800\n" \
                f"tv,{datum_text},1200\n"
    cesta = tmp_path / "test.csv"
    cesta.write_text(obsah_csv)
    nazev_produktu = "tv"
    # Act – zavolám testovanou funkci
    vysledek = najdi_minimum(nazev_produktu, cesta)
    assert vysledek == 800


def test_najdi_minimum_stara_cena(tmp_path):
    # Arrange – připravím si vstupy
    datum_pred_10_dny = datetime.now() - timedelta(days=10)
    datum_pred_200dny = datetime.now() - timedelta(days=200)
    datum_text = datum_pred_10_dny.strftime("%Y-%m-%d")
    datum_stary = datum_pred_200dny.strftime("%Y-%m-%d")
    obsah_csv = "nazev,datum,cena\n" \
                f"tv,{datum_text},1000\n" \
                f"tv,{datum_text},800\n" \
                f"tv,{datum_text},1200\n"\
                f"tv,{datum_stary},100\n"
    cesta = tmp_path / "test.csv"
    cesta.write_text(obsah_csv)
    nazev_produktu = "tv"
    # Act – zavolám testovanou funkci
    vysledek = najdi_minimum(nazev_produktu, cesta)
    assert vysledek == 800


def test_najdi_minimum_chybejici_produkt(tmp_path):
    # Arrange – připravím si vstupy
    datum_pred_10_dny = datetime.now() - timedelta(days=10)
    datum_text = datum_pred_10_dny.strftime("%Y-%m-%d")
    obsah_csv = "nazev,datum,cena\n" \
                f"lednice,{datum_text},1200\n"\
                f"lednice,{datum_text},800\n" \
                f"lednice,{datum_text},1200\n"\
                f"lednice,{datum_text},100\n"
    cesta = tmp_path / "test.csv"
    cesta.write_text(obsah_csv)
    nazev_produktu = "tv"
    # Act – zavolám testovanou funkci
    vysledek = najdi_minimum(nazev_produktu, cesta)
    assert vysledek is None


def test_soubor_neexistuje(tmp_path):
    cesta = tmp_path / "monitoringcen.csv"
    vysledek = najdi_minimum("Nintendo", cesta)
    assert vysledek is None


def test_radek_bez_ceny_se_preskoci(tmp_path):
    datum_text = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
    obsah_csv = "datum,nazev,cena\n" \
                f"{datum_text},tv,1000\n" \
                f"{datum_text},tv,\n"
    cesta = tmp_path / "test.csv"
    cesta.write_text(obsah_csv, encoding="utf-8")
    assert najdi_minimum("tv", cesta) == 1000
