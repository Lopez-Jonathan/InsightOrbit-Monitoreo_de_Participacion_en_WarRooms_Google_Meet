import cv2
import pytesseract
import spacy

# Cargar el modelo de lenguaje de spaCy para NER
nlp = spacy.load("es_core_news_sm")

# Ruta del video
video_path = 'prueba3.mp4'

# Coordenadas de la región de interés (ROI)
x1, y1 = 1442, 100  # Coordenadas de la esquina superior izquierda
x2, y2 = 2000, 800  # Coordenadas de la esquina inferior derecha

# Diccionario para almacenar los nombres extraídos y su conteo
nombres_contador = {}

# Crear un objeto VideoCapture
cap = cv2.VideoCapture(video_path)

# Obtener la frecuencia de cuadros por segundo (fps)
fps = cap.get(cv2.CAP_PROP_FPS)

# Establecer el tiempo inicial en 0
tiempo_actual = 0

# Leer el primer fotograma
ret, frame = cap.read()

# Verificar si la lectura fue exitosa
if ret:
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

            # Utilizar OCR para extraer el texto del fotograma completo
            texto_completo = pytesseract.image_to_string(gray_frame, lang='spa')

            # Reemplazar los saltos de línea con espacios
            texto_continuo = texto_completo.replace('\n', ' ')

            # Aplicar el modelo de spaCy NER al texto continuo
            doc = nlp(texto_continuo)

            # Filtrar y contar los nombres de personas
            for ent in doc.ents:
                if ent.label_ == "PER":  # Filtrar solo entidades que sean nombres de personas
                    nombre = ent.text.strip()  # Eliminar espacios en blanco alrededor
                    if nombre:
                        if nombre in nombres_contador:
                            nombres_contador[nombre] += 1
                        else:
                            nombres_contador[nombre] = 1

        # Aumentar el tiempo actual en 3 segundos (3000 ms)
        tiempo_actual += 1 * fps  # Multiplicar por fps para obtener el número de fotogramas en 3 segundos

        # Verificar si se alcanzó el final del video
        if tiempo_actual >= cap.get(cv2.CAP_PROP_FRAME_COUNT):
            break

# Imprimir los nombres extraídos y su conteo
for nombre, conteo in nombres_contador.items():
    print(f"{nombre}: {conteo}")

# Liberar el objeto VideoCapture
cap.release()
