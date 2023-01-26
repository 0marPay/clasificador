import cv2
from google.cloud import vision
from google.cloud.vision_v1 import types

# Cargar la imagen en un objeto de cv2
img = cv2.imread('test/caratula_test.jpg')

# Convertir la imagen a HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Definir los rangos de tonos de verde y rojo
green_lower = (20, 242, 21)
green_upper = (38, 229, 38)
red_lower = (193, 35, 36)
red_upper = (233, 11, 0)

# Crear máscaras para los tonos de verde y rojo
green_mask = cv2.inRange(hsv, green_lower, green_upper)
red_mask = cv2.inRange(hsv, red_lower, red_upper)

# Combina las máscaras
mask = cv2.bitwise_or(green_mask, red_mask)

# Encontrar los contornos en la máscara
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Inicializar cliente de Google Cloud Vision
client = vision.ImageAnnotatorClient()

# Iterar a través de los contornos encontrados
for contour in contours:
    # Encuentra las coordenadas de los vértices del rectángulo
    x, y, w, h = cv2.boundingRect(contour)
    # Recorta la imagen para solo contener el contenido dentro del rectángulo
    roi = img[y:y+h, x:x+w]
    #Convertir la imagen a bytes
    ret, buffer = cv2.imencode('.jpg', roi)
    #Crear un objeto de tipo Image
    img_bytes = buffer.tobytes()
    image = types.Image(content=img_bytes)
    #Realizar el OCR en el ROI
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print(texts)