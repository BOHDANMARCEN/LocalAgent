@echo off
setlocal
cd /d "%~dp0"

REM Run LocalAgent with a custom interval (seconds). Default is 1.0.
set "INTERVAL=%~1"
if "%INTERVAL%"=="" set "INTERVAL=1.0"
if not "%~1"=="" shift

python agent.py run --command-file gpt_command.json --interval %INTERVAL% %*
