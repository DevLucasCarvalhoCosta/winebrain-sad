@echo off
echo.
echo ============================================================
echo    WINEBRAIN - INSTALACAO DO FRONTEND
echo ============================================================
echo.

cd frontend

echo [1/1] Instalando dependencias NPM...
call npm install

echo.
echo ============================================================
echo    INSTALACAO CONCLUIDA!
echo ============================================================
echo.
echo Para iniciar o frontend: npm run dev
echo.
pause
