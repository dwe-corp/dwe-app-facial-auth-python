#!/usr/bin/env python3
"""
Script de configuração para a solução integrada de reconhecimento facial.
Este script configura o ambiente e prepara os dados necessários para a integração.
"""

import os
import sys
import subprocess
import yaml
import shutil
from pathlib import Path

def create_directories():
    """Cria os diretórios necessários."""
    print("📁 Criando diretórios necessários...")
    
    directories = [
        'faces',
        'encodings',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ {directory}/")
    
    print()

def install_dependencies():
    """Instala as dependências Python."""
    print("📦 Instalando dependências Python...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("   ✅ Dependências instaladas com sucesso")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Erro ao instalar dependências: {e}")
        print(f"   📋 Saída: {e.stdout}")
        print(f"   📋 Erro: {e.stderr}")
        return False
    
    print()
    return True

def update_config():
    """Atualiza o arquivo de configuração para integração."""
    print("⚙️  Atualizando configuração...")
    
    config_path = "config.yaml"
    
    # Carrega configuração existente
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}
    
    # Adiciona configurações de integração
    config['integration'] = {
        'auth_api_url': 'http://localhost:8080',
        'facial_api_url': 'http://localhost:5000',
        'mobile_api_url': 'http://192.168.0.14:8080'
    }
    
    config['api_server'] = {
        'host': '0.0.0.0',
        'port': 5000,
        'debug': True,
        'cors_enabled': True
    }
    
    # Salva configuração atualizada
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)
    
    print("   ✅ Configuração atualizada")
    print()

def create_startup_scripts():
    """Cria scripts de inicialização para diferentes sistemas operacionais."""
    print("📜 Criando scripts de inicialização...")
    
    # Script para Windows
    windows_script = """@echo off
echo Iniciando solucao integrada de reconhecimento facial...
python start_integrated_solution.py
pause
"""
    
    with open("start_windows.bat", "w") as f:
        f.write(windows_script)
    
    # Script para Linux/Mac
    unix_script = """#!/bin/bash
echo "Iniciando solução integrada de reconhecimento facial..."
python3 start_integrated_solution.py
"""
    
    with open("start_unix.sh", "w") as f:
        f.write(unix_script)
    
    # Torna o script Unix executável
    os.chmod("start_unix.sh", 0o755)
    
    print("   ✅ start_windows.bat criado")
    print("   ✅ start_unix.sh criado")
    print()

def create_documentation():
    """Cria documentação de integração."""
    print("📚 Criando documentação...")
    
    integration_doc = """# Integração de Reconhecimento Facial - Entrega 4

## Visão Geral

Este projeto evolui a POC da Entrega 3 para uma solução integrada que conecta o reconhecimento facial com os sistemas de autenticação e mobile.

## Arquitetura da Solução

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile App    │    │  Auth Service   │    │ Facial Service  │
│   (React)       │◄──►│    (Java)       │◄──►│   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Componentes

### 1. Serviço de Reconhecimento Facial (Python)
- **Porta**: 5000
- **Arquivo**: `src/api_server.py`
- **Funcionalidades**:
  - Reconhecimento facial via API REST
  - Cadastro de faces de usuários
  - Integração com sistema de autenticação

### 2. Serviço de Autenticação (Java)
- **Porta**: 8080
- **Novos endpoints**:
  - `POST /facial-auth/login` - Login via reconhecimento facial
  - `POST /facial-auth/enroll/{userId}` - Cadastro de face
  - `GET /facial-auth/enrolled-users` - Lista usuários cadastrados
  - `DELETE /facial-auth/delete/{userName}` - Remove face

### 3. Aplicação Mobile (React Native)
- **Novas telas**:
  - `FacialLoginScreen` - Login via reconhecimento facial
- **Novos serviços**:
  - `facialAuthService.ts` - Integração com APIs de reconhecimento

## Como Executar

### Pré-requisitos
1. Python 3.10+
2. Java 17+
3. Node.js 18+
4. Câmera ou dispositivo com câmera

### Passo a Passo

1. **Configure o ambiente Python**:
   ```bash
   cd dwe-app-facial-auth-python
   python setup_integration.py
   ```

2. **Inicie o serviço de autenticação Java**:
   ```bash
   cd dwe-app-auth-java
   ./mvnw spring-boot:run
   ```

3. **Inicie o serviço de reconhecimento facial**:
   ```bash
   cd dwe-app-facial-auth-python
   python start_integrated_solution.py
   ```

4. **Inicie a aplicação mobile**:
   ```bash
   cd dwe-app-mobile-react
   npm start
   ```

## Testando a Integração

1. **Cadastre um usuário** no sistema de autenticação
2. **Cadastre a face** do usuário via API ou interface
3. **Teste o login facial** no aplicativo mobile
4. **Verifique os logs** de acesso no sistema

## Endpoints da API

### Reconhecimento Facial (Porta 5000)

- `GET /health` - Health check
- `POST /recognize` - Reconhece face na imagem
- `POST /enroll` - Cadastra face de usuário
- `GET /enrolled-users` - Lista usuários cadastrados
- `DELETE /delete-user/<nome>` - Remove face do usuário

### Autenticação (Porta 8080)

- `POST /facial-auth/login` - Login via reconhecimento facial
- `POST /facial-auth/enroll/{userId}` - Cadastro de face
- `GET /facial-auth/enrolled-users` - Lista usuários cadastrados
- `DELETE /facial-auth/delete/{userName}` - Remove face

## Formato das Requisições

### Login Facial
```json
POST /facial-auth/login
{
  "image": "base64_encoded_image"
}
```

### Cadastro de Face
```json
POST /facial-auth/enroll/{userId}
{
  "image": "base64_encoded_image"
}
```

## Logs e Monitoramento

- Logs do serviço Python: console
- Logs do serviço Java: console
- Logs do mobile: console do React Native

## Troubleshooting

1. **Serviço não inicia**: Verifique se as portas 5000 e 8080 estão livres
2. **Face não reconhecida**: Verifique se a face foi cadastrada corretamente
3. **Erro de conexão**: Verifique se todos os serviços estão rodando
4. **Permissão de câmera**: Verifique as permissões no dispositivo mobile

## Próximos Passos

- Implementar autenticação JWT para APIs
- Adicionar criptografia para dados biométricos
- Implementar logs de auditoria
- Adicionar métricas de performance
"""
    
    with open("INTEGRATION_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(integration_doc)
    
    print("   ✅ INTEGRATION_GUIDE.md criado")
    print()

def main():
    """Função principal."""
    print("=" * 60)
    print("🔧 CONFIGURAÇÃO DA SOLUÇÃO INTEGRADA")
    print("=" * 60)
    print()
    
    # Verifica se está no diretório correto
    if not os.path.exists("src/api_server.py"):
        print("❌ Execute este script no diretório dwe-app-facial-auth-python/")
        sys.exit(1)
    
    # Executa configuração
    create_directories()
    
    if not install_dependencies():
        print("❌ Falha na instalação de dependências. Verifique os erros acima.")
        sys.exit(1)
    
    update_config()
    create_startup_scripts()
    create_documentation()
    
    print("=" * 60)
    print("✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print()
    print("📋 Próximos passos:")
    print("1. Inicie o serviço de autenticação Java (porta 8080)")
    print("2. Execute: python start_integrated_solution.py")
    print("3. Inicie a aplicação mobile")
    print("4. Teste o login facial!")
    print()
    print("📚 Consulte INTEGRATION_GUIDE.md para mais detalhes")

if __name__ == "__main__":
    main()
