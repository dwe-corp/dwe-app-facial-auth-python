#!/usr/bin/env python3
"""
Script de teste para a solução integrada de reconhecimento facial.
Este script testa as APIs e verifica se a integração está funcionando corretamente.
"""

import requests
import json
import base64
import time
import sys
import os
from PIL import Image
import io

# URLs dos serviços
FACIAL_API_URL = "http://localhost:5000"
AUTH_API_URL = "http://localhost:8080"

def test_facial_service():
    """Testa o serviço de reconhecimento facial."""
    print("🔍 Testando serviço de reconhecimento facial...")
    
    try:
        # Testa health check
        response = requests.get(f"{FACIAL_API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Health check OK")
            data = response.json()
            print(f"   📊 Status: {data.get('status')}")
            print(f"   🕐 Timestamp: {data.get('timestamp')}")
        else:
            print(f"   ❌ Health check falhou: {response.status_code}")
            return False
        
        # Testa endpoint de usuários cadastrados
        response = requests.get(f"{FACIAL_API_URL}/enrolled-users", timeout=5)
        if response.status_code == 200:
            print("   ✅ Endpoint /enrolled-users OK")
            data = response.json()
            users = data.get('users', [])
            print(f"   👥 Usuários cadastrados: {len(users)}")
            for user in users:
                print(f"      - {user.get('nome')} ({user.get('email')}) - {user.get('faces_count')} faces")
        else:
            print(f"   ❌ Endpoint /enrolled-users falhou: {response.status_code}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False

def test_auth_service():
    """Testa o serviço de autenticação."""
    print("🔍 Testando serviço de autenticação...")
    
    try:
        # Testa endpoint de usuários
        response = requests.get(f"{AUTH_API_URL}/auth", timeout=5)
        if response.status_code == 200:
            print("   ✅ Endpoint /auth OK")
            users = response.json()
            print(f"   👥 Usuários no sistema: {len(users)}")
            for user in users[:3]:  # Mostra apenas os primeiros 3
                print(f"      - {user.get('nome')} ({user.get('email')}) - {user.get('perfil')}")
        else:
            print(f"   ❌ Endpoint /auth falhou: {response.status_code}")
            return False
        
        # Testa endpoint de facial auth
        response = requests.get(f"{AUTH_API_URL}/facial-auth/enrolled-users", timeout=5)
        if response.status_code == 200:
            print("   ✅ Endpoint /facial-auth/enrolled-users OK")
            data = response.json()
            users = data.get('users', [])
            print(f"   👥 Usuários com faces: {len(users)}")
        else:
            print(f"   ❌ Endpoint /facial-auth/enrolled-users falhou: {response.status_code}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False

def create_test_image():
    """Cria uma imagem de teste simples."""
    print("🖼️  Criando imagem de teste...")
    
    # Cria uma imagem simples (quadrado azul)
    img = Image.new('RGB', (200, 200), color='blue')
    
    # Converte para base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    print("   ✅ Imagem de teste criada")
    return img_base64

def test_facial_recognition():
    """Testa o reconhecimento facial com imagem de teste."""
    print("🔍 Testando reconhecimento facial...")
    
    try:
        # Cria imagem de teste
        test_image = create_test_image()
        
        # Testa reconhecimento
        response = requests.post(f"{FACIAL_API_URL}/recognize", 
                               json={"image": test_image}, 
                               timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Endpoint /recognize OK")
            data = response.json()
            print(f"   📊 Sucesso: {data.get('success')}")
            print(f"   👤 Reconhecido: {data.get('recognized')}")
            print(f"   💬 Mensagem: {data.get('message')}")
        else:
            print(f"   ❌ Endpoint /recognize falhou: {response.status_code}")
            print(f"   📋 Resposta: {response.text}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False

def test_integration_flow():
    """Testa o fluxo completo de integração."""
    print("🔄 Testando fluxo de integração...")
    
    try:
        # 1. Busca usuários no sistema de auth
        response = requests.get(f"{AUTH_API_URL}/auth", timeout=5)
        if response.status_code != 200:
            print("   ❌ Não foi possível buscar usuários")
            return False
        
        users = response.json()
        if not users:
            print("   ⚠️  Nenhum usuário encontrado no sistema")
            return True
        
        # 2. Pega o primeiro usuário
        test_user = users[0]
        user_id = test_user.get('id')
        user_name = test_user.get('nome')
        
        print(f"   👤 Usuário de teste: {user_name} (ID: {user_id})")
        
        # 3. Cria imagem de teste
        test_image = create_test_image()
        
        # 4. Testa cadastro de face via API de auth
        response = requests.post(f"{AUTH_API_URL}/facial-auth/enroll/{user_id}",
                               json={"image": test_image},
                               timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Cadastro de face via API de auth OK")
            data = response.json()
            print(f"   💬 Mensagem: {data.get('message')}")
        else:
            print(f"   ❌ Cadastro de face falhou: {response.status_code}")
            print(f"   📋 Resposta: {response.text}")
        
        # 5. Testa login facial via API de auth
        response = requests.post(f"{AUTH_API_URL}/facial-auth/login",
                               json={"image": test_image},
                               timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Login facial via API de auth OK")
            data = response.json()
            print(f"   📊 Sucesso: {data.get('success')}")
            if data.get('user'):
                print(f"   👤 Usuário: {data.get('user').get('nome')}")
        else:
            print(f"   ❌ Login facial falhou: {response.status_code}")
            print(f"   📋 Resposta: {response.text}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False

def main():
    """Função principal."""
    print("=" * 60)
    print("🧪 TESTE DE INTEGRAÇÃO - RECONHECIMENTO FACIAL")
    print("=" * 60)
    print()
    
    # Verifica se os serviços estão rodando
    print("🔍 Verificando serviços...")
    
    facial_ok = test_facial_service()
    auth_ok = test_auth_service()
    
    print()
    
    if not facial_ok:
        print("❌ Serviço de reconhecimento facial não está rodando!")
        print("   Execute: python start_integrated_solution.py")
        return
    
    if not auth_ok:
        print("❌ Serviço de autenticação não está rodando!")
        print("   Execute: ./mvnw spring-boot:run no diretório dwe-app-auth-java/")
        return
    
    print("✅ Ambos os serviços estão rodando!")
    print()
    
    # Testa funcionalidades
    print("🧪 Executando testes...")
    
    test_facial_recognition()
    print()
    
    test_integration_flow()
    print()
    
    print("=" * 60)
    print("✅ TESTES CONCLUÍDOS!")
    print("=" * 60)
    print()
    print("📱 Para testar no mobile:")
    print("1. Inicie a aplicação mobile")
    print("2. Use a opção 'Login Facial'")
    print("3. Tire uma foto ou escolha da galeria")
    print()
    print("🔧 Para testar via API:")
    print("1. Use Postman ou curl")
    print("2. Endpoints disponíveis em:")
    print(f"   - Reconhecimento: {FACIAL_API_URL}")
    print(f"   - Autenticação: {AUTH_API_URL}")

if __name__ == "__main__":
    main()
