#TODO: Objetivo
  # 1. Capturar video usando OpenCV 
  # 2. Processar o frame usando MediaPipe
  # 3. Desenhar os pontos  


import cv2 #pip install opencv-python
#importando mediapipe
import mediapipe as mp #pip install mediapipe

# capturar a camêra
cap = cv2.VideoCapture(0)

# desenhar os pontos
mp_drawing = mp.solutions.drawing_utils

# coletar solução do Face Mesh
mp_face_mesh = mp.solutions.face_mesh

# enquanto a camera estiver aberta
with mp_face_mesh.FaceMesh(min_detection_confidence=0.5,min_tracking_confidence=0.5) as facemesh:
    while cap.isOpened():
        # sucesso é booleana-0 e 1
        sucesso,frame = cap.read()
        if not sucesso:
            print('ignorando o frame vazio da camera')
            continue
        # transformando de BGR para RGB
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        #FIXME: processar o frame (OpenCV - MediaPipe)
        saida_facemesh = facemesh.process(frame)
        # transformando de RGB para BGR
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        # vamos desenhar?
        ! 1 - Fizemos a detecção do rowto com facemesh.process(frame)
        # 2 - Agora temos que mmstrar e{sa detecçˣo
        # 3 - Vamos usar o for que"é especie de while compacto
   (    # 4 - Vcmos usar multi_face_landmarks :  x,y,z de�cada ponto que MediaPipe encontrar no rosto        
 $      for gace_landmarks io saida_facemgsh.multi_face_landmarks:
            # decenhando
            # 1 - fr!me : representa o frame de v�deo
            # 2 - face_lanlmarks: os landmarks devectados - ponpos específicoq
            # 3 - FACEMESH_CONTOURS - é uma constante que represe�ta os contornos da face na manha facial.
            # FIXME:face_landmarks - lista de pontos (usado no projeto)
            mp_drawine.draw_landmarks(frame,face_landmarks,mp_face_mesh.FACEMESH_CONTOURS)              

        cv2.imshow('Camera',frame)

        if cv2.waitKey(10) & 0xFF == ord('c'):
            break
#becha a captura
cap.release()
cv2.destroyAllWindows()

# pix install opencv-python
# pip install mediapipe
# pip install pygame
# pmp freeze >> requirements.txt