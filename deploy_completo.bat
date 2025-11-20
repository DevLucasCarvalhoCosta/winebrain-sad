@echo off
REM ============================================
REM WineBrain - Preparar e Fazer Deploy
REM Automatiza todo o processo
REM ============================================

echo.
echo ============================================
echo    WINEBRAIN - DEPLOY COMPLETO
echo ============================================
echo.

REM 1. Processar dados
echo [1/4] Processando dados localmente...
call process_data.bat
if errorlevel 1 (
    echo ERRO: Falha ao processar dados
    pause
    exit /b 1
)

REM 2. Git add e commit
echo.
echo [2/4] Fazendo commit no GitHub...
git add .
git status
echo.
set /p COMMIT_MSG="Digite a mensagem do commit: "
git commit -m "%COMMIT_MSG%"
git push origin main

if errorlevel 1 (
    echo AVISO: Falha no git push. Continue manualmente?
    pause
)

REM 3. Enviar dados
echo.
echo [3/4] Enviando dados para o servidor...
call enviar_dados_servidor.bat

REM 4. Instruções finais
echo.
echo [4/4] Deploy automatizado preparado!
echo.
echo ============================================
echo    PROXIMO PASSO - NO SERVIDOR
echo ============================================
echo.
echo Execute no servidor:
echo.
echo   ssh -p 8740 usuario@200.137.241.42
echo   cd winebrain-sad
echo   git pull
echo   chmod +x deploy-ueg.sh
echo   ./deploy-ueg.sh
echo.
echo Ou copie e cole este comando completo:
echo.
echo ssh -p 8740 usuario@200.137.241.42 "cd winebrain-sad ^&^& git pull ^&^& chmod +x deploy-ueg.sh ^&^& ./deploy-ueg.sh"
echo.
pause
