# Modulos de terceros
from selenium.webdriver.common.by import By  # Para buscar por tipos de elementos
from selenium.webdriver.support.ui import WebDriverWait  # Para esperar por elementos en selenium
from selenium.webdriver.support import expected_conditions as ec  # Para condiciones en selenium
from selenium.webdriver.common.keys import Keys  # Para pulsar teclas especiales (ej: AvPag, ENTER)
import time
import os

# Modulos Propios
from Log_me_Google_Chrome_UC.open_webdriver_uc import start_webdriver

def main():
    # Definir ruta del archivo
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')

    # Declaramos variables
    email = "MAIL_GMAIL"
    password = "PASSWORD"
    meeting_url = "URL_GOOGLE_MEET"

    # Iniciamos webdriver
    driver = start_webdriver(headless=False, pos="maximizada")
    wait = WebDriverWait(driver, 60)

    # Cargamos la página de login de Google
    driver.get("https://accounts.google.com/")

    # Introducimos el usuario
    e = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']")))
    e.send_keys(email)
    e.send_keys(Keys.ENTER)

    # Introducimos contraseña
    e = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
    e.send_keys(password)
    e.send_keys(Keys.ENTER)

    # Navegamos a la URL de la reunión
    driver.get(meeting_url)
    driver.refresh()
    time.sleep(2)

    e = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "button[jsname='Qx7uuf']")))
    e.click()
    time.sleep(2)

    # Click en el botón "Ver todos"
    e = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "button[jsname='A5il2e']")))
    if len(e) >= 2:
        e[1].click()

    # Obtener nombres de participantes
    participants = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div[jsname='mu2b5d'] span")))
    participant_names = [participant.text for participant in participants]

    # Cerrar la ventana de participantes
    time.sleep(2)
    e = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "button[jsname='CQylAd']")))
    e.click()

    # Escribir nombres de participantes en el archivo (sobrescribir)
    with open(file_path, 'a') as file:
        file.write('\n') 
        for participant in participant_names:
            if 'domain_disabled' not in participant:
                file.write(participant + '\n')

if __name__ == '__main__':
    main()
