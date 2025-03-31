

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os

# Credenciales de la cuenta de Google
email = "GMAIL"
password = "PASSWORD"

# Ruta del archivo en el escritorio
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')

# URL de la reunión de Google Meet
meeting_url = "URL_GOOGLE_MEET"

# Configuración del navegador Microsoft Edge
edge_options = webdriver.EdgeOptions()
# edge_options.add_argument("--disable-infobars")
# edge_options.add_argument("--disable-extensions")
# edge_options.add_argument("--disable-popup-blocking")

# Inicializar el controlador web de Microsoft Edge
driver = webdriver.Edge(options=edge_options)

# Abrir la página de inicio de sesión de Google
driver.get("https://accounts.google.com/")
time.sleep(2)

# Ingresar correo electrónico
email_input = driver.find_element(By.XPATH, '//input[@name="identifier"]')
email_input.send_keys(email)
email_input.send_keys(Keys.ENTER)
time.sleep(60)

# Ingresar contraseña
password_input = driver.find_element_by_xpath("//input[@type='password']")
password_input.send_keys(password)
password_input.send_keys(Keys.ENTER)
time.sleep(2)

# Abrir la reunión de Google Meet
driver.get(meeting_url)

# Función para obtener los nombres de los participantes
def obtener_participantes(driver):
    # Esperar un tiempo para que carguen los participantes
    time.sleep(10)
    
    # Encontrar los elementos que contienen los nombres de los participantes
    participants = driver.find_elements_by_xpath("//div[@class='NlWrkb snByac']//span[@class='ZjFb7c']")
    
    # Lista para almacenar los nombres de los participantes
    participant_names = []
    
    # Obtener los nombres de los participantes y agregarlos a la lista
    for participant in participants:
        participant_names.append(participant.text)
    
    return participant_names

# Llamar a la función para obtener los nombres de los participantes
participants_list = obtener_participantes(driver)

# Cerrar el navegador
driver.quit()

# Escribir los nombres de los participantes en el archivo de texto
with open(file_path, 'w') as file:
    for participant in participants_list:
        file.write(participant + '\n')

print("Los nombres de los participantes se han guardado en el archivo:", file_path)
