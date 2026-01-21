# 🤖 LocalAgent

> **A secure, local-first JSON command runner for Windows, designed for AI-driven automation.**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey.svg)](https://www.microsoft.com/windows)

---

## 📖 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Installation](#-installation)
- [How to Run](#-how-to-run)
- [JSON Command Format](#-json-command-format)
- [Command Reference](#-command-reference)
- [Logging](#-logging)
- [Development](#-development)
- [License](#-license)

---

## 🎯 About

**LocalAgent** is a lightweight and secure daemon that runs on your Windows machine, executing whitelisted commands sent via a simple JSON file. It acts as a safe bridge between AI models (like GPT) and your local environment, allowing you to automate tasks without exposing your machine to the internet.

The agent periodically polls `gpt_command.json`. When a valid command is found, it executes the corresponding action, logs the result, and clears the file to prevent re-execution.

---

## ✨ Features

- **🔒 Secure by Design**: Only explicitly whitelisted commands can be executed. There is no `eval()` or arbitrary code execution.
- **📄 Simple JSON Interface**: Interact with the agent by writing commands to a local JSON file.
- ** backward-compatible**: Supports both the new `params` object and the old flat structure for parameters.
- **🛡️ Hardened Commands**: Critical operations like file deletion and process killing have built-in safety checks.
- **📝 Robust Logging**: All actions, warnings, and errors are logged to `agent.log` for easy auditing.
- **🔧 Configurable**: Set the polling interval via command-line arguments.

---

## 🚀 Installation

### Prerequisites
- **OS**: Windows 10/11
- **Python**: 3.10 or higher

### Steps

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/LocalAgent.git
    cd LocalAgent
    ```

2.  **Install Dependencies**:
    While the agent is designed to be lightweight, some commands for process management require `psutil`.
    ```bash
    pip install psutil
    ```

---

## 🏃 How to Run

Run the agent from your terminal:

```bash
python agent.py
```

The agent will start, create `gpt_command.json` and `agent.log` if they don't exist, and begin watching the command file.

### Customizing the Poll Interval

You can change how frequently the agent checks the command file using the `--poll-interval` argument. For example, to check every 5 seconds:

```bash
python agent.py --poll-interval 5.0
```

---

## 📦 JSON Command Format

To execute a command, write a JSON object to the `gpt_command.json` file.

### Standard Format (Recommended)

The agent expects a JSON object with a `command` and an optional `params` object.

```json
{
  "command": "some_command_name",
  "params": {
    "key1": "value1",
    "key2": 123
  }
}
```

### Backward-Compatible Format

For convenience, the agent also supports a flatter structure. If the `params` key is missing, all other keys (except `command`) will be treated as parameters.

This command:
```json
{
  "command": "message",
  "text": "Hello from LocalAgent!"
}
```

...is automatically normalized to:
```json
{
  "command": "message",
  "params": {
    "text": "Hello from LocalAgent!"
  }
}
```

The agent will process the command and then clear the file, waiting for the next instruction.

---

## 📚 Command Reference

The following commands are currently implemented.

### `message`
Logs a message from the AI.
```json
{
  "command": "message",
  "params": {
    "text": "Hello, this is a test message."
  }
}
```

### `open_app`
Launches an application.
```json
{
  "command": "open_app",
  "params": {
    "path": "notepad.exe"
  }
}
```

### `run_powershell_script`
Executes a PowerShell script string. This is useful for running more complex system commands.
```json
{
  "command": "run_powershell_script",
  "params": {
    "script": "Get-Process | Sort-Object CPU -Descending | Select-Object -First 5"
  }
}
```

### `system_check`
Logs a summary of the system's OS, CPU, memory, and disk information.
```json
{
  "command": "system_check"
}
```

### `delete_file`
Deletes a file. **This command is dangerous.** To prevent accidental deletion, you **must** include `"confirm": true` in the parameters.
```json
{
  "command": "delete_file",
  "params": {
    "path": "C:/path/to/your/file_to_delete.txt",
    "confirm": true
  }
}
```
If `confirm` is not `true`, the agent will log a warning and skip the deletion.

### `kill_process_by_name`
Terminates a running process by its executable name. It includes a denylist to prevent a user from killing critical system processes.
```json
{
  "command": "kill_process_by_name",
  "params": {
    "name": "notepad.exe"
  }
}
```

---

## 📝 Logging

The agent creates and writes to a file named `agent.log` in the same directory. This file contains a timestamped record of:
- Agent startup and shutdown.
- Commands received and their parameters.
- The outcome of each command (success or failure).
- Any warnings (e.g., invalid JSON, unknown commands).
- Detailed error messages with stack traces for debugging.

---

## 🔧 Development

To add a new command:
1.  Define a new function in `agent.py` that takes its parameters as arguments.
2.  Add the function to the `COMMANDS` dictionary, mapping the desired command name (e.g., `"my_new_command"`) to the function object (e.g., `my_new_command`).
3.  Document the new command and its parameters in this `README.md` file.

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.