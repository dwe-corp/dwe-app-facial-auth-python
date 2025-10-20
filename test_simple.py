#!/usr/bin/env python3
"""
Teste simples para verificar se os serviços estão funcionando.
"""

import requests
import time

def test_facial_service():
    """Testa o serviço de reconhecimento facial."""
    print("🔍 Testando serviço de reconhecimento facial...")
    
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Serviço de reconhecimento facial está rodando!")
            data = response.json()
            print(f"   📊 Status: {data.get('status')}")
            return True
        else:
            print(f"   ❌ Serviço retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False

def test_auth_service():
    """Testa o serviço de autenticação."""
    print("🔍 Testando serviço de autenticação...")
    
    try:
        response = requests.get("http://localhost:8080/auth", timeout=5)
        if response.status_code == 200:
            print("   ✅ Serviço de autenticação está rodando!")
            users = response.json()
            print(f"   👥 Usuários no sistema: {len(users)}")
            return True
        else:
            print(f"   ❌ Serviço retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False

def main():
    print("=" * 50)
    print("🧪 TESTE SIMPLES DOS SERVIÇOS")
    print("=" * 50)
    print()
    
    facial_ok = test_facial_service()
    print()
    
    auth_ok = test_auth_service()
    print()
    
    if facial_ok and auth_ok:
        print("🎉 Ambos os serviços estão funcionando!")
        print()
        print("📱 Próximos passos:")
        print("1. Inicie a aplicação mobile")
        print("2. Use a opção 'Login Facial'")
        print("3. Teste o reconhecimento facial")
    elif facial_ok:
        print("⚠️  Apenas o serviço de reconhecimento facial está rodando")
        print("   Para testar a integração completa, inicie também o serviço de autenticação Java")
    elif auth_ok:
        print("⚠️  Apenas o serviço de autenticação está rodando")
        print("   Para testar a integração completa, inicie também o serviço de reconhecimento facial")
    else:
        print("❌ Nenhum serviço está rodando")
        print("   Inicie os serviços primeiro")

if __name__ == "__main__":
    main()
