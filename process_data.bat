@echo off
echo.
echo ============================================================
echo    WINEBRAIN - PROCESSAMENTO DE DADOS
echo ============================================================
echo.

cd backend

if not exist "venv\Scripts\activate.bat" (
    echo ERRO: Ambiente virtual nao encontrado!
    echo Execute install.bat primeiro
    pause
    exit
)

call venv\Scripts\activate.bat

echo [1/2] Processando dados do Excel...
python load_data.py

echo.
echo [2/2] Treinando modelo de Machine Learning...
python models\churn_model.py

echo.
echo [3/3] Copiando arquivos para backend\app_data (deploy)...

cd ..

if not exist "backend\app_data\raw" mkdir backend\app_data\raw
if not exist "backend\app_data\processed" mkdir backend\app_data\processed
if not exist "backend\app_data\models" mkdir backend\app_data\models

copy data\raw\clientes.csv backend\app_data\raw\clientes.csv >nul
copy data\raw\compras.csv backend\app_data\raw\compras.csv >nul
copy data\raw\produtos.csv backend\app_data\raw\produtos.csv >nul
copy data\processed\clientes_agregado.csv backend\app_data\processed\clientes_agregado.csv >nul
copy data\processed\summary.json backend\app_data\processed\summary.json >nul
copy data\models\churn_model.pkl backend\app_data\models\churn_model.pkl >nul

echo Arquivos copiados para deploy!

echo.
echo ============================================================
echo    PROCESSAMENTO CONCLUIDO!
echo ============================================================
echo.
echo Dados processados e modelo treinado com sucesso!
echo Arquivos preparados para deploy na Vercel!
echo Agora voce pode iniciar o servidor com: start_backend.bat
echo.
pause
