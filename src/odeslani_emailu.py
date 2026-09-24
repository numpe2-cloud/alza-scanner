"""Skript, který zajistí odeslání emailu."""

import logging
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

HOST = "smtp.gmail.com"
PORT = 465

odesilatel = os.getenv("odesilatel")
heslo = os.getenv("heslo")
prijemce = os.getenv("prijemce")


def posli_email(nazev, cena, url, podezrela=False):
    zprava = EmailMessage()
    text = f"Položka {nazev} aktuálně stojí {cena}. Klikni zde {url}"
    if podezrela:
        zprava["Subject"] = f"{nazev} Extrémně nízká cena - ověř!!!"
        text += (
            "\nCena je o víc než 70 % pod minimem. "
            "Může to být chyba v ceně na webu, nebo chyba scrapování."
        )
    else:
        zprava["Subject"] = f"{nazev} Nebezpečně nízká cena!!!"
    zprava["From"] = odesilatel
    zprava["To"] = prijemce
    zprava.set_content(text)
    try:
        with smtplib.SMTP_SSL(HOST, PORT) as smtp:
            smtp.login(odesilatel, heslo)
            smtp.send_message(zprava)
        return True
    except (smtplib.SMTPException, OSError) as e:
        logging.error(f"Email se neposlal! Protože {e}")
        return False
