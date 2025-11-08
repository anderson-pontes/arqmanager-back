@echo off
echo ============================================================
echo   Iniciando ARQManager API
echo ============================================================
echo.

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Iniciando servidor...
echo API disponivel em: http://localhost:8000
echo Documentacao em: http://localhost:8000/docs
echo.
echo Pressione CTRL+C para parar o servidor
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
