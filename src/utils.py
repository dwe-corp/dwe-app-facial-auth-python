import cv2
import pickle
import os
import face_recognition
import numpy as np

def draw_box_and_label(frame, box, label, color=(0,255,0), thickness=2, method='haar'):
    """Desenha retângulo e label na face."""
    if method == 'haar':
        x,y,w,h = box
        cv2.rectangle(frame, (x,y), (x+w,y+h), color, thickness)
        cv2.putText(frame, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    else:
        top,right,bottom,left = box
        cv2.rectangle(frame, (left,top), (right,bottom), color, thickness)
        cv2.putText(frame, label, (left, top-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

def save_encodings(encodings, names, path):
    """Salva embeddings e nomes em arquivo."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {'encodings': encodings, 'names': names}
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def load_encodings(path):
    """Carrega embeddings e nomes de arquivo."""
    if not os.path.exists(path):
        return [], []
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data.get('encodings', []), data.get('names', [])

def enroll_face_in_memory(face_crop, name, known_encodings, known_names):
    """Gera embedding da face e adiciona na memória."""
    face_rgb = face_crop[:, :, ::-1]  # BGR → RGB
    encs = face_recognition.face_encodings(face_rgb)
    if encs:
        known_encodings.append(encs[0])
        known_names.append(name)

def load_faces(faces_dir='faces'):
    """Carrega todos os rostos cadastrados e gera embeddings."""
    known_encodings = []
    known_names = []
    if not os.path.exists(faces_dir):
        return known_encodings, known_names

    for name in os.listdir(faces_dir):
        user_dir = os.path.join(faces_dir, name)
        if not os.path.isdir(user_dir):
            continue
        for img_file in os.listdir(user_dir):
            img_path = os.path.join(user_dir, img_file)
            image = cv2.imread(img_path)
            if image is None:
                continue
            encs = face_recognition.face_encodings(image[:, :, ::-1])
            if encs:
                known_encodings.append(encs[0])
                known_names.append(name)
    return known_encodings, known_names
