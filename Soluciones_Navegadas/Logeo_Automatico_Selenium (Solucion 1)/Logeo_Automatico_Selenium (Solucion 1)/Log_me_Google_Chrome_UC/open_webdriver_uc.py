# import undetected_chromedriver as uc

# #Inicia un navegador de Chrome y devuelve el objeto Webdriver instanciado.
# #pos: indica la posicion del navegador en la pantalla ("maximizada","izquierda,"derecha").
# def start_webdriver(headless=False,pos="maximizada"):
    
#     #Instanciamos las opciones de Chrome
#     options = uc.ChromeOptions()
#     options.headless=False
#     options.add_argument("--disable-popup-blocking")
#     options.add_argument("--use-fake-ui-for-media-stream")
#     options.add_argument("--use-fake-device-for-media-stream")

#     #Desactivamos el guardado de credenciales
#     options.add_argument("--password-store=basic")
#     options.add_experimental_option(
#         "prefs",
#         {
#         "credentials_enable_service": False,
#         "profile.password_manager_enabled": False,
#         },
#     )

#     #iniciamos el driver
#     driver = uc.Chrome(
#         options=options,
#         headless=headless,
#         log_level=3,
#     )

#     #Posicionamos la ventana segun corresponda
#     if not headless:
#         #maximizamos la ventana
#         driver.maximize_window()
#         if pos != "maximizada":
#             #Obtenemos la resolucion de la ventana
#             size= driver.get_window_size()
#             ancho, alto = size["width"], size["height"]
#             if pos == "izquierda":
#                 #posicionamos la ventana en la mitad izquierda de la pantalla
#                 driver.set_window_rect(x=0, y=0, width=ancho/2, height=alto)
#             elif pos =="derecha":
#                 driver.set_window_rect(x=ancho//2, y=0, width=ancho/2, height=alto)
#     return driver

# import undetected_chromedriver as uc

# def start_webdriver(headless=False, pos="maximizada"):
#     #Instanciamos las opciones de Chrome
#     options = uc.ChromeOptions()
#     options.headless = headless
#     options.add_argument("--disable-popup-blocking")
#     options.add_argument("--use-fake-ui-for-media-stream")
#     options.add_argument("--use-fake-device-for-media-stream")
#     options.add_argument("--password-store=basic")
    
#     options.add_argument(r"--user-data-dir=C:\Users\Voolkia\AppData\Local\Google\Chrome\User Data\Profile 2")
#     options.add_argument('--profile-directory=Profile 2')

#     #Desactivamos el guardado de credenciales
#     prefs = {
#         "credentials_enable_service": False,
#         "profile.password_manager_enabled": False
#     }
#     options.add_experimental_option("prefs", prefs)

#     #Iniciamos el driver
#     driver = uc.Chrome(options=options, headless=headless, log_level=3)

#     #Posicionamos la ventana si no es headless
#     if not headless:
#         driver.maximize_window()
#         if pos != "maximizada":
#             size = driver.get_window_size()
#             ancho, alto = size["width"], size["height"]
#             if pos == "izquierda":
#                 driver.set_window_rect(x=0, y=0, width=ancho // 2, height=alto)
#             elif pos == "derecha":
#                 driver.set_window_rect(x=ancho // 2, y=0, width=ancho // 2, height=alto)
#     return driver


import undetected_chromedriver as uc

def start_webdriver(headless=False, pos="maximizada"):
    # Instanciamos las opciones de Chrome
    options = uc.ChromeOptions()
    options.headless = headless
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")
    options.add_argument("--password-store=basic")
    
    #options.add_argument("--user-data-dir=C:\\Users\\Voolkia\\AppData\\Local\\Google\\Chrome\\User Data")
    #options.add_argument('--profile-directory=Profile 2')

    # Desactivamos el guardado de credenciales
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    # Iniciamos el driver
    driver = uc.Chrome(options=options, headless=headless, log_level=3)
    # Posicionamos la ventana si no es headless
    if not headless:
        driver.maximize_window()
        if pos != "maximizada":
            size = driver.get_window_size()
            ancho, alto = size["width"], size["height"]
            if pos == "izquierda":
                driver.set_window_rect(x=0, y=0, width=ancho // 2, height=alto)
            elif pos == "derecha":
                driver.set_window_rect(x=ancho // 2, y=0, width=ancho // 2, height=alto)
    return driver
