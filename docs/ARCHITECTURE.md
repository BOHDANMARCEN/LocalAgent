# Architecture

## Components
- Command file: gpt_command.json
- Agent loop: agent.py polling loop
- Command handlers: Python functions in COMMANDS map

## Data flow
1. Writer places JSON in gpt_command.json.
2. Agent reads JSON and validates structure.
3. Agent clears the file to {} to avoid replays.
4. Agent dispatches to a whitelisted handler.
5. Handler performs the local action.

## Trust boundaries
- Only local filesystem access.
- No network listeners.
- Only whitelisted commands are callable.

## Error handling
- Invalid JSON is ignored.
- Unknown commands are rejected.
- Handler errors are reported to stdout.

## Extensibility
- Add a handler function.
- Register it in COMMANDS.
- Document it in docs/COMMANDS.md.
