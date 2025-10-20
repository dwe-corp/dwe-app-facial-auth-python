from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import yaml
import time
import os
import numpy as np
import base64
import io
from PIL import Image
import requests
import logging
from src.detectors import HaarDetector
from src.utils import draw_box_and_label, load_encodings, save_encodings, enroll_face_in_memory

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Carrega configuração
with open('config.yaml') as f:
    cfg = yaml.safe_load(f)

FACES_DIR = 'faces'
ENC_FILE = 'encodings/encodings.pkl'
AUTH_API_URL = 'http://localhost:8082'  # URL do serviço de autenticação

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

def base64_to_image(base64_string):
    """Converte string base64 para imagem OpenCV."""
    try:
        # Remove o prefixo data:image/jpeg;base64, se existir
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decodifica base64
        image_data = base64.b64decode(base64_string)
        
        # Converte para PIL Image
        pil_image = Image.open(io.BytesIO(image_data))
        
        # Converte para OpenCV format (BGR)
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        return opencv_image
    except Exception as e:
        logger.error(f"Erro ao converter base64 para imagem: {e}")
        return None

def recognize_face(image):
    """Reconhece face na imagem e retorna o nome se encontrado."""
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = haar.detect(gray)
        
        if len(faces) == 0:
            return None, "Nenhuma face detectada"
        
        # Pega a primeira face detectada
        (x, y, w, h) = faces[0]
        face_crop = image[y:y+h, x:x+w]
        
        # Reconhecimento via face_recognition
        face_rgb = face_crop[:, :, ::-1]
        import face_recognition
        encodings = face_recognition.face_encodings(face_rgb)
        
        if not encodings:
            return None, "Não foi possível extrair características da face"
        
        distances = face_recognition.face_distance(known_encodings, encodings[0])
        if len(distances) > 0:
            min_idx = np.argmin(distances)
            if distances[min_idx] <= cfg['face_recog']['tolerance']:
                return known_names[min_idx], "Face reconhecida"
        
        return None, "Face não reconhecida"
        
    except Exception as e:
        logger.error(f"Erro no reconhecimento facial: {e}")
        return None, f"Erro no processamento: {str(e)}"

def get_user_by_name(name):
    """Busca usuário no sistema de autenticação pelo nome."""
    try:
        response = requests.get(f"{AUTH_API_URL}/auth")
        if response.status_code == 200:
            users = response.json()
            for user in users:
                if user.get('nome', '').lower() == name.lower():
                    return user
        return None
    except Exception as e:
        logger.error(f"Erro ao buscar usuário: {e}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check."""
    return jsonify({
        "status": "healthy",
        "service": "facial-recognition-api",
        "timestamp": time.time()
    })

@app.route('/recognize', methods=['POST'])
def recognize():
    """Endpoint para reconhecimento facial."""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({
                "success": False,
                "error": "Imagem não fornecida"
            }), 400
        
        # Converte base64 para imagem
        image = base64_to_image(data['image'])
        if image is None:
            return jsonify({
                "success": False,
                "error": "Erro ao processar imagem"
            }), 400
        
        # Reconhece a face
        name, message = recognize_face(image)
        
        if name:
            # Busca dados do usuário no sistema de autenticação
            user = get_user_by_name(name)
            if user:
                return jsonify({
                    "success": True,
                    "recognized": True,
                    "user": {
                        "id": user.get('id'),
                        "nome": user.get('nome'),
                        "email": user.get('email'),
                        "perfil": user.get('perfil')
                    },
                    "message": message
                })
            else:
                return jsonify({
                    "success": True,
                    "recognized": True,
                    "user": {
                        "nome": name
                    },
                    "message": f"Face reconhecida como {name}, mas usuário não encontrado no sistema"
                })
        else:
            return jsonify({
                "success": True,
                "recognized": False,
                "message": message
            })
            
    except Exception as e:
        logger.error(f"Erro no endpoint /recognize: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/enroll', methods=['POST'])
def enroll():
    """Endpoint para cadastro de nova face."""
    try:
        data = request.get_json()
        if not data or 'image' not in data or 'user_id' not in data:
            return jsonify({
                "success": False,
                "error": "Imagem e user_id são obrigatórios"
            }), 400
        
        # Busca dados do usuário
        user_response = requests.get(f"{AUTH_API_URL}/auth/{data['user_id']}")
        if user_response.status_code != 200:
            return jsonify({
                "success": False,
                "error": "Usuário não encontrado"
            }), 404
        
        user = user_response.json()
        user_name = user.get('nome')
        
        # Converte base64 para imagem
        image = base64_to_image(data['image'])
        if image is None:
            return jsonify({
                "success": False,
                "error": "Erro ao processar imagem"
            }), 400
        
        # Detecta face na imagem
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = haar.detect(gray)
        
        if len(faces) == 0:
            return jsonify({
                "success": False,
                "error": "Nenhuma face detectada na imagem"
            }), 400
        
        # Pega a primeira face detectada
        (x, y, w, h) = faces[0]
        face_crop = image[y:y+h, x:x+w]
        
        # Cria diretório do usuário se não existir
        user_dir = os.path.join(FACES_DIR, user_name)
        os.makedirs(user_dir, exist_ok=True)
        
        # Salva a imagem
        timestamp = int(time.time())
        image_path = os.path.join(user_dir, f"{timestamp}.jpg")
        cv2.imwrite(image_path, face_crop)
        
        # Adiciona encoding à memória
        enroll_face_in_memory(face_crop, user_name, known_encodings, known_names)
        
        # Salva encodings atualizados
        save_encodings(known_encodings, known_names, ENC_FILE)
        
        return jsonify({
            "success": True,
            "message": f"Face cadastrada com sucesso para {user_name}",
            "user": {
                "id": user.get('id'),
                "nome": user.get('nome'),
                "email": user.get('email')
            }
        })
        
    except Exception as e:
        logger.error(f"Erro no endpoint /enroll: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/enrolled-users', methods=['GET'])
def get_enrolled_users():
    """Retorna lista de usuários com faces cadastradas."""
    try:
        enrolled_users = []
        if os.path.exists(FACES_DIR):
            for name in os.listdir(FACES_DIR):
                user_dir = os.path.join(FACES_DIR, name)
                if os.path.isdir(user_dir):
                    # Busca dados do usuário no sistema de autenticação
                    user = get_user_by_name(name)
                    if user:
                        enrolled_users.append({
                            "id": user.get('id'),
                            "nome": user.get('nome'),
                            "email": user.get('email'),
                            "perfil": user.get('perfil'),
                            "faces_count": len([f for f in os.listdir(user_dir) if f.endswith('.jpg')])
                        })
        
        return jsonify({
            "success": True,
            "users": enrolled_users
        })
        
    except Exception as e:
        logger.error(f"Erro no endpoint /enrolled-users: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/delete-user/<user_name>', methods=['DELETE'])
def delete_user_face(user_name):
    """Remove face cadastrada de um usuário."""
    try:
        user_dir = os.path.join(FACES_DIR, user_name)
        if os.path.exists(user_dir):
            # Remove arquivos de imagem
            for f in os.listdir(user_dir):
                os.remove(os.path.join(user_dir, f))
            os.rmdir(user_dir)
            
            # Remove da memória
            global known_encodings, known_names
            indices = [i for i, n in enumerate(known_names) if n == user_name]
            for i in sorted(indices, reverse=True):
                del known_names[i]
                del known_encodings[i]
            
            # Salva encodings atualizados
            save_encodings(known_encodings, known_names, ENC_FILE)
            
            return jsonify({
                "success": True,
                "message": f"Face removida com sucesso para {user_name}"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Usuário não encontrado"
            }), 404
            
    except Exception as e:
        logger.error(f"Erro no endpoint /delete-user: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

if __name__ == '__main__':
    logger.info("Iniciando servidor de reconhecimento facial...")
    logger.info(f"API de autenticação: {AUTH_API_URL}")
    logger.info(f"Usuários cadastrados: {len(known_names)}")
    app.run(host='0.0.0.0', port=5000, debug=True)
