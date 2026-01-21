# Technical Spec

## Command file
- Path: gpt_command.json
- Format: JSON object with "command" and "params"

### Schema
command: string
params: object (optional)

## Polling
- Interval: 1.0 seconds
- The agent sleeps between polls.

## Command lifecycle
1. read_json_file loads JSON.
2. If valid, clear_command_file writes {}.
3. Dispatch to handler.

## Validation rules
- Root must be an object.
- command must be a string.
- params must be an object if present.

## Standard output
- Status and warnings are printed to stdout.

## Optional dependencies
- psutil adds RAM and uptime details for system_check.
