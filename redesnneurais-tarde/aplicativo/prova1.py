import cv2  # pip install opencv-python
import mediapipe as mp  # pip install mediapipe
import numpy as np
import time
import pygame

# Inicializa o mixer de áudio
pygame.mixer.init()

# Carrega o arquivo de som
pygame.mixer.music.load("videoplayback.mp3")

# Captura da câmera
cap = cv2.VideoCapture(0)

# Inicializa a biblioteca de desenho do Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# Pontos dos olhos (esquerdo e direito)
p_olho_esq = [385, 380, 387, 373, 362, 263]
p_olho_dir = [160, 144, 158, 153, 33, 133]
p_olhos = p_olho_esq + p_olho_dir

# Função para calcular o EAR
def calculo_ear(face, p_olho_dir, p_olho_esq):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_esq = face[p_olho_esq, :]
        face_dir = face[p_olho_dir, :]

        # Distâncias verticais e horizontais dos olhos esquerdo e direito
        ear_esq = (np.linalg.norm(face_esq[0] - face_esq[1]) + np.linalg.norm(face_esq[2] - face_esq[3])) / (2 * np.linalg.norm(face_esq[4] - face_esq[5]))
        ear_dir = (np.linalg.norm(face_dir[0] - face_dir[1]) + np.linalg.norm(face_dir[2] - face_dir[3])) / (2 * np.linalg.norm(face_dir[4] - face_dir[5]))
    except Exception as e:
        print(f"Erro no cálculo do EAR: {e}")
        ear_esq, ear_dir = 0.0, 0.0

    media_ear = (ear_esq + ear_dir) / 2
    return media_ear

# Limite para detectar sono (EAR)
ear_limiar = 0.27
dormindo = 0

# Loop de captura de vídeo
with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as facemesh:
    while cap.isOpened():
        sucesso, frame = cap.read()
        if not sucesso:
            print('Ignorando o frame vazio da câmera')
            continue
        
        comprimento, largura, _ = frame.shape
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertendo BGR para RGB
        saida_facemesh = facemesh.process(frame)  # Processando a imagem para detectar rostos
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convertendo RGB de volta para BGR

        try:
            for face_landmarks in saida_facemesh.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 102, 102), thickness=1, circle_radius=1),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(102, 204, 0), thickness=1, circle_radius=1)
                )

                # Calculando o EAR
                face = face_landmarks.landmarks
                ear = calculo_ear(face, p_olho_dir, p_olho_esq)

                # Exibindo o EAR na tela
                cv2.rectangle(frame, (0, 1), (290, 140), (58, 58, 55), -1)
                cv2.putText(frame, f"EAR {round(ear, 2)}", (1, 24), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)

                # Monitorando tempo de olhos fechados
                if ear < ear_limiar:
                    t_inicial = time.time() if dormindo == 0 else t_inicial
                    dormindo = 1
                if dormindo == 1 and ear >= ear_limiar:
                    dormindo = 0
                t_final = time.time()

                tempo = (t_final - t_inicial) if dormindo == 1 else 0.0
                cv2.putText(frame, f"Tempo: {round(tempo, 3)}", (1, 80), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)

                if tempo >= 1.5:
                    cv2.rectangle(frame, (30, 400), (610, 452), (109, 233, 219), -1)
                    cv2.putText(frame, f"Muito tempo com olhos fechados", (80, 435), cv2.FONT_HERSHEY_DUPLEX, 0.85, (58, 58, 55), 1)

        except Exception as e:
            print(f"Erro ao processar a imagem: {e}")
        finally:
            print("Processamento concluído")

        cv2.imshow('Camera', frame)

        if cv2.waitKey(10) & 0xFF == ord('c'):
            break

cap.release()
