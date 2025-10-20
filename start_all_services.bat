@echo off
echo ========================================
echo 🚀 INICIANDO SOLUÇÃO INTEGRADA COMPLETA
echo ========================================
echo.

echo 📱 1. Aplicação Mobile (já rodando)
echo    - Expo: http://localhost:8081
echo    - QR Code para Expo Go
echo.

echo 🔐 2. Servidor de Reconhecimento Facial
echo    - Iniciando na porta 5000...
start "Facial Recognition API" cmd /k "cd /d D:\Desktop\sprintiot\dwe-app-facial-auth-python && python -m src.api_server"
timeout /t 3 /nobreak >nul

echo.
echo ☕ 3. Servidor de Autenticação Java
echo    - Iniciando na porta 8080...
start "Auth Service" cmd /k "cd /d D:\Desktop\sprintiot\dwe-app-auth-java && ./mvnw spring-boot:run"
timeout /t 3 /nobreak >nul

echo.
echo ✅ TODOS OS SERVIÇOS INICIADOS!
echo.
echo 📊 Status dos Serviços:
echo    - Mobile App: http://localhost:8081
echo    - Facial API: http://localhost:5000
echo    - Auth API: http://localhost:8080
echo.
echo 🧪 Para testar:
echo    1. Abra http://localhost:8081 no navegador
echo    2. Use a opção "Login Facial"
echo    3. Teste o reconhecimento facial
echo.
echo 📱 Para testar no celular:
echo    1. Instale o app "Expo Go"
echo    2. Escaneie o QR Code
echo    3. Teste o login facial
echo.
pause
