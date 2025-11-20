@echo off
echo.
echo ============================================================
echo    WINEBRAIN - INICIANDO BACKEND
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

echo Iniciando servidor FastAPI...
echo.
echo Servidor disponivel em: http://localhost:8000
echo Documentacao: http://localhost:8000/docs
echo.

python run.py
