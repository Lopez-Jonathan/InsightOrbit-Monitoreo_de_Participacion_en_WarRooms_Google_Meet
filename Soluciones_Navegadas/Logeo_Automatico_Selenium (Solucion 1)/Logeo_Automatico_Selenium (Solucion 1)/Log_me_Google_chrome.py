# from selenium import webdriver
# import time
# import os

# # Ruta del archivo en el escritorio
# desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')

# # URL de la reunión de Google Meet
# meeting_url = "URL_GOOGLE_MEET"

# # Función para obtener los nombres de los participantes
# def obtener_participantes(driver):
#     # Esperar un tiempo para que carguen los participantes
#     time.sleep(10)
    
#     # Encontrar los elementos que contienen los nombres de los participantes
#     participants = driver.find_elements_by_xpath("//div[@class='NlWrkb snByac']//span[@class='ZjFb7c']")
    
#     # Lista para almacenar los nombres de los participantes
#     participant_names = []
    
#     # Obtener los nombres de los participantes y agregarlos a la lista
#     for participant in participants:
#         participant_names.append(participant.text)
    
#     return participant_names

# # Configuración del navegador Chrome
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-popup-blocking")

# # Iniciar el navegador Chrome
# driver = webdriver.Chrome(executable_path='./chromedriver')

# # Abrir la reunión de Google Meet
# driver.get(meeting_url)

# # Llamar a la función para obtener los nombres de los participantes
# participants_list = obtener_participantes(driver)

# # Cerrar el navegador
# driver.quit()

# # Escribir los nombres de los participantes en el archivo de texto
# with open(file_path, 'w') as file:
#     for participant in participants_list:
#         file.write(participant + '\n')

# print("Los nombres de los participantes se han guardado en el archivo:", file_path)

# from selenium import webdriver
# import time
# import os

# # Ruta del archivo en el escritorio
# desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')

# # URL de la reunión de Google Meet
# meeting_url = "URL_GOOGLE_MEET"

# # Configuración del navegador Chrome
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-popup-blocking")

# # Iniciar el navegador Chrome
# driver = webdriver.Chrome(options=chrome_options)

# # Abrir la reunión de Google Meet
# driver.get(meeting_url)

# # Función para obtener los nombres de los participantes
# def obtener_participantes(driver):
#     # Esperar un tiempo para que carguen los participantes
#     time.sleep(10)
    
#     # Encontrar los elementos que contienen los nombres de los participantes
#     participants = driver.find_elements_by_xpath("//div[@class='NlWrkb snByac']//span[@class='ZjFb7c']")
    
#     # Lista para almacenar los nombres de los participantes
#     participant_names = []
    
#     # Obtener los nombres de los participantes y agregarlos a la lista
#     for participant in participants:
#         participant_names.append(participant.text)
    
#     return participant_names

# # Llamar a la función para obtener los nombres de los participantes
# participants_list = obtener_participantes(driver)

# # Cerrar el navegador
# driver.quit()

# # Escribir los nombres de los participantes en el archivo de texto
# with open(file_path, 'w') as file:
#     for participant in participants_list:
#         file.write(participant + '\n')

# print("Los nombres de los participantes se han guardado en el archivo:", file_path)

# from selenium import webdriver
# import time
# import os

# # Ruta del archivo en el escritorio
# desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')

# # URL de la reunión de Google Meet
# meeting_url = "URL_GOOGLE_MEET"

# # Configuración del navegador Chrome
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-popup-blocking")

# # Iniciar el navegador Chrome
# driver = webdriver.Chrome(options=chrome_options)

# # Abrir la reunión de Google Meet
# driver.get(meeting_url)

# # Función para obtener los nombres de los participantes
# def obtener_participantes(driver):
#     # Esperar un tiempo para que carguen los participantes
#     time.sleep(10)
    
#     # Encontrar los elementos que contienen los nombres de los participantes
#     participants = driver.find_elements_by_xpath("//div[@class='NlWrkb snByac']//span[@class='ZjFb7c']")
    
#     # Lista para almacenar los nombres de los participantes
#     participant_names = []
    
#     # Obtener los nombres de los participantes y agregarlos a la lista
#     for participant in participants:
#         participant_names.append(participant.text)
    
#     return participant_names

# # Llamar a la función para obtener los nombres de los participantes
# participants_list = obtener_participantes(driver)

# # Cerrar el navegador
# driver.quit()

# # Escribir los nombres de los participantes en el archivo de texto
# with open(file_path, 'w') as file:
#     for participant in participants_list:
#         file.write(participant + '\n')

# print("Los nombres de los participantes se han guardado en el archivo:", file_path)

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# import os

# # Credenciales de la cuenta de Google
# email = "GMAIL"  # Reemplaza con tu dirección de correo electrónico
# password = "PASSWORD"     # Reemplaza con tu contraseña

# # Ruta del archivo en el escritorio
# desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')

# # URL de la reunión de Google Meet
# meeting_url = "URL_GOOGLE_MEET"

# # Configuración del navegador Chrome
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-popup-blocking")

# # Iniciar el navegador Chrome
# driver = webdriver.Chrome(options=chrome_options)

# # Abrir la página de inicio de sesión de Google
# driver.get("https://accounts.google.com/")
# time.sleep(2)

# # Ingresar correo electrónico
# email_input = driver.find_element_by_xpath("//input[@type='email']")
# email_input.send_keys(email)
# email_input.send_keys(Keys.ENTER)
# time.sleep(2)

# # Ingresar contraseña
# password_input = driver.find_element_by_xpath("//input[@type='password']")
# password_input.send_keys(password)
# password_input.send_keys(Keys.ENTER)
# time.sleep(2)

# # Abrir la reunión de Google Meet
# driver.get(meeting_url)

# # Función para obtener los nombres de los participantes
# def obtener_participantes(driver):
#     # Esperar un tiempo para que carguen los participantes
#     time.sleep(10)
    
#     # Encontrar los elementos que contienen los nombres de los participantes
#     participants = driver.find_elements_by_xpath("//div[@class='NlWrkb snByac']//span[@class='ZjFb7c']")
    
#     # Lista para almacenar los nombres de los participantes
#     participant_names = []
    
#     # Obtener los nombres de los participantes y agregarlos a la lista
#     for participant in participants:
#         participant_names.append(participant.text)
    
#     return participant_names

# # Llamar a la función para obtener los nombres de los participantes
# participants_list = obtener_participantes(driver)

# # Cerrar el navegador
# driver.quit()

# # Escribir los nombres de los participantes en el archivo de texto
# with open(file_path, 'w') as file:
#     for participant in participants_list:
#         file.write(participant + '\n')

# print("Los nombres de los participantes se han guardado en el archivo:", file_path)

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# import os

# # Credenciales de la cuenta de Google
# email = "tu_email@gmail.com"  # Reemplaza con tu dirección de correo electrónico
# password = "tu_contraseña"     # Reemplaza con tu contraseña

# # Ruta del archivo en el escritorio
# desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')

# # URL de la reunión de Google Meet
# meeting_url = "URL_DE_LA_REUNION"

# # Configuración del navegador Chrome
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-popup-blocking")

# # Iniciar el navegador Chrome
# driver = webdriver.Chrome(options=chrome_options)

# # Abrir la página de inicio de sesión de Google
# driver.get("https://accounts.google.com/")
# time.sleep(2)

# # Ingresar correo electrónico
# email_input = driver.find_element_by_name("identifier")
# email_input.send_keys(email)
# email_input.send_keys(Keys.ENTER)
# time.sleep(2)

# # Ingresar contraseña
# password_input = driver.find_element_by_name("password")
# password_input.send_keys(password)
# password_input.send_keys(Keys.ENTER)
# time.sleep(2)

# # Abrir la reunión de Google Meet
# driver.get(meeting_url)

# # Función para obtener los nombres de los participantes
# def obtener_participantes(driver):
#     # Esperar un tiempo para que carguen los participantes
#     time.sleep(10)
    
#     # Encontrar los elementos que contienen los nombres de los participantes
#     participants = driver.find_elements_by_xpath("//div[@class='NlWrkb snByac']//span[@class='ZjFb7c']")
    
#     # Lista para almacenar los nombres de los participantes
#     participant_names = []
    
#     # Obtener los nombres de los participantes y agregarlos a la lista
#     for participant in participants:
#         participant_names.append(participant.text)
    
#     return participant_names

# # Llamar a la función para obtener los nombres de los participantes
# participants_list = obtener_participantes(driver)

# # Cerrar el navegador
# driver.quit()

# # Escribir los nombres de los participantes en el archivo de texto
# with open(file_path, 'w') as file:
#     for participant in participants_list:
#         file.write(participant + '\n')

# print("Los nombres de los participantes se han guardado en el archivo:", file_path)

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# import os

# # Credenciales de la cuenta de Google
# email = "GMAIL"  # Reemplaza con tu dirección de correo electrónico
# password = "PASSWORD"     # Reemplaza con tu contraseña

# # Ruta del archivo en el escritorio
# desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')

# # URL de la reunión de Google Meet
# meeting_url = "URL_GOOGLE_MEET"

# # Configuración del navegador Chrome
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-popup-blocking")

# # Iniciar el navegador Chrome
# driver = webdriver.Chrome(options=chrome_options)

# # Abrir la página de inicio de sesión de Google
# driver.get("https://accounts.google.com/")
# time.sleep(2)

# # Ingresar correo electrónico
# email_input = driver.find_element_by_css_selector("input[type='email']")
# email_input.send_keys(email)
# email_input.send_keys(Keys.ENTER)
# time.sleep(2)

# # Ingresar contraseña
# password_input = driver.find_element_by_css_selector("input[type='password']")
# password_input.send_keys(password)
# password_input.send_keys(Keys.ENTER)
# time.sleep(2)

# # Abrir la reunión de Google Meet
# driver.get(meeting_url)

# # Función para obtener los nombres de los participantes
# def obtener_participantes(driver):
#     # Esperar un tiempo para que carguen los participantes
#     time.sleep(10)
    
#     # Encontrar los elementos que contienen los nombres de los participantes
#     participants = driver.find_elements_by_xpath("//div[@class='NlWrkb snByac']//span[@class='ZjFb7c']")
    
#     # Lista para almacenar los nombres de los participantes
#     participant_names = []
    
#     # Obtener los nombres de los participantes y agregarlos a la lista
#     for participant in participants:
#         participant_names.append(participant.text)
    
#     return participant_names

# # Llamar a la función para obtener los nombres de los participantes
# participants_list = obtener_participantes(driver)

# # Cerrar el navegador
# driver.quit()

# # Escribir los nombres de los participantes en el archivo de texto
# with open(file_path, 'w') as file:
#     for participant in participants_list:
#         file.write(participant + '\n')

# print("Los nombres de los participantes se han guardado en el archivo:", file_path)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.options import Options
import time
import os


# Credenciales de la cuenta de Google
email = "GMAIL"  # Reemplaza con tu dirección de correo electrónico
password = "PASSWORD"     # Reemplaza con tu contraseña

# Ruta del archivo en el escritorio
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')

# URL de la reunión de Google Meet
meeting_url = "URL_GOOGLE_MEET"

# Configuración del navegador Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")

# Inicializar el controlador web Chrome
driver = webdriver.Chrome(options=chrome_options)

# Abrir la página de inicio de sesión de Google
driver.get("https://accounts.google.com/")
time.sleep(2)

# Ingresar correo electrónico
# email_input = driver.find_element_by_name("identifier")
email_input = driver.find_element(By.XPATH, '//input[@name="identifier"]')
email_input.send_keys(email)
email_input.send_keys(Keys.ENTER)
time.sleep(2)

# Ingresar contraseña
#password_input = driver.find_element_by_name("password")
password_input = driver.find_element(By.XPATH, '//input[@name="Passwd"]')
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
