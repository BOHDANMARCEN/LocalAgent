@echo off
setlocal
cd /d "%~dp0"

REM Start LocalAgent loop. Pass extra args after this script if needed.
python agent.py run --command-file gpt_command.json %*
