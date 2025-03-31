import requests
import json
import time

from Optimized_2_Log_me_UC import main as run_main

def check_event():
    url = "https://sme-panic-button.adminml.com/get_incident"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            processed_events = set()  # Conjunto para almacenar los IDs de eventos procesados
            for event in data:
                incident_id = event.get('id', None)  # Obtenemos el ID del evento
                if incident_id and incident_id not in processed_events:  # Verificamos si el evento no ha sido procesado antes
                    processed_events.add(incident_id)  # Agregamos el ID del evento al conjunto de eventos procesados
                    incident = event.get('incident', {})
                    provider = incident.get('provider', False)
                    if not provider:
                        # Ejecutar el código anterior
                        run_main()

if __name__ == "__main__":
    while True:
        check_event()
        time.sleep(10)  # Espera 10 segundos antes de hacer otra solicitud