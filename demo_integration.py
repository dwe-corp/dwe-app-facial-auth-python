#!/usr/bin/env python3
"""
Script de demonstração da solução integrada de reconhecimento facial.
Este script demonstra o fluxo completo de integração e gera dados de exemplo.
"""

import requests
import json
import base64
import time
import sys
import os
from PIL import Image, ImageDraw, ImageFont
import io
import random

# URLs dos serviços
FACIAL_API_URL = "http://localhost:5000"
AUTH_API_URL = "http://localhost:8080"

def create_demo_image(name, size=(300, 300)):
    """Cria uma imagem de demonstração com o nome do usuário."""
    # Cria imagem com fundo colorido
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    bg_color = random.choice(colors)
    
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Adiciona texto com o nome
    try:
        # Tenta usar uma fonte padrão
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        # Se não encontrar, usa fonte padrão
        font = ImageFont.load_default()
    
    # Calcula posição central
    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Desenha o texto
    draw.text((x, y), name, fill='white', font=font)
    
    # Converte para base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return img_base64

def create_demo_users():
    """Cria usuários de demonstração no sistema de autenticação."""
    print("👥 Criando usuários de demonstração...")
    
    demo_users = [
        {"nome": "João Silva", "email": "joao@email.com", "senha": "123456", "perfil": "INVESTIDOR"},
        {"nome": "Maria Santos", "email": "maria@email.com", "senha": "123456", "perfil": "ASSESSOR"},
        {"nome": "Pedro Costa", "email": "pedro@email.com", "senha": "123456", "perfil": "INVESTIDOR"},
        {"nome": "Ana Oliveira", "email": "ana@email.com", "senha": "123456", "perfil": "ASSESSOR"},
    ]
    
    created_users = []
    
    for user_data in demo_users:
        try:
            response = requests.post(f"{AUTH_API_URL}/auth", json=user_data, timeout=5)
            if response.status_code == 200:
                user = response.json()
                created_users.append(user)
                print(f"   ✅ {user['nome']} criado (ID: {user['id']})")
            else:
                print(f"   ❌ Erro ao criar {user_data['nome']}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Erro de conexão para {user_data['nome']}: {e}")
    
    return created_users

def enroll_demo_faces(users):
    """Cadastra faces de demonstração para os usuários."""
    print("📸 Cadastrando faces de demonstração...")
    
    for user in users:
        try:
            # Cria imagem de demonstração
            demo_image = create_demo_image(user['nome'])
            
            # Cadastra face via API de autenticação
            response = requests.post(f"{AUTH_API_URL}/facial-auth/enroll/{user['id']}",
                                   json={"image": demo_image},
                                   timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ Face cadastrada para {user['nome']}")
            else:
                print(f"   ❌ Erro ao cadastrar face para {user['nome']}: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Erro de conexão para {user['nome']}: {e}")

def test_facial_login(users):
    """Testa login facial para os usuários cadastrados."""
    print("🔐 Testando login facial...")
    
    for user in users:
        try:
            # Cria imagem de demonstração (mesma do cadastro)
            demo_image = create_demo_image(user['nome'])
            
            # Testa login facial
            response = requests.post(f"{AUTH_API_URL}/facial-auth/login",
                                   json={"image": demo_image},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('user'):
                    recognized_user = data['user']
                    print(f"   ✅ Login facial OK para {recognized_user['nome']}")
                    print(f"      📧 Email: {recognized_user['email']}")
                    print(f"      👤 Perfil: {recognized_user['perfil']}")
                else:
                    print(f"   ❌ Face não reconhecida para {user['nome']}")
            else:
                print(f"   ❌ Erro no login facial para {user['nome']}: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Erro de conexão para {user['nome']}: {e}")

def show_integration_stats():
    """Mostra estatísticas da integração."""
    print("📊 Estatísticas da integração...")
    
    try:
        # Estatísticas do serviço de reconhecimento facial
        response = requests.get(f"{FACIAL_API_URL}/enrolled-users", timeout=5)
        if response.status_code == 200:
            data = response.json()
            users = data.get('users', [])
            print(f"   👥 Usuários com faces cadastradas: {len(users)}")
            for user in users:
                print(f"      - {user['nome']} ({user['email']}) - {user['faces_count']} faces")
        
        # Estatísticas do serviço de autenticação
        response = requests.get(f"{AUTH_API_URL}/auth", timeout=5)
        if response.status_code == 200:
            users = response.json()
            print(f"   👥 Total de usuários no sistema: {len(users)}")
            
            # Conta por perfil
            profiles = {}
            for user in users:
                profile = user.get('perfil', 'UNKNOWN')
                profiles[profile] = profiles.get(profile, 0) + 1
            
            for profile, count in profiles.items():
                print(f"      - {profile}: {count} usuários")
                
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro ao buscar estatísticas: {e}")

def main():
    """Função principal."""
    print("=" * 60)
    print("🎭 DEMONSTRAÇÃO DA SOLUÇÃO INTEGRADA")
    print("=" * 60)
    print()
    
    # Verifica se os serviços estão rodando
    print("🔍 Verificando serviços...")
    
    try:
        # Testa serviço de reconhecimento facial
        response = requests.get(f"{FACIAL_API_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Serviço de reconhecimento facial não está rodando!")
            print("   Execute: python start_integrated_solution.py")
            return
        print("   ✅ Serviço de reconhecimento facial OK")
        
        # Testa serviço de autenticação
        response = requests.get(f"{AUTH_API_URL}/auth", timeout=5)
        if response.status_code != 200:
            print("❌ Serviço de autenticação não está rodando!")
            print("   Execute: ./mvnw spring-boot:run no diretório dwe-app-auth-java/")
            return
        print("   ✅ Serviço de autenticação OK")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return
    
    print()
    
    # Cria usuários de demonstração
    users = create_demo_users()
    if not users:
        print("❌ Não foi possível criar usuários de demonstração")
        return
    
    print()
    
    # Cadastra faces de demonstração
    enroll_demo_faces(users)
    print()
    
    # Testa login facial
    test_facial_login(users)
    print()
    
    # Mostra estatísticas
    show_integration_stats()
    print()
    
    print("=" * 60)
    print("✅ DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print()
    print("🎯 O que foi demonstrado:")
    print("1. ✅ Criação de usuários no sistema de autenticação")
    print("2. ✅ Cadastro de faces via API integrada")
    print("3. ✅ Login facial via API integrada")
    print("4. ✅ Estatísticas da integração")
    print()
    print("📱 Próximos passos:")
    print("1. Inicie a aplicação mobile")
    print("2. Use a opção 'Login Facial'")
    print("3. Teste com as faces cadastradas")
    print()
    print("🔧 Para testar via API:")
    print(f"   - Reconhecimento: {FACIAL_API_URL}")
    print(f"   - Autenticação: {AUTH_API_URL}")

if __name__ == "__main__":
    main()
