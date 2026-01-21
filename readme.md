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
    git clone https://github.com/BOHDANMARCEN/LocalAgent
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

The agent will start, create `gpt_command.json` and `agent.log` if they don't exist, and begin watching the command file. The `run_agent.bat` script is also available for a quick launch.

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
- **Params**: `{"text": "your message"}`

### `open_app`
Launches an application.
- **Params**: `{"path": "path_to_app.exe"}`

### `run_powershell_script`
Executes a PowerShell script string.
- **Params**: `{"script": "Get-Process"}`

### `system_check`
Logs a summary of system information (OS, CPU, memory, disk).
- **Params**: None

### `delete_file`
Deletes a file. **Requires confirmation.**
- **Params**: `{"path": "/path/to/file", "confirm": true}`

### `kill_process_by_name`
Terminates a process by name.
- **Params**: `{"name": "process_name.exe"}`

### `create_file`
Creates a new file, optionally with content.
- **Params**: `{"path": "/path/to/file", "content": "initial content"}`

### `create_folder`
Creates a new directory.
- **Params**: `{"path": "/path/to/folder"}`

### `move_file`
Moves or renames a file.
- **Params**: `{"from_path": "/src", "to_path": "/dest"}`

### `copy_file`
Copies a file.
- **Params**: `{"from_path": "/src", "to_path": "/dest"}`

### `rename_file`
Renames a file.
- **Params**: `{"path": "/path/to/file", "new_name": "new_name.txt"}`

### `list_dir`
Logs the contents of a directory.
- **Params**: `{"path": "/path/to/dir"}`

### `read_file`
Logs the content of a file.
- **Params**: `{"path": "/path/to/file"}`

### `write_file`
Writes content to a file, overwriting existing content.
- **Params**: `{"path": "/path/to/file", "content": "new content"}`

### `append_file`
Appends content to the end of a file.
- **Params**: `{"path": "/path/to/file", "content": "appended content"}`

### `run_instrukey`
Runs an InstruKey executable.
- **Params**: `{"path": "C:/Tools/InstruKey/InstruKey.exe"}`

### `scan_defender`
Starts a Windows Defender scan on a file or folder.
- **Params**: `{"path": "C:/path/to/scan"}`

### `list_processes`
Logs a list of all running processes.
- **Params**: None

### `start_process`
Starts a new process.
- **Params**: `{"path": "process.exe", "args": "--arg1"}`

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