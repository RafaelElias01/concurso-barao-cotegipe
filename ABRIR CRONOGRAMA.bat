@echo off
chcp 65001 >nul
title Cronograma Barão de Cotegipe (RS) – Odontólogo/PSF
if not exist "%~dp0cronograma\servidor.py" goto incompleta
cd /d "%~dp0cronograma"
set "PYTHONIOENCODING=utf-8"
set "PY="
if exist "%~dp0ferramentas\python\python.exe" set "PY=%~dp0ferramentas\python\python.exe"
if not defined PY ( python --version >nul 2>&1 && set "PY=python" )
if not defined PY ( py --version >nul 2>&1 && set "PY=py" )
if not defined PY goto sem_python

echo ============================================================
echo  CRONOGRAMA DE ESTUDOS – BARÃO DE COTEGIPE (RS)
echo  Cargo: Odontólogo / PSF (Instituto DOM) – Prova: 22/11/2026
echo ------------------------------------------------------------
echo  O navegador vai abrir sozinho.
echo  DEIXE ESTA JANELA ABERTA enquanto estuda.
echo  Terminou? Feche esta janela. Seu progresso já está salvo.
echo ============================================================
echo.
"%PY%" servidor.py %*
echo.
echo O cronograma foi desligado.
pause
exit /b

:sem_python
echo [AVISO] Python não foi encontrado no sistema.
echo Abrindo o cronograma diretamente no navegador padrão...
start "" "%~dp0cronograma\index.html"
echo.
echo O cronograma foi aberto diretamente no navegador.
echo Seu progresso ficará salvo no navegador deste computador.
echo Para salvar em arquivo texto (progresso.json), instale o Python.
echo.
pause
exit /b

:incompleta
echo A pasta do projeto parece incompleta (servidor.py não foi encontrado).
echo Verifique se os arquivos estão na pasta cronograma\.
echo Veja o README.md (COMECE AQUI).
echo.
pause
