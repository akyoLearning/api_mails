from imap_tools import MailBox, AND
from bs4 import BeautifulSoup
import requests
import os

EMAIL = os.getenv("CORREO_EMAIL")
PASSWORD = os.getenv("CORREO_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("TOKEN")

ASUNTO_CLAVE = "apartar sala"

def extraer_datos(texto_plano, html=None):
    if not texto_plano and html:
        soup = BeautifulSoup(html, "html.parser")
        texto_plano = soup.get_text()

    print("📝 Texto extraído para análisis:")
    print(texto_plano)

    datos = {}
    for line in texto_plano.splitlines():
        if ':' in line:
            clave, valor = line.split(':', 1)
            datos[clave.strip().lower()] = valor.strip()

    if 'hora' not in datos or '-' not in datos['hora']:
        raise ValueError("Formato de hora inválido o faltante")

    hora_inicio, hora_fin = [h.strip() for h in datos['hora'].split('-')]
    return {
        "sala": datos.get('sala'),
        "fecha": datos.get('fecha'),
        "hora_inicio": hora_inicio + ":00",
        "hora_fin": hora_fin + ":00",
        "responsable": datos.get('responsable')
    }

def leer_y_enviar_correos():
    resultados = []
    print("📡 Iniciando conexión con IMAP...")
    with MailBox(IMAP_SERVER).login(EMAIL, PASSWORD) as mailbox:
        print("✅ Conexión IMAP exitosa")
        # Modo debug: leer todos los correos (incluso leídos)
        for msg in mailbox.fetch():
            print(f"📬 Revisión de correo: {msg.subject}")

            if ASUNTO_CLAVE in msg.subject.lower():
                print(f"✅ Coincidencia encontrada con asunto: {msg.subject}")
                try:
                    texto = msg.text or ""
                    html = msg.html or ""
                    datos = extraer_datos(texto, html)

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

                    # Marcar como leído
                    mailbox.flag(msg.uid, '\\Seen', True)
                except Exception as e:
                    print(f"❌ Error procesando correo: {e}")
                    resultados.append({
                        "correo": msg.subject,
                        "error": str(e)
                    })
            else:
                print("⏭️ Asunto ignorado")
    return resultados
