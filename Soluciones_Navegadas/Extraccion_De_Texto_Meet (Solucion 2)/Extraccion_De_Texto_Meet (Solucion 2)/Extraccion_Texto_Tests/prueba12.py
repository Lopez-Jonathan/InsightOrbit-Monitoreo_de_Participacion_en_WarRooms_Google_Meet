import re
import nltk
from collections import defaultdict
import cv2
import pytesseract
import spacy
import Levenshtein as lev

# Descargar los recursos necesarios de NLTK
nltk.download('punkt')

# Cargar el modelo de lenguaje de spaCy para NER
nlp = spacy.load("es_core_news_sm")

# Ruta del video
video_path = 'prueba4.mp4'

# Coordenadas de la región de interés (ROI)
x1, y1 = 1444, 647  # Coordenadas de la esquina superior izquierda
x2, y2 = 2000, 672  # Coordenadas de la esquina inferior derecha

# Diccionario para almacenar los nombres extraídos y su conteo
nombres_contador = defaultdict(int)

# Crear un objeto VideoCapture
cap = cv2.VideoCapture(video_path)

# Obtener la frecuencia de cuadros por segundo (fps)
fps = cap.get(cv2.CAP_PROP_FPS)

# Establecer el tiempo inicial en 0
tiempo_actual = 0

def limpiar_texto(texto):
    # Eliminar caracteres especiales utilizando expresiones regulares
    texto_limpio = re.sub(r'[^\w\s]', '', texto)
    return texto_limpio

def hay_texto(gray_frame):
    # Aplicar umbral para binarizar la imagen
    _, thresh = cv2.threshold(gray_frame, 200, 255, cv2.THRESH_BINARY)
    # Contar los píxeles no negros (blancos)
    num_white_pixels = cv2.countNonZero(thresh)
    # Si hay una cantidad significativa de píxeles blancos, asumimos que hay texto
    return num_white_pixels > 50

def eliminar_repeticiones_finales(nombre):
    partes = nombre.split()
    for i in range(len(partes) - 1):
        subcadena = ' '.join(partes[i:])
        if nombre.endswith(subcadena) and ' '.join(partes[:i]).find(subcadena) != -1:
            return ' '.join(partes[:i])
    return nombre

# Bucle para capturar y procesar cada fotograma
while True:
    # Avanzar al siguiente fotograma
    cap.set(cv2.CAP_PROP_POS_MSEC, tiempo_actual * 1000)
    ret, frame = cap.read()

    # Verificar si se pudo leer el fotograma
    if ret:
        # Leer la región de interés (ROI)
        roi = frame[y1:y2, x1:x2]

        # Convertir el fotograma a escala de grises
        gray_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Verificar si hay texto en la región de interés
        if hay_texto(gray_frame):
            # Aplicar umbral para resaltar los píxeles más blancos
            _, thresh = cv2.threshold(gray_frame, 200, 300, cv2.THRESH_BINARY)
            # Opcional: aplicar dilatación para mejorar la detección de texto
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,1))
            dilated = cv2.dilate(thresh, kernel, iterations=1)

            # Utilizar OCR para extraer el texto del fotograma completo
            texto_completo = pytesseract.image_to_string(dilated, lang='spa', config='--psm 7')

            # Limpiar el texto extraído de caracteres especiales
            texto_limpo = limpiar_texto(texto_completo)

            # Tokenizar el texto limpio
            lineas_tokenizadas = [nltk.word_tokenize(linea) for linea in texto_limpo.split('\n')]

            # Aplicar el modelo de spaCy NER a cada línea tokenizada
            for tokens in lineas_tokenizadas:
                linea = ' '.join(tokens)  # Convertir tokens de vuelta a texto
                doc = nlp(linea)
                for ent in doc.ents:
                    if ent.label_ == "PER":  # Filtrar solo entidades que sean nombres de personas
                        nombre = ent.text.strip()  # Eliminar espacios en blanco alrededor
                        if nombre:
                            nombre_limpio = eliminar_repeticiones_finales(nombre)  # Eliminar repeticiones finales
                            nombres_contador[nombre_limpio] += 1
            
            # Mostrar el fotograma actual
            cv2.imshow('ROI', dilated)
            print(f"Fotograma en tiempo {tiempo_actual / fps:.2f} segundos procesado.")

    # Aumentar el tiempo actual en 3 segundos (3000 ms)
    tiempo_actual += 1 * fps  # Multiplicar por fps para obtener el número de fotogramas en 3 segundos

    # Verificar si se alcanzó el final del video
    if tiempo_actual >= cap.get(cv2.CAP_PROP_FRAME_COUNT):
        break
    cv2.waitKey(1)

# Diccionario para almacenar los nombres corregidos y su conteo
nombres_corregidos = defaultdict(int)

# Procesar los nombres para corregir duplicados
for nombre, conteo in nombres_contador.items():
    # Buscar nombres similares en el diccionario de nombres corregidos
    encontrado = False
    for nombre_corregido in nombres_corregidos.keys():
        # Calcular la distancia de Levenshtein entre los nombres
        distancia = lev.distance(nombre.lower(), nombre_corregido.lower())
        # Si la distancia es menor que 5 caracteres, consideramos los nombres como similares
        if distancia < 5:
            # Conservar el nombre con mayor conteo de fotogramas
            nombres_corregidos[nombre_corregido] += conteo
            encontrado = True
            break
    # Si no se encontró un nombre similar, agregarlo al diccionario de nombres corregidos
    if not encontrado:
        nombres_corregidos[nombre] += conteo

# Imprimir los nombres extraídos y su conteo
for nombre, conteo in nombres_corregidos.items():
    print(f"{nombre}: {conteo}")

# Liberar el objeto VideoCapture
cap.release()
cv2.destroyAllWindows()



