@echo off
echo.
echo ============================================================
echo    WINEBRAIN - INICIANDO FRONTEND
echo ============================================================
echo.

cd frontend

if not exist "node_modules" (
    echo ERRO: Dependencias nao instaladas!
    echo Execute install.bat primeiro
    pause
    exit
)

echo Iniciando aplicacao React...
echo.
echo Aplicacao disponivel em: http://localhost:3000
echo.

call npm run dev
