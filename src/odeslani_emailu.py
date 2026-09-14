"""Skript, který zajistí odeslání emailu."""

import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

odesilatel = os.getenv("odesilatel")
heslo = os.getenv("heslo")
prijemce = os.getenv("prijemce")


def posli_email(nazev, cena, url):
    zprava = EmailMessage()
    zprava["Subject"] = f"{nazev} Nebezpečně nízká cena!!!"
    zprava["From"] = odesilatel
    zprava["To"] = prijemce
    zprava.set_content(f"Položka {nazev} aktuálně stojí {cena}. Klikni zde {url}")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(odesilatel, heslo)
        smtp.send_message(zprava)
