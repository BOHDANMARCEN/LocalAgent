@echo off
setlocal
cd /d "%~dp0"

REM Run LocalAgent once and exit. Pass extra args after this script if needed.
python agent.py run --command-file gpt_command.json --once %*
