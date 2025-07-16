# app/correo_reader.py
from imap_tools import MailBox, AND
import requests
from bs4 import BeautifulSoup
import os

EMAIL = os.getenv("CORREO_EMAIL")
PASSWORD = os.getenv("CORREO_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("TOKEN")

ASUNTO_CLAVE = "apartar sala"



def extraer_datos(texto_plano, html=None):
    if not texto_plano and html:
        # Convertimos HTML a texto legible
        soup = BeautifulSoup(html, "html.parser")
        texto_plano = soup.get_text()

    datos = {}
    for line in texto_plano.splitlines():
        if ':' in line:
            clave, valor = line.split(':', 1)
            datos[clave.strip().lower()] = valor.strip()

    hora_inicio, hora_fin = [h.strip() for h in datos['hora'].split('-')]
    return {
        "sala": datos['sala'],
        "fecha": datos['fecha'],
        "hora_inicio": hora_inicio + ":00",
        "hora_fin": hora_fin + ":00",
        "responsable": datos['responsable']
    }


def leer_y_enviar_correos():
    resultados = []
    with MailBox(IMAP_SERVER).login(EMAIL, PASSWORD) as mailbox:
        for msg in mailbox.fetch(AND(seen=False)):
            if ASUNTO_CLAVE in msg.subject.lower():
                try:
                    datos = extraer_datos(msg.text, msg.html)
                    response = requests.post(
                        API_URL,
                        json=datos,
                        headers={"Authorization": f"Bearer {API_TOKEN}"}
                    )
                    resultados.append({
                        "correo": msg.subject,
                        "estatus": response.status_code,
                        "respuesta": response.text
                    })
                    mailbox.flag(msg.uid, '\\Seen', True)
                except Exception as e:
                    resultados.append({
                        "correo": msg.subject,
                        "error": str(e)
                    })
    return resultados
