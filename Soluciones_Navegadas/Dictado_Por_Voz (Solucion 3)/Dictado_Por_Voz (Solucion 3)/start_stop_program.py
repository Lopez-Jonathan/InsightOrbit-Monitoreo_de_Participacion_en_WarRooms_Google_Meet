import requests
import json
import time
import subprocess
from datetime import datetime

program_started = False  # Bandera para indicar si el programa ya se ha iniciado
incident_warning_shown = False  # Bandera para indicar si se ha mostrado la advertencia de incidente

def check_incidents_and_execute_program(program_path):
    global program_started, incident_warning_shown  # Acceder a las variables globales

    current_hour = datetime.now().hour
    if 16 <= current_hour <= 23:
        url = "https://sme-panic-button.adminml.com/get_incident"
        try:
            # Desactivar las advertencias de SSL
            requests.packages.urllib3.disable_warnings()
            # Realizar la solicitud sin verificar el certificado SSL
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                data = response.json()
                if data and not program_started:
                    print("Se ha detectado un incidente y nos encontramos entre las 16hs y las 23hs. Ejecutando el programa...")
                    execute_program(program_path, data)
                    program_started = True
                elif not data and program_started:
                    print("No se detectaron incidentes en la URL. Deteniendo el programa...")
                    stop_program(program_path)
                    program_started = False
                elif data and program_started:
                    if not incident_warning_shown:
                        print("Se ha detectado un incidente, pero el programa ya está en ejecución.")
                        incident_warning_shown = True
                else:
                    pass
            else:
                print("Error al obtener datos de la URL:", response.status_code)
        except requests.RequestException as e:
            print("Error al realizar la solicitud:", e)
    else:
        if program_started:
            print("La hora actual no está entre las 16hs y las 23hs. Deteniendo el programa...")
            stop_program(program_path)
            program_started = False
        else:
            print("La hora actual no está entre las 16hs y las 23hs. No se ejecutará el programa.")

def execute_program(program_path, data):
    try:
        subprocess.Popen(['python', program_path, json.dumps(data)])
        print(f"Iniciando el programa {program_path}")
    except Exception as e:
        print(f"Error al iniciar el programa: {e}")

def stop_program(program_path):
    try:
        subprocess.run(['taskkill', '/IM', 'python.exe', '/F'], check=True)
        print(f"Programa {program_path} detenido.")
    except subprocess.CalledProcessError as e:
        print(f"Error al detener el programa: {e}")

if __name__ == "__main__":
    # Definir la ruta del programa a ejecutar
    program_path = "C:/Users/Voolkia/Documents/Python/Dictado por Voz/dictado3.py"

    # Verificar incidentes y ejecutar el programa cada minuto
    while True:
        check_incidents_and_execute_program(program_path)
        time.sleep(60)  # Esperar 60 segundos antes de realizar la próxima verificación