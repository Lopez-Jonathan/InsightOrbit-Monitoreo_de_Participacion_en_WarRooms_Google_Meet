#modulos de terceros
from selenium.webdriver.common.by import By #Para buscar por tipos de elementos
from selenium.webdriver.support.ui import WebDriverWait #Para esperar por elementos en selenium
from selenium.webdriver.support import expected_conditions as ec #Para condiciones en selenium
from selenium.webdriver.common.keys import Keys #Para pulsar teclas especiales (ej: AvPag, ENTER)
import time
import os
#Modulos Propios
from Log_me_Google_Chrome_UC.open_webdriver_uc import start_webdriver

# desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')
if __name__== '__main__':
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')
    #Declaramos variables
    email = "GMAIL"
    password = "PASSWORD"
    # email = "GMAIL"
    # password = "PASSWORD"
    # email = "GMAIL"
    # password = "PASSWORD"
    meeting_url = "URL_GOOGLE_MEET"
    #iniciamos webdriver
    driver = start_webdriver(headless=False,pos="maximizada")
    wait = WebDriverWait(driver,60)
    #cargamos la pagina de login de Google
    driver.get("https://accounts.google.com/")
    #introducimos el usuario
    e = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']")))
    e.send_keys(email)
    e.send_keys(Keys.ENTER)
    #introducimos contrasena
    e = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
    e.send_keys(password)
    e.send_keys(Keys.ENTER)
    driver.get(meeting_url)
    driver.refresh()
    time.sleep(2)
    e = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "button[jsname='Qx7uuf']")))
    e.click()
    time.sleep(2)
    #e = wait.until(ec.presence_of_all_element_located((By.CSS_SELECTOR, "button[jsname='A5il2e']")))
    e = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "button[jsname='A5il2e']")))
    if len(e)>=2:
        e[1].click()
    participants = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div[jsname='mu2b5d'] span")))
    participant_names = []
    for participant in participants:
        participant_names.append(participant.text)
    time.sleep(2)
    e = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "button[jsname='CQylAd']")))
    e.click()
    driver.quit()
    with open(file_path, 'w') as file:
        for participant in participant_names:
            file.write(participant + '\n')

with open('C:/Users/Voolkia/Desktop/integrantes_reunion.txt', 'r') as file:
    lines = file.readlines()

participants_cleaned = [line.strip() for line in lines if 'domain_disabled' not in line]

# Guardar los nombres limpios en un nuevo archivo
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

with open(os.path.join(desktop_path, 'integrantes_reunion_cleaned.txt'), 'w') as file:
    for participant in participants_cleaned:
        file.write(participant + '\n')
