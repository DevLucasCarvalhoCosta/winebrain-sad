@echo off
echo.
echo ============================================================
echo    WINEBRAIN - INSTALACAO DO BACKEND
echo ============================================================
echo.

cd backend

echo [1/3] Criando ambiente virtual Python...
python -m venv venv

echo.
echo [2/3] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo [3/3] Instalando dependencias...
pip install -r requirements.txt

echo.
echo ============================================================
echo    INSTALACAO CONCLUIDA!
echo ============================================================
echo.
echo Proximos passos:
echo 1. Processar dados: python load_data.py
echo 2. Treinar modelo: python models\churn_model.py
echo 3. Iniciar servidor: python run.py
echo.
pause
