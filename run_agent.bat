@echo off
cd /d "%~dp0"

REM Запускає LocalAgent у фоновому режимі (без консолі).
REM Для зупинки завершіть процес pythonw.exe або через Диспетчер завдань.
start "" pythonw agent.py
