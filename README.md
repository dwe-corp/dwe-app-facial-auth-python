# FaceID-Local 😎

Aplicação local de **detecção e identificação facial** para desktop/notebook, usando **OpenCV (Haar Cascade)** para detecção de faces e **face\_recognition (dlib)** para reconhecimento facial baseado em encodings.

O projeto permite cadastrar usuários, reconhecer rostos previamente cadastrados, e exibir em tempo real a identificação diretamente na tela da câmera. 🎥

## Equipe - DWE 👥

* Deivison Pertel – RM 550803
* Eduardo Akira Murata – RM 98713
* Wesley Souza de Oliveira – RM 97874
---
## 🎥 Demonstração em Vídeo

[Assista aqui no YouTube](https://youtu.be/YVRBcE0Dz8Q)

---

## Objetivo do Projeto 🎯

* Desenvolver uma aplicação local que reconheça rostos de usuários usando técnicas de visão computacional e aprendizado de máquina. 🤖
* Demonstrar parâmetros ajustáveis de detecção (Haar Cascade) e reconhecimento (face\_recognition) e seu impacto no desempenho e precisão. ⚙️
* Permitir cadastro, exclusão e atualização de usuários de forma simples e interativa. 📝
* Fornecer feedback visual claro para rostos reconhecidos e não reconhecidos. 👀

---

## Requisitos / Dependências 📦

* Python 3.10 ou superior 🐍
* OpenCV (`opencv-python`) 🖼️
* NumPy (`numpy`) 📊
* dlib (`dlib`) e face\_recognition (`face_recognition`) 🧠
* PyYAML (`PyYAML`) 📄
* imutils (`imutils`) 🔧
* pickle (`pickle`) 💾

Instalação das dependências:

```bash
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
FaceID-Local/
│
├─ src/
│   ├─ models/          # Modelo de leitura frontalface haar
│   ├─ main.py          # Aplicação principal (câmera e reconhecimento)
│   ├─ detectors.py     # Classe HaarDetector para detecção
│   ├─ utils.py         # Funções auxiliares (draw_box, load/save encodings)
│
├─ config.yaml          # Configurações do projeto (Haar, face_recog, câmera)
├─ faces/               # Imagens cadastradas dos usuários
├─ encodings/           # Arquivo encodings.pkl com encodings salvos
├─ requirements.txt     # Dependências Python
```

---

## Execução ▶️

1. **Cadastrar usuário** (opcional via terminal ou dentro da aplicação):

```bash
python -m src.enroll --name SeuNome --num 5
```

2. **Executar aplicação principal**:

```bash
python -m src.main
```

3. Ajuste parâmetros em `config.yaml` (ex.: Haar cascade, tolerância do reconhecimento, resolução da câmera, FPS). ⚙️

---

## Controles da aplicação ⌨️

* **C**: Cadastrar novo usuário. ➕
* **D**: Deletar usuário existente. ❌
* **Q**: Encerrar o programa. 🛑

### Feedback visual 👁️

* **Rostos reconhecidos**: nome exibido em **verde** ✅
* **Rostos não reconhecidos**: quadrado vermelho com a label "**Rosto Desconhecido**" ❌
* FPS exibido no canto superior esquerdo (opcional) ⏱️

## Nota Ética 🛡️

* **Consentimento**: obtenha consentimento explícito de todas as pessoas cujas imagens serão capturadas. 🙋‍♂️🙋‍♀️
* **Minimização de dados**: armazene apenas o necessário, evite reter dados por tempo excessivo. 📉
* **Segurança**: proteja imagens e encodings (criptografia, controle de acesso). 🔒
* **Viés e justiça**: modelos pré-treinados podem ter enviesamentos; teste com diversidade. ⚖️
* **Uso responsável**: não utilize para vigilância em larga escala ou decisões automatizadas sem supervisão. 🚫
