@echo off
REM ============================================
REM WineBrain - Enviar Dados para Servidor UEG
REM ============================================

echo.
echo ============================================
echo    WINEBRAIN - ENVIAR DADOS PARA SERVIDOR
echo ============================================
echo.

set SERVIDOR=usuario@200.137.241.42
set PORTA=8740
set DESTINO=~/winebrain-sad/data

echo Enviando dados processados para o servidor UEG...
echo Servidor: %SERVIDOR%
echo Porta: %PORTA%
echo.

REM Verificar se os dados existem
if not exist "data\processed\clientes_agregado.csv" (
    echo ERRO: Dados nao encontrados!
    echo Execute process_data.bat primeiro
    pause
    exit /b 1
)

echo [1/5] Enviando clientes_agregado.csv...
scp -P %PORTA% data\processed\clientes_agregado.csv %SERVIDOR%:%DESTINO%/processed/

echo [2/5] Enviando summary.json...
scp -P %PORTA% data\processed\summary.json %SERVIDOR%:%DESTINO%/processed/

echo [3/5] Enviando compras.csv...
scp -P %PORTA% data\raw\compras.csv %SERVIDOR%:%DESTINO%/raw/

echo [4/5] Enviando produtos.csv...
scp -P %PORTA% data\raw\produtos.csv %SERVIDOR%:%DESTINO%/raw/

echo [5/5] Enviando modelo ML...
scp -P %PORTA% data\models\churn_model.pkl %SERVIDOR%:%DESTINO%/models/

echo.
echo ============================================
echo    DADOS ENVIADOS COM SUCESSO!
echo ============================================
echo.
echo Proximos passos:
echo 1. SSH no servidor: ssh -p %PORTA% %SERVIDOR%
echo 2. Executar deploy: cd winebrain-sad ^&^& ./deploy-ueg.sh
echo.
pause
