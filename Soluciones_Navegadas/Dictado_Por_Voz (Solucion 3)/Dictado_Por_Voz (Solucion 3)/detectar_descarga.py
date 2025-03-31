import os
import time
import re
import requests

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directorio de descargas
directorio_descargas = os.path.join(os.path.expanduser("~"), "Downloads")

# Expresión regular para el formato de nombre de archivo
nombre_archivo_regex = r'war_room_companion_\d{4}-\d{2}-\d{2}\.csv'

# URL del webhook de Slack
webhook_url = 'https://hooks.slack.com/services/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'

class DescargaHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            archivo = event.src_path
            if re.match(nombre_archivo_regex, os.path.basename(archivo)):
                nombres = extraer_nombres(archivo)
                enviar_a_slack(nombres)

def extraer_nombres(archivo):
    nombres = []
    with open(archivo, 'r', encoding='utf-8') as f:
        # Leer las líneas del archivo
        for linea in f:
            # Dividir la línea en partes utilizando la coma como separador
            partes = linea.strip().split(',')
            # Si hay al menos una parte y la primera no está vacía, agregarla a la lista de nombres
            if partes and partes[0]:
                nombres.append(partes[0])
    return nombres

def enviar_a_slack(nombres):
    payload = {'text': f'Nombres extraídos: {nombres}'}
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Nombres enviados exitosamente a Slack.")
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar nombres a Slack: {e}")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(DescargaHandler(), directorio_descargas, recursive=False)
    observer.start()
    print("Monitoreando el directorio de descargas...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()