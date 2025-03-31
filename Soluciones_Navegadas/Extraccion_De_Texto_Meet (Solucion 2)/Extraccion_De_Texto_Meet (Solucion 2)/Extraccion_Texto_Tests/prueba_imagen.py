import cv2

# Función para manejar los eventos del mouse
def mouse_callback(event, x, y, flags, param):
    global roi_points

    if event == cv2.EVENT_LBUTTONDOWN:
        roi_points.append((x, y))
        if len(roi_points) == 2:
            print("Coordenadas de la esquina superior izquierda (x1, y1):", roi_points[0])
            print("Coordenadas de la esquina inferior derecha (x2, y2):", roi_points[1])
            print("Tamaño de la región de interés (ancho, alto):", roi_points[1][0] - roi_points[0][0], ",", roi_points[1][1] - roi_points[0][1])
            roi_points = []

# Cargar la imagen
image = cv2.imread("prueba2.jpg")

# Crear una copia de la imagen para mostrar la región de interés seleccionada
clone = image.copy()

# Inicializar la lista de puntos de la región de interés (ROI)
roi_points = []

# Mostrar la imagen y esperar a que se seleccione la región de interés
cv2.imshow("Image", image)
cv2.setMouseCallback("Image", mouse_callback)
cv2.waitKey(0)
cv2.destroyAllWindows()
