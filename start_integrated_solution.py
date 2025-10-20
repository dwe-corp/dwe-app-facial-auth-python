#!/usr/bin/env python3
"""
Script para iniciar a solução integrada de reconhecimento facial.
Este script inicia o servidor de reconhecimento facial e verifica a conectividade
com os outros serviços da aplicação.
"""

import subprocess
import time
import requests
import sys
import os
from threading import Thread

def check_service_health(url, service_name, timeout=5):
    """Verifica se um serviço está rodando."""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {service_name} está rodando em {url}")
            return True
        else:
            print(f"❌ {service_name} retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {service_name} não está acessível: {e}")
        return False

def start_facial_recognition_service():
    """Inicia o serviço de reconhecimento facial."""
    print("🚀 Iniciando serviço de reconhecimento facial...")
    try:
        # Muda para o diretório do projeto
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Inicia o servidor Flask
        subprocess.run([sys.executable, "src/api_server.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar serviço de reconhecimento facial: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Serviço de reconhecimento facial interrompido pelo usuário")
        sys.exit(0)

def main():
    """Função principal."""
    print("=" * 60)
    print("🔐 SOLUÇÃO INTEGRADA DE RECONHECIMENTO FACIAL")
    print("=" * 60)
    print()
    
    # Verifica se as dependências estão instaladas
    print("📦 Verificando dependências...")
    try:
        import flask
        import cv2
        import face_recognition
        import requests
        print("✅ Todas as dependências estão instaladas")
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("Execute: pip install -r requirements.txt")
        sys.exit(1)
    
    print()
    
    # Verifica conectividade com outros serviços
    print("🔍 Verificando conectividade com outros serviços...")
    
    auth_service_ok = check_service_health("http://localhost:8080/auth", "Serviço de Autenticação")
    
    if not auth_service_ok:
        print()
        print("⚠️  ATENÇÃO: O serviço de autenticação Java não está rodando!")
        print("   Para iniciar o serviço de autenticação:")
        print("   1. Navegue até dwe-app-auth-java/")
        print("   2. Execute: ./mvnw spring-boot:run")
        print("   3. Aguarde o serviço iniciar na porta 8080")
        print()
        print("🔄 Continuando com o serviço de reconhecimento facial...")
        print("   (Algumas funcionalidades podem não funcionar sem o serviço de auth)")
    
    print()
    
    # Inicia o serviço de reconhecimento facial
    print("🎯 Iniciando serviço de reconhecimento facial...")
    print("   URL: http://localhost:5000")
    print("   Endpoints disponíveis:")
    print("   - GET  /health - Health check")
    print("   - POST /recognize - Reconhecimento facial")
    print("   - POST /enroll - Cadastro de face")
    print("   - GET  /enrolled-users - Lista usuários cadastrados")
    print("   - DELETE /delete-user/<nome> - Remove face do usuário")
    print()
    print("📱 Para testar no mobile:")
    print("   1. Certifique-se de que o app mobile está rodando")
    print("   2. Use a opção 'Login Facial' na tela de login")
    print()
    print("🛑 Pressione Ctrl+C para parar o serviço")
    print("=" * 60)
    
    start_facial_recognition_service()

if __name__ == "__main__":
    main()
