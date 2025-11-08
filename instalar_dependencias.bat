@echo off
echo ============================================================
echo   Instalando Dependencias - ARQManager Backend
echo ============================================================
echo.

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Instalando dependencias do requirements.txt...
pip install -r requirements.txt

echo.
echo ============================================================
echo   Instalacao concluida!
echo ============================================================
echo.
echo Proximo passo: python migrar.py
echo.
pause
