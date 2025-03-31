# # Modulos de terceros
# from selenium.webdriver.common.by import By  # Para buscar por tipos de elementos
# from selenium.webdriver.support.ui import WebDriverWait  # Para esperar por elementos en selenium
# from selenium.webdriver.support import expected_conditions as ec  # Para condiciones en selenium
# from selenium.webdriver.common.keys import Keys  # Para pulsar teclas especiales (ej: AvPag, ENTER)
# from selenium.common.exceptions import TimeoutException  # Para manejar excepciones de tiempo de espera
# import time
# import os

# # Modulos Propios
# from Log_me_Google_Chrome_UC.open_webdriver_uc import start_webdriver

# def main():
#     try:
#         # Iniciar webdriver
#         driver = start_webdriver(headless=False, pos="maximizada")
#         wait = WebDriverWait(driver, 60)

#         # Cargar la página de inicio de sesión de Google
#         driver.get("https://accounts.google.com/")

#         # Introducir el usuario
#         email_input = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']")))
#         email_input.send_keys(email)
#         email_input.send_keys(Keys.ENTER)

#         # Introducir la contraseña
#         password_input = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
#         password_input.send_keys(password)
#         password_input.send_keys(Keys.ENTER)

#         # Navegar a la URL de la reunión
#         driver.get(meeting_url)

#         #Es necesario refrescar para que tome la cuenta de google
#         driver.refresh()

#         #time.sleep necesario para permitir cargar el Button
#         time.sleep(2)

#         #Se inabilita el microfono
#         # e = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div[jsname='BOHaEe']")))
#         # e.click()

#         e = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div[jsname='BOHaEe']")))
#         if len(e) >= 2:
#             for button in e[:2]:
#                 button.click()
#         #Se clickea el Button "Unirse Ahora"
#         e = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "button[jsname='Qx7uuf']")))
#         e.click()

#         #Se espera hasta que aparezca el boton "Mostrar a todos"
#         view_all_button = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "button[jsname='A5il2e']")))
#         if len(view_all_button) >= 2:
#             view_all_button[1].click()

#         #Se localiza todos los div que contienen un span con el nombre de los integrantes y se almacena
#         participants = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div[jsname='mu2b5d'] span")))

#         #Se recorre lo almacenado con un for para almacenarlo pero esta vez en un diccionario
#         participant_names = [participant.text for participant in participants]

#         #Clickea el boton para salir de la llamada
#         close_button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname='CQylAd']")))
#         close_button.click()

#         # Escribir nombres de participantes en el archivo, continua la escritura sin sobreescribir, dejando dos renglones vacios.
#         with open(file_path, 'a') as file:
#             file.write('\n\n')  # Agregar dos líneas vacías antes de escribir los nuevos nombres
#             for participant in participant_names:
#                 if 'domain_disabled' not in participant:
#                     file.write(participant + '\n')
#     #Excepciones en caso de que algun objeto no cargue en el tiempo correspondientes o por alguna falla.
#     except TimeoutException:
#         print("Tiempo de espera excedido.")
#     except Exception as e:
#         print(f"Ocurrió un error inesperado: {e}")
#     finally:
#         driver.quit()

# if __name__ == '__main__':
#     # Definir ruta del archivo y creacion
#     desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
#     file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')

#     # Declaramos variables
#     email = "totitolopjona@gmail.com"
#     password = "Cabezon123"
#     meeting_url = "https://meet.google.com/wrw-avxj-qst?authuser=0"


# # Modulos de terceros
# from selenium.webdriver.common.by import By  # Para buscar por tipos de elementos
# from selenium.webdriver.support.ui import WebDriverWait  # Para esperar por elementos en selenium
# from selenium.webdriver.support import expected_conditions as ec  # Para condiciones en selenium
# from selenium.webdriver.common.keys import Keys  # Para pulsar teclas especiales (ej: AvPag, ENTER)
# from selenium.common.exceptions import TimeoutException  # Para manejar excepciones de tiempo de espera
# import os
# import time
# # Modulos Propios
# from Log_me_Google_Chrome_UC.open_webdriver_uc import start_webdriver

# def main():
#     # Declaramos variables
#     email = "totitolopjona@gmail.com"
#     password = "Cabezon123"
#     meeting_url = "https://meet.google.com/bwi-jxzh-jax"
#     name="Bot"
    
#     try:
    
#         # Iniciar webdriver
#         driver = start_webdriver(headless=False, pos="maximizada")
#         wait = WebDriverWait(driver, 60)

#         # # Cargar la página de inicio de sesión de Google
#         driver.get("https://accounts.google.com/")

#         #Introducir el usuario
#         email_input = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']")))
#         email_input.send_keys(email)
#         email_input.send_keys(Keys.ENTER)

#         # Introducir la contraseña
#         password_input = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
#         password_input.send_keys(password)
#         password_input.send_keys(Keys.ENTER)
    
#         # Navegar a la URL de la reunión
#         driver.get(meeting_url)

#         #Es necesario refrescar para que tome la cuenta de google
#         driver.refresh()
#         #time.sleep necesario para permitir cargar el Button
#         time.sleep(2)

#         #Se inabilita el microfono
#         e = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div[jsname='BOHaEe']")))
#         if len(e) >= 2:
#             for button in e[:2]:
#                 button.click()
        
#         #Se clickea el Button "Unirse Ahora"
#         e = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "button[jsname='Qx7uuf']")))
#         e.click()

#         #Se espera hasta que aparezca el boton "Mostrar a todos"
#         view_all_button = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "button[jsname='A5il2e']")))
#         if len(view_all_button) >= 2:
#             view_all_button[1].click()

#         #Se localiza todos los div que contienen un span con el nombre de los integrantes y se almacena
#         participants = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div[jsname='mu2b5d'] span")))

#         #Se recorre lo almacenado con un for para almacenarlo pero esta vez en un diccionario
#         participant_names = [participant.text for participant in participants]

#         #Clickea el boton para salir de la llamada
#         close_button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname='CQylAd']")))
#         close_button.click()

#         # Escribir nombres de participantes en el archivo, continua la escritura sin sobreescribir, dejando dos renglones vacios.
#         desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
#         file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')

#         with open(file_path, 'a') as file:
#             file.write('\n\n')  # Agregar dos líneas vacías antes de escribir los nuevos nombres
#             for participant in participant_names:
#                 if 'domain_disabled' not in participant:
#                     file.write(participant + '\n')

#     #Excepciones en caso de que algun objeto no cargue en el tiempo correspondientes o por alguna falla.
#     except TimeoutException:
#         print("Tiempo de espera excedido.")
#     except Exception as e:
#         print(f"Ocurrió un error inesperado: {e}")
#     finally:
#         try:
#             driver.quit()
#         except Exception as e:
#             print("Error al cerrar el navegador:", e)
# if __name__ == '__main__':
#     main()

# import os
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import TimeoutException
# from Log_me_Google_Chrome_UC.open_webdriver_uc import start_webdriver

# def main():
#     # Declaramos variables
#     email = "totitolopjona@gmail.com"
#     password = "Cabezon123"
#     meeting_url = "https://meet.google.com/ibr-mzmi-bzs"
#     name = "Jonathan Lopez"

#     try:

#         # Iniciar webdriver
#         driver = start_webdriver(headless=False, pos="maximizada")
#         wait = WebDriverWait(driver, 60)

#         # Cargar la página de inicio de sesión de Google
#         driver.get("https://accounts.google.com/")

#         # Introducir el usuario
#         email_input = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']")))
#         email_input.send_keys(email)
#         email_input.send_keys(Keys.ENTER)

#         # Introducir la contraseña
#         password_input = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
#         password_input.send_keys(password)
#         password_input.send_keys(Keys.ENTER)

#         # Navegar a la URL de la reunión
#         driver.get(meeting_url)

#         # Es necesario refrescar para que tome la cuenta de google
#         driver.refresh()
#         # time.sleep necesario para permitir cargar el Button
#         time.sleep(2)

#         # Se inabilita el microfono
#         e = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div[jsname='BOHaEe']")))
#         if len(e) >= 2:
#             for button in e[:2]:
#                 button.click()

#         # Se clickea el Button "Unirse Ahora"
#         e = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "button[jsname='Qx7uuf']")))
#         e.click()

#         # Se espera hasta que aparezca el boton "Mostrar a todos"
#         view_all_button = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "button[jsname='A5il2e']")))
#         if len(view_all_button) >= 2:
#             view_all_button[1].click()

#         # Se localiza todos los div que contienen un span con el nombre de los integrantes y se almacena
#         participants = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div[jsname='mu2b5d'] span")))

#         # Esperar 5 minutos antes de verificar si el bot es el único participante
#         time.sleep(120)

#         # Verificar si el bot es el único participante presente
#         if len(participants) == 1 and participants[0].text == name:
#             # Si el bot es el único participante, hacer clic en el botón para salir de la llamada
#             close_button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname='CQylAd']")))
#             close_button.click()

#         # Escribir nombres de participantes en el archivo, continua la escritura sin sobreescribir, dejando dos renglones vacios.
#         desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
#         file_path = os.path.join(desktop_path, 'integrantes_reunion.txt')

#         with open(file_path, 'a') as file:
#             file.write('\n\n')  # Agregar dos líneas vacías antes de escribir los nuevos nombres
#             for participant in participants:
#                 if 'domain_disabled' not in participant.text:
#                     file.write(participant.text + '\n')

#     # Excepciones en caso de que algun objeto no cargue en el tiempo correspondientes o por alguna falla.
#     except TimeoutException:
#         print("Tiempo de espera excedido.")
#     except Exception as e:
#         print(f"Ocurrió un error inesperado: {e}")
#     finally:
#         try:
#             driver.quit()
#         except Exception as e:
#             print("Error al cerrar el navegador:", e)

# if __name__ == '__main__':
#     main()

import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from Log_me_Google_Chrome_UC.open_webdriver_uc import start_webdriver

def main():
    # Declaramos variables
    email = "totitolopjona@gmail.com"
    password = "Cabezon123"
    meeting_url = "https://meet.google.com/xcj-jkyn-aur?authuser=1"
    name = "Jonathan Lopez"

    try:
        # Iniciar webdriver
        driver = start_webdriver(headless=False, pos="maximizada")
        wait = WebDriverWait(driver, 60)

        # Cargar la página de inicio de sesión de Google
        driver.get("https://accounts.google.com/")

        # Introducir el usuario
        email_input = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']")))
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)

        # Introducir la contraseña
        password_input = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        # Navegar a la URL de la reunión
        driver.get(meeting_url)

        # Es necesario refrescar para que tome la cuenta de google
        driver.refresh()
        # time.sleep necesario para permitir cargar el Button
        time.sleep(2)

        # Se inabilita el micrófono\camara
        e = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div[jsname='BOHaEe']")))
        if len(e) >= 2:
            for button in e[:2]:
                button.click()

        #Se clickea el Button "Unirse Ahora"
        e = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "button[jsname='Qx7uuf']")))
        e.click()

        #Se espera hasta que aparezca el boton "Mostrar a todos"
        view_all_button = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "button[jsname='A5il2e']")))
        if len(view_all_button) >= 2:
             view_all_button[1].click()

        participants = set()  # Set para almacenar los nombres de los participantes
        while True:
            # Se localiza todos los div que contienen un span con el nombre de los integrantes y se almacena
            all_participants_elements = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div[jsname='mu2b5d']")))
            participants_elements = [element for element in all_participants_elements if '(Tú)' not in element.text]
            current_participants = {participant.text for participant in participants_elements}

            # Verificar si hay nuevos participantes
            new_participants = current_participants - participants
            if new_participants:
                participants.update(new_participants)

                # Escribir nuevos participantes en el archivo
                desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                file_path = os.path.join(desktop_path, 'Integrantes_reunion.txt')
                with open(file_path, 'a') as file:
                    for participant in new_participants:
                        file.write(participant + '\n')

            # Verificar si solo queda el bot para que salga de la videollamada
            if len(all_participants_elements) == 1:
                break  # Salir del bucle si solo queda el bot

            # Esperar antes de volver a verificar
            time.sleep(30)


        # Salir de la llamada
        e = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname='CQylAd']")))
        e.click()

    except TimeoutException:
        print("Tiempo de espera excedido.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        try:
            driver.quit()  # Usa quit() 
        except Exception as e:
            print("Error al cerrar el navegador:", e)

if __name__ == '__main__':
    main()