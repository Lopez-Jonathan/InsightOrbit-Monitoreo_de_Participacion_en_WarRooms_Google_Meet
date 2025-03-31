import schedule
import time
import subprocess

def start_program(program_path):
    try:
        subprocess.Popen(['python', program_path])
        print(f"Iniciando el programa {program_path}")
    except Exception as e:
        print(f"Error al iniciar el programa: {e}")

def stop_program(program_name):
    try:
        subprocess.run(['taskkill', '/IM', program_name, '/F'], check=True)
        print(f"Programa {program_name} detenido.")
    except subprocess.CalledProcessError as e:
        print(f"Error al detener el programa: {e}")

def start_at_specific_time(program_path, hour, minute):
    print(f"Iniciando el programa {program_path} a las {hour}:{minute}")
    schedule.every().day.at(f"{hour}:{minute}").do(start_program, program_path)

def stop_at_specific_time(program_name, hour, minute):
    print(f"Deteniendo el programa {program_name} a las {hour}:{minute}")
    schedule.every().day.at(f"{hour}:{minute}").do(stop_program, program_name)

# Definir la ruta del programa a ejecutar
program_path = "C:/Users/Voolkia/Documents/Python/Dictado por Voz/dictado2.py"
program_name = "python.exe"  # Nombre del proceso en Windows

# Programar el inicio del programa a las 16:00
start_at_specific_time(program_path, hour="16", minute="00")

# Programar la detención del programa a las 23:59
stop_at_specific_time(program_name, hour="23", minute="59")

while True:
    schedule.run_pending()
    time.sleep(10)  # Esperar 60 segundos antes de volver a verificar