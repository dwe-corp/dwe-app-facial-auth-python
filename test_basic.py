#!/usr/bin/env python3
"""
Teste básico para verificar se a aplicação está funcionando.
"""

import sys
import os

def test_imports():
    """Testa se as dependências estão instaladas."""
    print("🔍 Testando dependências...")
    
    try:
        import cv2
        print("   ✅ OpenCV instalado")
    except ImportError:
        print("   ❌ OpenCV não instalado")
        return False
    
    try:
        import numpy as np
        print("   ✅ NumPy instalado")
    except ImportError:
        print("   ❌ NumPy não instalado")
        return False
    
    try:
        import yaml
        print("   ✅ PyYAML instalado")
    except ImportError:
        print("   ❌ PyYAML não instalado")
        return False
    
    try:
        import face_recognition
        print("   ✅ face_recognition instalado")
    except ImportError:
        print("   ❌ face_recognition não instalado")
        return False
    
    return True

def test_files():
    """Testa se os arquivos necessários existem."""
    print("🔍 Testando arquivos...")
    
    files_to_check = [
        "src/main.py",
        "src/api_server.py",
        "src/detectors.py",
        "src/utils.py",
        "config.yaml",
        "src/models/haarcascade_frontalface_default.xml"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} não encontrado")
            all_exist = False
    
    return all_exist

def test_directories():
    """Testa se os diretórios necessários existem."""
    print("🔍 Testando diretórios...")
    
    dirs_to_check = [
        "faces",
        "encodings",
        "src/models"
    ]
    
    all_exist = True
    for dir_path in dirs_to_check:
        if os.path.exists(dir_path):
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ❌ {dir_path}/ não encontrado")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 50)
    print("🧪 TESTE BÁSICO DA APLICAÇÃO")
    print("=" * 50)
    print()
    
    imports_ok = test_imports()
    print()
    
    files_ok = test_files()
    print()
    
    dirs_ok = test_directories()
    print()
    
    if imports_ok and files_ok and dirs_ok:
        print("🎉 Tudo está configurado corretamente!")
        print()
        print("📱 Como testar:")
        print("1. Aplicação original (câmera local):")
        print("   python -m src.main")
        print()
        print("2. Servidor de APIs:")
        print("   python src/api_server.py")
        print()
        print("3. Teste no navegador:")
        print("   http://localhost:5000/health")
    else:
        print("❌ Alguns problemas foram encontrados")
        print("   Instale as dependências: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
