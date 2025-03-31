import cv2

# Ruta del video
video_path = 'prueba.mp4'

# Crear un objeto VideoCapture
cap = cv2.VideoCapture(video_path)

# Establecer la posición en el segundo 00:00:50 (50 segundos)
cap.set(cv2.CAP_PROP_POS_MSEC, 50000)

# Leer el fotograma en la posición actual
ret, frame = cap.read()

# Verificar si la lectura fue exitosa
if ret:
    # Obtener las dimensiones del fotograma
    height, width, _ = frame.shape
    print("Ancho del fotograma:", width)
    print("Alto del fotograma:", height)

    # Definir las coordenadas de la región de interés (ROI)
    x1, y1 = 1444, 647  # Coordenadas de la esquina superior izquierda
    x2, y2 = 2000, 672  # Coordenadas de la esquina inferior derecha

    # Leer solo la parte deseada del fotograma
    roi = frame[y1:y2, x1:x2]

    # Mostrar la parte deseada del fotograma
    cv2.imshow('Parte del Fotograma', roi)
    cv2.waitKey(0)  # Esperar a que se presione una tecla para cerrar la ventana
    cv2.destroyAllWindows()
else:
    print("No se pudo leer el fotograma.")

# Liberar el objeto VideoCapture
cap.release()