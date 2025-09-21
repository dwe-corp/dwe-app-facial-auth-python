import cv2
import yaml
import time
import os
import numpy as np
from src.detectors import HaarDetector
from src.utils import draw_box_and_label, load_encodings, save_encodings, enroll_face_in_memory

# Carrega configuração
with open('config.yaml') as f:
    cfg = yaml.safe_load(f)

FACES_DIR = 'faces'
ENC_FILE = 'encodings/encodings.pkl'

def enroll_user(cap, known_encodings, known_names):
    """Cadastra novo usuário e salva encoding."""
    name = input("Digite o nome do usuário para cadastro: ")
    user_dir = os.path.join(FACES_DIR, name)
    os.makedirs(user_dir, exist_ok=True)
    count = 0
    print(f"[INFO] Capturando 5 imagens para '{name}'...")
    
    while count < 5:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = haar.detect(gray)
        for (x, y, w, h) in faces:
            face_crop = frame[y:y+h, x:x+w]
            # Salva a imagem
            cv2.imwrite(os.path.join(user_dir, f"{count+1}.jpg"), face_crop)
            # Salva o encoding em memória
            enroll_face_in_memory(face_crop, name, known_encodings, known_names)
            count += 1
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, f"Captura {count}/5", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.imshow("Cadastro de Rosto", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return
    print("[INFO] Cadastro concluído.")
    save_encodings(known_encodings, known_names, ENC_FILE)  # salva os encodings no disco

def delete_user(known_encodings, known_names):
    """Exclui um usuário cadastrado."""
    name = input("Digite o nome do usuário para excluir: ")
    user_dir = os.path.join(FACES_DIR, name)
    if os.path.exists(user_dir):
        for f in os.listdir(user_dir):
            os.remove(os.path.join(user_dir, f))
        os.rmdir(user_dir)
        print(f"[INFO] Usuário '{name}' excluído.")
        # Remove da memória também
        indices = [i for i, n in enumerate(known_names) if n == name]
        for i in sorted(indices, reverse=True):
            del known_names[i]
            del known_encodings[i]
        save_encodings(known_encodings, known_names, ENC_FILE)
    else:
        print("[INFO] Usuário não encontrado.")

def run():
    global haar
    cap = cv2.VideoCapture(0)
    fps_time = time.time()

    # Inicializa detector Haar Cascade
    haar_cfg = cfg.get('haar', {})
    haar = HaarDetector(
        cascade_path='src/models/haarcascade_frontalface_default.xml',
        scaleFactor=haar_cfg.get('scaleFactor', 1.1),
        minNeighbors=haar_cfg.get('minNeighbors', 5),
        minSize=tuple(haar_cfg.get('minSize', (30, 30)))
    )

    # Carrega encodings cadastrados
    known_encodings, known_names = load_encodings(ENC_FILE)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = haar.detect(gray)

        for (x, y, w, h) in faces:
            face_crop = frame[y:y+h, x:x+w]
            # Reconhecimento via face_recognition
            face_rgb = face_crop[:, :, ::-1]
            import face_recognition
            encodings = face_recognition.face_encodings(face_rgb)
            name = "Rosto Desconhecido"
            color = (0,0,255)  # vermelho por padrão
            if encodings:
                distances = face_recognition.face_distance(known_encodings, encodings[0])
                if len(distances) > 0:
                    min_idx = np.argmin(distances)
                    if distances[min_idx] <= cfg['face_recog']['tolerance']:
                        name = known_names[min_idx]
                        color = (0,255,0)  # verde
            draw_box_and_label(frame, (x, y, w, h), name, color=color)

        cv2.putText(frame, "C: Cadastrar | D: Deletar | Q: Sair", (10, frame.shape[0]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv2.imshow(cfg.get('window_name', 'FaceID-Local'), frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            enroll_user(cap, known_encodings, known_names)
        elif key == ord('d'):
            delete_user(known_encodings, known_names)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run()
