import cv2
import numpy as np
import pytesseract
from sklearn.cluster import KMeans
from collections import defaultdict
import os

# Configurar la variable de entorno para `joblib`
os.environ['LOKY_MAX_CPU_COUNT'] = '4'  # Ajusta este valor según los núcleos lógicos de tu máquina

# Configurar la ruta de Tesseract directamente en el script
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Voolkia\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
print(f"Tesseract path: {pytesseract.pytesseract.tesseract_cmd}")

# Función para calcular el histograma de un fotograma
def calculate_histogram(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv_image], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()

# Coordenadas y tamaño de la región de interés donde aparece el nombre
y1, x1 = 410, 926  # Coordenadas de la esquina superior izquierda
y2, x2 = 422, 1063  # Coordenadas de la esquina inferior derecha
h = y2 - y1  # Altura de la región de interés
w = x2 - x1  # Ancho de la región de interés

# Función para extraer el nombre del hablante usando OCR
def extract_name(frame):
    roi = frame[y1:y1+h, x1:x1+w]
    try:
        name = pytesseract.image_to_string(roi)  # Incrementar el timeout a 10 segundos
    except pytesseract.TesseractError as e:
        print(f"Error: {e}")
        name = ""
    return name.strip()

# Ruta del video (en el mismo directorio)
video_path = 'prueba.mp4'

# Inicializar variables
frames = []
histograms = []

# Cargar el video
cap = cv2.VideoCapture(video_path)
frame_rate = cap.get(cv2.CAP_PROP_FPS)

# Procesamiento incremental de fotogramas
while cap.isOpened():
    # Leer un fotograma
    ret, frame = cap.read()
    if not ret:
        break

    # Procesar el fotograma
    hist = calculate_histogram(frame)
    histograms.append(hist)
    frames.append(frame)

# Cerrar el video
cap.release()

# Realizar el clustering con KMeans
optimal_n_clusters = 10  # Ajusta según los resultados
kmeans = KMeans(n_clusters=optimal_n_clusters)
labels = kmeans.fit_predict(histograms)

# Agrupar los fotogramas por labels
grouped_frames = defaultdict(list)
for label, frame in zip(labels, frames):
    grouped_frames[label].append(frame)

# Diccionario para almacenar los nombres y sus conteos
speaker_names = defaultdict(int)

for label, frames in grouped_frames.items():
    for frame in frames:
        name = extract_name(frame)
        if name:
            speaker_names[name] += 1
            break  # Salir después de encontrar un nombre en el grupo

# Guardar los resultados en un archivo de texto
with open("resultados.txt", "w") as f:
    for name, count in speaker_names.items():
        f.write(f"Speaker: {name}, Frame Count: {count}\n")