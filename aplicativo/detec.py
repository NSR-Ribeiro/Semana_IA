import tensorflow as tf
import numpy as np
import cv2

# Carregar modelo de detecção de objetos (exemplo com o SSD Mobilenet)
model = tf.saved_model.load("ssd_mobilenet_v2_coco/saved_model")

# Função para detectar objetos
def detect_objects(image):
    input_tensor = tf.convert_to_tensor(image)
    input_tensor = input_tensor[tf.newaxis,...]

    # Detecção de objetos
    detections = model(input_tensor)

    return detections

# Captura de vídeo
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Redimensionar a imagem para o tamanho esperado pelo modelo
    image_resized = cv2.resize(frame, (300, 300))
    image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)

    detections = detect_objects(image_rgb)

    # Desenhar caixas delimitadoras (bounding boxes) sobre os objetos detectados
    for detection in detections['detection_boxes']:
        # (Nota: A detecção pode retornar coordenadas normalizadas, então você pode precisar ajustá-las)
        (ymin, xmin, ymax, xmax) = detection[0].numpy()

        # Converter para pixels reais
        start_point = (int(xmin * frame.shape[1]), int(ymin * frame.shape[0]))
        end_point = (int(xmax * frame.shape[1]), int(ymax * frame.shape[0]))

        # Desenhar a caixa
        cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 2)

    # Exibir a imagem com as caixas
    cv2.imshow('Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
