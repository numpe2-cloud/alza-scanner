import pytest
from src.posouzeni_ceny import posouzeni_ceny


def test_cena_pod_minimem():
    # Arrange – připravím si vstupy
    aktualni_cena = 1000
    minimalni_cena = 1500
    # Act – zavolám testovanou funkci
    vysledek = posouzeni_ceny(aktualni_cena, minimalni_cena, prah=0.9)
    assert vysledek


def test_cena_nad_minimem():
    # Arrange – připravím si vstupy
    aktualni_cena = 1600
    minimalni_cena = 1500
    # Act – zavolám testovanou funkci
    vysledek = posouzeni_ceny(aktualni_cena, minimalni_cena, prah=0.9)
    assert not vysledek


def test_minimalni_cena_je_none():
    # Arrange – připravím si vstupy
    aktualni_cena = 1600
    minimalni_cena = None
    # Act – zavolám testovanou funkci
    vysledek = posouzeni_ceny(aktualni_cena, minimalni_cena, prah=0.9)
    assert not vysledek


def test_minimalni_cena_je_nula():
    # Arrange – připravím si vstupy
    aktualni_cena = 1600
    minimalni_cena = 0
    # Act – zavolám testovanou funkci
    vysledek = posouzeni_ceny(aktualni_cena, minimalni_cena, prah=0.9)
    assert not vysledek


def test_spatny_typ_ceny():
    with pytest.raises(TypeError):
        # Arrange – připravím si vstupy
        aktualni_cena = "abc"
        minimalni_cena = 1600
        # Act – zavolám testovanou funkci
        posouzeni_ceny(aktualni_cena, minimalni_cena, prah=0.9)
