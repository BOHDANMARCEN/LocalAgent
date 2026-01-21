# CLI

LocalAgent includes a simple command line interface in `agent.py`.

## Run the agent
```powershell
python agent.py
python agent.py run --interval 1
python agent.py run --once
```

## Send commands
```powershell
python agent.py send message --param text=Hello
python agent.py send open_app --param path=notepad
python agent.py send scan_defender --param path=C:/Downloads
python agent.py send delete_file --params-json "{\"path\":\"C:/Temp/test.txt\",\"confirm\":true}"
```

## Validate JSON
```powershell
python agent.py validate --command-file gpt_command.json
python agent.py validate --json "{\"command\":\"message\",\"params\":{\"text\":\"Hi\"}}"
```

## List commands and examples
```powershell
python agent.py commands
python agent.py commands --json
python agent.py example system_check --pretty
```

## Notes on params
- `--params-json` expects a JSON object.
- `--param key=value` parses values as JSON when possible.
  For strings, pass plain text; for booleans or numbers, pass JSON values.
