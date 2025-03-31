import re
from collections import defaultdict
import cv2
import pytesseract
import spacy
import Levenshtein as lev

# Cargar el modelo de lenguaje de spaCy para NER
nlp = spacy.load("es_core_news_sm")

# Ruta del video
video_path = 'prueba4.mp4'

# Coordenadas de la región de interés (ROI)
x1, y1 = 1444, 647  # Esquina superior izquierda
x2, y2 = 2000, 672  # Esquina inferior derecha

# Diccionario para almacenar los nombres extraídos y su conteo
nombres_contador = defaultdict(int)

# Crear un objeto VideoCapture para leer el video
cap = cv2.VideoCapture(video_path)

# Verificar si el video se abrió correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir el video.")
    exit()

# Obtener la frecuencia de cuadros por segundo (fps)
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"FPS del video: {fps}")

# Establecer el tiempo inicial en 0
tiempo_actual = 0

def limpiar_texto(texto):
    """Eliminar caracteres especiales utilizando expresiones regulares"""
    return re.sub(r'[^\w\s]', '', texto)

def hay_texto(gray_frame):
    """Verificar si hay texto en una imagen en escala de grises"""
    _, thresh = cv2.threshold(gray_frame, 200, 255, cv2.THRESH_BINARY)
    return cv2.countNonZero(thresh) > 50

def eliminar_repeticiones_finales(nombre):
    """Eliminar repeticiones finales en un nombre"""
    partes = nombre.split()
    for i in range(len(partes) - 1):
        subcadena = ' '.join(partes[i:])
        if nombre.endswith(subcadena) and ' '.join(partes[:i]).find(subcadena) != -1:
            return ' '.join(partes[:i])
    return nombre

# Procesar fotogramas del video
while True:
    cap.set(cv2.CAP_PROP_POS_MSEC, tiempo_actual * 1000)
    ret, frame = cap.read()

    if not ret:
        print("No se pudo leer el fotograma o se llegó al final del video.")
        break

    roi = frame[y1:y2, x1:x2]
    gray_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    if hay_texto(gray_frame):
        _, thresh = cv2.threshold(gray_frame, 200, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
        dilated = cv2.dilate(thresh, kernel, iterations=1)

        texto_completo = pytesseract.image_to_string(dilated, lang='spa', config='--psm 7')
        texto_limpio = limpiar_texto(texto_completo)

        for linea in texto_limpio.split('\n'):
            doc = nlp(linea)
            for ent in doc.ents:
                if ent.label_ == "PER":
                    nombre = ent.text.strip()
                    if nombre:
                        nombre_limpio = eliminar_repeticiones_finales(nombre)
                        nombres_contador[nombre_limpio] += 1

        print(f"Fotograma en tiempo {tiempo_actual / fps:.2f} segundos procesado.")

    tiempo_actual += 1 * fps
    if tiempo_actual >= cap.get(cv2.CAP_PROP_FRAME_COUNT):
        print("Fin del video alcanzado.")
        break
    cv2.waitKey(1)

nombres_corregidos = defaultdict(int)

for nombre, conteo in nombres_contador.items():
    encontrado = False
    for nombre_corregido in nombres_corregidos.keys():
        if lev.distance(nombre.lower(), nombre_corregido.lower()) < 5:
            nombres_corregidos[nombre_corregido] += conteo
            encontrado = True
            break
    if not encontrado:
        nombres_corregidos[nombre] += conteo

for nombre, conteo in nombres_corregidos.items():
    print(f"{nombre}: {conteo}")

cap.release()
print("Procesamiento completado.")