# FaceID-Integrated 🔐

Solução integrada de **reconhecimento facial** que conecta com sistemas de autenticação e aplicações mobile, usando **OpenCV (Haar Cascade)** para detecção de faces e **face\_recognition (dlib)** para reconhecimento facial baseado em encodings.

O projeto evoluiu da POC da Entrega 3 para uma solução completa que permite autenticação via reconhecimento facial em aplicações web/mobile, integrando com sistemas de autenticação Java e aplicações React Native. 🚀

## Equipe - DWE 👥

* Deivison Pertel – RM 550803
* Eduardo Akira Murata – RM 98713
* Wesley Souza de Oliveira – RM 97874
---
## 🎥 Demonstração em Vídeo

[Assista aqui no YouTube](https://youtu.be/YVRBcE0Dz8Q)
[SPRINT 4](https://youtu.be/7hxYT513nWM)

---

## Objetivo do Projeto 🎯

* **Integrar reconhecimento facial** com sistemas de autenticação existentes (Java Spring Boot). 🔗
* **Implementar autenticação biométrica** em aplicações mobile (React Native). 📱
* **Criar APIs REST** para comunicação entre serviços de reconhecimento facial e autenticação. 🌐
* **Demonstrar integração prática** entre diferentes tecnologias (Python, Java, React Native). ⚙️
* **Fornecer solução completa** de autenticação via reconhecimento facial. 🎯

---

## Requisitos / Dependências 📦

### Python (Serviço de Reconhecimento Facial)
* Python 3.10 ou superior 🐍
* OpenCV (`opencv-python`) 🖼️
* NumPy (`numpy`) 📊
* dlib (`dlib`) e face\_recognition (`face_recognition`) 🧠
* PyYAML (`PyYAML`) 📄
* imutils (`imutils`) 🔧
* pickle (`pickle`) 💾
* Flask (`flask`) 🌐
* Flask-CORS (`flask-cors`) 🔗
* Pillow (`pillow`) 🖼️
* requests (`requests`) 📡

### Java (Serviço de Autenticação)
* Java 17+ ☕
* Spring Boot 3.x 🍃
* Maven 3.6+ 📦

### React Native (Aplicação Mobile)
* Node.js 18+ 🟢
* React Native 0.72+ ⚛️
* Expo Camera 📷

### Instalação Rápida

```bash
# Configure tudo automaticamente
python setup_integration.py

# Ou instale manualmente
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Estrutura do Projeto 📂

```
FaceID-Integrated/
│
├─ src/
│   ├─ models/              # Modelo de leitura frontalface haar
│   ├─ main.py              # Aplicação original (câmera local)
│   ├─ api_server.py        # Servidor Flask para APIs REST
│   ├─ detectors.py         # Classe HaarDetector para detecção
│   ├─ utils.py             # Funções auxiliares (draw_box, load/save encodings)
│
├─ config.yaml              # Configurações do projeto
├─ faces/                   # Imagens cadastradas dos usuários
├─ encodings/               # Arquivo encodings.pkl com encodings salvos
├─ requirements.txt         # Dependências Python
├─ setup_integration.py     # Script de configuração automática
├─ start_integrated_solution.py  # Script de inicialização
├─ INTEGRATION_GUIDE.md     # Guia completo de integração
└─ README.md               # Este arquivo
```

## Arquitetura da Solução 🏗️

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile App    │    │  Auth Service   │    │ Facial Service  │
│   (React)       │◄──►│    (Java)       │◄──►│   (Python)      │
│   Port: 3000    │    │   Port: 8080    │    │   Port: 5000    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## Execução ▶️

### 🚀 Início Rápido (Solução Integrada)

1. **Configure o ambiente**:
```bash
python setup_integration.py
```

2. **Inicie o serviço de autenticação Java** (em outro terminal):
```bash
cd ../dwe-app-auth-java
./mvnw spring-boot:run
```

3. **Inicie o serviço de reconhecimento facial**:
```bash
python start_integrated_solution.py
```

4. **Inicie a aplicação mobile** (em outro terminal):
```bash
cd ../dwe-app-mobile-react
npm start
```

### 🔧 Execução Individual

1. **Aplicação local original**:
```bash
python -m src.main
```

2. **Servidor de APIs**:
```bash
python src/api_server.py
```

3. **Cadastrar usuário** (opcional):
```bash
python -m src.enroll --name SeuNome --num 5
```

---

## APIs Disponíveis 🌐

### Serviço de Reconhecimento Facial (Porta 5000)

* `GET /health` - Health check do serviço
* `POST /recognize` - Reconhece face na imagem (base64)
* `POST /enroll` - Cadastra face de usuário
* `GET /enrolled-users` - Lista usuários com faces cadastradas
* `DELETE /delete-user/<nome>` - Remove face do usuário

### Serviço de Autenticação (Porta 8080)

* `POST /facial-auth/login` - Login via reconhecimento facial
* `POST /facial-auth/enroll/{userId}` - Cadastro de face
* `GET /facial-auth/enrolled-users` - Lista usuários cadastrados
* `DELETE /facial-auth/delete/{userName}` - Remove face

### Controles da Aplicação Local ⌨️

* **C**: Cadastrar novo usuário. ➕
* **D**: Deletar usuário existente. ❌
* **Q**: Encerrar o programa. 🛑

### Feedback Visual 👁️

* **Rostos reconhecidos**: nome exibido em **verde** ✅
* **Rostos não reconhecidos**: quadrado vermelho com a label "**Rosto Desconhecido**" ❌
* FPS exibido no canto superior esquerdo (opcional) ⏱️

## Testes e Demonstração 🧪

### Teste Automatizado
```bash
# Testa toda a integração
python test_integration.py

# Demonstração completa com dados de exemplo
python demo_integration.py
```

### Teste Manual via API
```bash
# Health check
curl http://localhost:5000/health

# Lista usuários cadastrados
curl http://localhost:5000/enrolled-users

# Login facial (substitua pela imagem base64)
curl -X POST http://localhost:8080/facial-auth/login \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_encoded_image"}'
```

## Docker Support 🐳

### Execução com Docker Compose
```bash
# Inicia todos os serviços
docker-compose up --build

# Para desenvolvimento
docker-compose up -d
```

### Docker Individual
```bash
# Apenas o serviço de reconhecimento facial
docker build -t facial-recognition .
docker run -p 5000:5000 facial-recognition
```

## Nota Ética 🛡️

* **Consentimento**: obtenha consentimento explícito de todas as pessoas cujas imagens serão capturadas. 🙋‍♂️🙋‍♀️
* **Minimização de dados**: armazene apenas o necessário, evite reter dados por tempo excessivo. 📉
* **Segurança**: proteja imagens e encodings (criptografia, controle de acesso). 🔒
* **Viés e justiça**: modelos pré-treinados podem ter enviesamentos; teste com diversidade. ⚖️
* **Uso responsável**: não utilize para vigilância em larga escala ou decisões automatizadas sem supervisão. 🚫

## Entrega 4 - Integração Completa ✅

Esta solução atende aos requisitos da Entrega 4:

- ✅ **Reconhecimento facial funcionando** de forma consistente
- ✅ **Integração prática** com aplicação escolhida (não isolado)
- ✅ **Conexão comprovada** entre reconhecimento facial e aplicação final
- ✅ **README atualizado** com instruções completas
- ✅ **Explicação clara** de como o reconhecimento facial está conectado
- ✅ **APIs REST** para comunicação entre serviços
- ✅ **Aplicação mobile** com login facial integrado
- ✅ **Sistema de autenticação** Java integrado
- ✅ **Logs e monitoramento** de acesso
- ✅ **Documentação completa** da integração
