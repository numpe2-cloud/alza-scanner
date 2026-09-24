import src.alerty as alerty


def test_novy_alert_se_zapise_po_odeslani(tmp_path, monkeypatch):
    cesta = tmp_path / "seznam_alertu.csv"
    monkeypatch.setattr(alerty, "posli_email", lambda nazev, cena, url, podezrela: True)
    alerty.kontrola_alertu("tv", 900, "https://example.com", cesta)
    assert "tv" in cesta.read_text(encoding="utf-8-sig")


def test_neodeslany_alert_se_nezapise(tmp_path, monkeypatch):
    cesta = tmp_path / "seznam_alertu.csv"
    monkeypatch.setattr(alerty, "posli_email", lambda nazev, cena, url, podezrela: False)
    alerty.kontrola_alertu("tv", 900, "https://example.com", cesta)
    assert "tv" not in cesta.read_text(encoding="utf-8-sig")


def test_podezrela_cena_posle_email_s_upozornenim(tmp_path, monkeypatch):
    cesta = tmp_path / "seznam_alertu.csv"
    odeslane = []
    monkeypatch.setattr(
        alerty, "posli_email",
        lambda nazev, cena, url, podezrela: odeslane.append(podezrela) or True
    )
    alerty.kontrola_alertu("tv", 100, "https://example.com", cesta, podezrela=True)
    assert odeslane == [True]
