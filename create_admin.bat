@echo off
echo ============================================================
echo   Criar Usuario Administrador - ARQManager
echo ============================================================
echo.

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Criando usuario administrador...
python create_admin.py

echo.
pause
