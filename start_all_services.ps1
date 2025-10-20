# Script PowerShell para iniciar todos os serviços
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 INICIANDO SOLUÇÃO INTEGRADA COMPLETA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📱 1. Aplicação Mobile (já rodando)" -ForegroundColor Green
Write-Host "   - Expo: http://localhost:8081" -ForegroundColor Yellow
Write-Host "   - QR Code para Expo Go" -ForegroundColor Yellow
Write-Host ""

Write-Host "🔐 2. Servidor de Reconhecimento Facial" -ForegroundColor Green
Write-Host "   - Iniciando na porta 5000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'D:\Desktop\sprintiot\dwe-app-facial-auth-python'; python -m src.api_server"
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "☕ 3. Servidor de Autenticação Java" -ForegroundColor Green
Write-Host "   - Iniciando na porta 8080..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'D:\Desktop\sprintiot\dwe-app-auth-java'; ./mvnw spring-boot:run"
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "✅ TODOS OS SERVIÇOS INICIADOS!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Status dos Serviços:" -ForegroundColor Cyan
Write-Host "   - Mobile App: http://localhost:8081" -ForegroundColor White
Write-Host "   - Facial API: http://localhost:5000" -ForegroundColor White
Write-Host "   - Auth API: http://localhost:8080" -ForegroundColor White
Write-Host ""
Write-Host "🧪 Para testar:" -ForegroundColor Cyan
Write-Host "   1. Abra http://localhost:8081 no navegador" -ForegroundColor White
Write-Host "   2. Use a opção 'Login Facial'" -ForegroundColor White
Write-Host "   3. Teste o reconhecimento facial" -ForegroundColor White
Write-Host ""
Write-Host "📱 Para testar no celular:" -ForegroundColor Cyan
Write-Host "   1. Instale o app 'Expo Go'" -ForegroundColor White
Write-Host "   2. Escaneie o QR Code" -ForegroundColor White
Write-Host "   3. Teste o login facial" -ForegroundColor White
Write-Host ""
Read-Host "Pressione Enter para continuar"
