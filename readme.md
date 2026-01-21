# 🤖 LocalAgent

> **A secure, local-first JSON command runner for Windows with advanced GUI automation, file operations, and system control.**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey.svg)](https://www.microsoft.com/windows)

---

## 📖 Table of Contents

- [About](#-about)
- [Philosophy](#-philosophy)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Command Reference](#-command-reference)
- [Security Model](#-security-model)
- [Examples](#-examples)
- [Architecture](#-architecture)
- [Development](#-development)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 About

**LocalAgent** is a powerful automation framework that bridges the gap between AI assistants (like GPT) and your local Windows environment. It executes JSON-formatted commands with military-grade security, enabling safe automation of GUI interactions, file operations, system management, and development workflows.

### Why LocalAgent?

- **🔒 Security First**: Whitelist-only commands with 4-level permission system
- **🌐 Network-Free**: Completely offline operation (no remote access vulnerabilities)
- **🤖 AI-Ready**: Designed for GPT/Claude integration via simple JSON interface
- **⚡ Lightning Fast**: Minimal overhead, instant command execution
- **🎯 Developer-Friendly**: Clean architecture, extensive documentation, easy to extend

---

## 💭 Philosophy

LocalAgent is built on three core principles:

### 1. **Security Through Simplicity**
```
Only whitelisted commands → No arbitrary code execution → Sleep peacefully
```

### 2. **Local-First Architecture**
```
No network → No remote exploits → Complete control over your data
```

### 3. **Human-AI Collaboration**
```
GPT generates commands → LocalAgent executes safely → Productivity multiplied
```

The project emerged from a simple need: **What if AI could help me automate my desktop?** But with one critical requirement: **It must be absolutely secure.**

---

## ✨ Features

### 🖱️ **Advanced GUI Automation**
- Keyboard control (typing, hotkeys, key holding)
- Mouse operations (click, drag, scroll, smooth movement)
- Image recognition with OpenCV (find UI elements visually)
- Window management (screenshots, active window detection)
- "Human-like" behavior (random delays, smooth curves)

### 📁 **File System Operations**
- CRUD operations (create, read, update, delete)
- Advanced search with filters and recursion
- Archive management (zip/unzip with compression control)
- File comparison and integrity checking
- Safe deletion with recycle bin option

### 🖥️ **System Control**
- Process management (list, start, kill, set priority)
- System monitoring (CPU, RAM, disk, network, GPU)
- Power management (shutdown, restart, sleep, lock)
- Registry operations (read/write with confirmation)
- Scheduled tasks management

### 🔧 **Developer Tools**
- Git integration (status, commit, push, pull, merge)
- Package managers (npm, pip)
- Docker container management
- Virtual environment handling
- Database operations (SQLite)
- Script execution (batch, PowerShell, Python)

### 🎭 **Macro System**
- Complex workflows with multiple steps
- Variables and templating (`{{date}}`, `{{time}}`)
- Conditional logic (if/else)
- Loop support (for/while)
- Error handling and rollback

---

## 🚀 Installation

### Prerequisites
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.10 or higher
- **RAM**: 2GB minimum (4GB recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/LocalAgent.git
cd LocalAgent
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Core dependencies:**
```
pyautogui>=0.9.54       # GUI automation
opencv-python>=4.8.0    # Image recognition
pynput>=1.7.6           # Keyboard/mouse control
psutil>=5.9.0           # System monitoring
pywin32>=306            # Windows API access
Pillow>=10.0.0          # Screenshot handling
```

### Step 3: Verify Installation
```bash
python agent.py
```

You should see:
```
🤖 LocalAgent v1.0.0
📍 Watching: gpt_command.json
✅ Ready to execute commands
```

---

## 🎬 Quick Start

### Example 1: Simple Message
Create `gpt_command.json`:
```json
{
  "command": "message",
  "text": "Hello from LocalAgent! 🚀"
}
```

Run the agent:
```bash
python agent.py
```

### Example 2: GUI Automation
```json
{
  "command": "type_text",
  "text": "This text is typed automatically!",
  "speed": 0.05
}
```

### Example 3: File Operations
```json
{
  "command": "create_file",
  "path": "C:/Temp/test.txt",
  "content": "LocalAgent was here!",
  "encoding": "utf-8"
}
```

### Example 4: Screenshot
```json
{
  "command": "screenshot",
  "path": "C:/Screenshots/desktop.png"
}
```

---

## 📚 Command Reference

### 🖱️ GUI Automation Commands

#### `type_text`
Types text character by character.
```json
{
  "command": "type_text",
  "text": "Hello World",
  "speed": 0.05
}
```
**Parameters:**
- `text` (string): Text to type
- `speed` (float): Delay between characters in seconds

---

#### `press_key`
Presses a single key.
```json
{
  "command": "press_key",
  "key": "enter"
}
```
**Supported keys:** `enter`, `tab`, `esc`, `space`, `backspace`, `delete`, `home`, `end`, `pageup`, `pagedown`, `f1`-`f12`, `up`, `down`, `left`, `right`

---

#### `hotkey`
Executes keyboard shortcuts.
```json
{
  "command": "hotkey",
  "keys": ["ctrl", "c"]
}
```
**Common combinations:**
- `["ctrl", "c"]` - Copy
- `["ctrl", "v"]` - Paste
- `["ctrl", "shift", "esc"]` - Task Manager
- `["win", "r"]` - Run dialog

---

#### `hold_key`
Holds a key for specified duration.
```json
{
  "command": "hold_key",
  "key": "shift",
  "duration": 2
}
```

---

#### `mouse_move`
Moves mouse cursor smoothly.
```json
{
  "command": "mouse_move",
  "x": 500,
  "y": 300,
  "duration": 0.5
}
```

---

#### `mouse_click`
Clicks mouse button.
```json
{
  "command": "mouse_click",
  "button": "left",
  "clicks": 1,
  "x": 500,
  "y": 300
}
```
**Buttons:** `left`, `right`, `middle`

---

#### `mouse_drag`
Drags from one point to another.
```json
{
  "command": "mouse_drag",
  "from_x": 100,
  "from_y": 100,
  "to_x": 500,
  "to_y": 500,
  "duration": 1
}
```

---

#### `scroll`
Scrolls mouse wheel.
```json
{
  "command": "scroll",
  "direction": "down",
  "amount": 3
}
```
**Directions:** `up`, `down`

---

#### `screenshot`
Captures screen or region.
```json
{
  "command": "screenshot",
  "path": "C:/Screenshots/screen.png",
  "region": [0, 0, 1920, 1080]
}
```
**Region format:** `[x, y, width, height]` (optional)

---

#### `screenshot_window`
Captures specific window.
```json
{
  "command": "screenshot_window",
  "window_title": "Notepad",
  "path": "C:/Screenshots/notepad.png"
}
```

---

#### `find_image`
Locates image on screen using OpenCV.
```json
{
  "command": "find_image",
  "template": "C:/Templates/button.png",
  "confidence": 0.8,
  "action": "click"
}
```
**Actions:** `click`, `move`, `highlight`, `none`

---

#### `wait_for_image`
Waits for image to appear.
```json
{
  "command": "wait_for_image",
  "template": "C:/Templates/loading.png",
  "timeout": 30
}
```

---

#### `wait`
Pauses execution.
```json
{
  "command": "wait",
  "seconds": 5
}
```

---

#### `wait_random`
Pauses for random duration (more human-like).
```json
{
  "command": "wait_random",
  "min": 1,
  "max": 3
}
```

---

#### `get_mouse_position`
Returns current mouse coordinates.
```json
{
  "command": "get_mouse_position"
}
```
**Returns:** `{"x": 742, "y": 389}`

---

#### `get_active_window`
Returns active window information.
```json
{
  "command": "get_active_window"
}
```
**Returns:** `{"title": "Notepad", "handle": 12345}`

---

### 📁 File System Commands

#### `open_app`
Opens application or file.
```json
{
  "command": "open_app",
  "path": "notepad.exe"
}
```

---

#### `delete_file`
Deletes file (DANGEROUS - requires confirmation).
```json
{
  "command": "delete_file",
  "path": "C:/Temp/file.txt",
  "confirm": true
}
```

---

### 🖥️ System Commands

#### `system_check`
Returns system information.
```json
{
  "command": "system_check"
}
```
**Returns:**
```json
{
  "os": "Windows 11",
  "cpu": "Intel Core i7-9700K @ 3.60GHz",
  "ram": "16GB",
  "disk": "512GB SSD"
}
```

---

## 🛡️ Security Model

LocalAgent implements a **4-tier security system**:

### Security Levels

#### ✅ SAFE (No confirmation required)
Commands that cannot cause harm:
- `message`
- `get_mouse_position`
- `get_active_window`
- `system_check`

#### ⚠️ MEDIUM (Logged only)
Commands with minimal risk:
- `type_text`
- `mouse_click`
- `screenshot`
- `open_app`

#### 🔴 DANGEROUS (Requires confirmation)
Commands that modify system state:
- `delete_file`
- `kill_process`
- `registry_write`
- `run_script`

#### ☢️ CRITICAL (Double confirmation required)
Commands with severe consequences:
- `delete_folder` (recursive)
- `shutdown`
- `format_drive`

### Confirmation Flow

For DANGEROUS commands:
```
1. Agent detects dangerous command
2. Displays warning with details
3. User must type "YES" to confirm
4. Action is logged with timestamp
5. Command executes
```

### Path Whitelisting

Allowed paths (configurable):
```python
ALLOWED_PATHS = [
    "C:/Users/YourName/Documents",
    "C:/Temp",
    "D:/Projects"
]
```

Blocked paths (system-protected):
```python
BLOCKED_PATHS = [
    "C:/Windows",
    "C:/System32",
    "C:/Program Files"
]
```

---

## 💡 Examples

### Example 1: Auto-Login Workflow
```json
{
  "command": "macro",
  "name": "auto_login",
  "steps": [
    {"command": "open_app", "path": "chrome.exe"},
    {"command": "wait", "seconds": 2},
    {"command": "find_image", "template": "C:/Templates/login_btn.png", "action": "click"},
    {"command": "wait", "seconds": 1},
    {"command": "type_text", "text": "username@email.com"},
    {"command": "press_key", "key": "tab"},
    {"command": "type_text", "text": "SecurePassword123"},
    {"command": "press_key", "key": "enter"},
    {"command": "wait_for_image", "template": "C:/Templates/dashboard.png", "timeout": 10},
    {"command": "message", "text": "✅ Login successful!"}
  ]
}
```

---

### Example 2: Daily Backup
```json
{
  "command": "macro",
  "name": "daily_backup",
  "steps": [
    {"command": "create_folder", "path": "D:/Backups/{{date}}"},
    {"command": "zip_files", "files": ["D:/Projects"], "output": "D:/Backups/{{date}}/projects.zip"},
    {"command": "message", "text": "✅ Backup completed: {{date}}"}
  ],
  "variables": {
    "date": "{{current_date}}"
  }
}
```

---

### Example 3: UI Testing
```json
{
  "command": "macro",
  "name": "test_calculator",
  "steps": [
    {"command": "open_app", "path": "calc.exe"},
    {"command": "wait", "seconds": 2},
    {"command": "find_image", "template": "C:/Tests/num_2.png", "action": "click"},
    {"command": "find_image", "template": "C:/Tests/plus.png", "action": "click"},
    {"command": "find_image", "template": "C:/Tests/num_2.png", "action": "click"},
    {"command": "find_image", "template": "C:/Tests/equals.png", "action": "click"},
    {"command": "screenshot", "path": "C:/Tests/result.png"},
    {"command": "message", "text": "✅ Test completed"}
  ]
}
```

---

### Example 4: Morning Routine
```json
{
  "command": "macro",
  "name": "morning_routine",
  "steps": [
    {"command": "message", "text": "🌅 Good morning! Starting your environment..."},
    {"command": "open_app", "path": "chrome.exe"},
    {"command": "wait", "seconds": 2},
    {"command": "open_app", "path": "code.exe"},
    {"command": "wait", "seconds": 2},
    {"command": "open_app", "path": "spotify.exe"},
    {"command": "wait", "seconds": 1},
    {"command": "set_volume", "level": 30},
    {"command": "message", "text": "✅ Environment ready! Have a productive day!"}
  ]
}
```

---

## 🏗️ Architecture

### Project Structure
```
LocalAgent/
├── agent.py                 # Main execution engine
├── gpt_command.json         # Command input file
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
│
├── docs/
│   ├── ARCHITECTURE.md     # System design
│   ├── COMMANDS.md         # Full command reference
│   ├── SECURITY.md         # Security guidelines
│   ├── TECH_SPEC.md        # Technical specifications
│   └── ROADMAP.md          # Development roadmap
│
├── tests/
│   ├── test_gui.py         # GUI automation tests
│   ├── test_files.py       # File operation tests
│   └── test_security.py    # Security tests
│
└── examples/
    ├── auto_login.json
    ├── daily_backup.json
    └── ui_testing.json
```

### Core Components

#### 1. Command Parser
Validates JSON structure and parameters:
```python
def parse_command(json_data):
    """
    Validates command structure
    Returns: (command_name, params) or raises ValidationError
    """
```

#### 2. Security Layer
Enforces permission checks:
```python
def check_permission(command_name, params):
    """
    Checks:
    - Command in whitelist?
    - Path allowed?
    - Confirmation required?
    """
```

#### 3. Execution Engine
Runs validated commands:
```python
def execute_command(command_name, params):
    """
    Maps command to function
    Executes with error handling
    Returns result or error
    """
```

#### 4. Logger
Records all operations:
```python
def log_action(level, command, result):
    """
    Formats: [TIMESTAMP] [LEVEL] command -> result
    Writes to: agent.log
    """
```

### Data Flow
```
1. GPT/User writes gpt_command.json
2. Agent detects file change
3. Parser validates JSON
4. Security layer checks permissions
5. Executor runs command
6. Logger records action
7. File is cleared (prevents re-execution)
8. Result returned to user
```

---

## 🔧 Development

### Setting Up Development Environment

1. **Fork and clone:**
```bash
git clone https://github.com/yourusername/LocalAgent.git
cd LocalAgent
```

2. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Install dev dependencies:**
```bash
pip install -r requirements-dev.txt
```

4. **Run tests:**
```bash
pytest tests/
```

### Adding New Commands

**Step 1: Define function in `agent.py`**
```python
def my_new_command(params):
    """
    Description of what this command does
    
    Args:
        params (dict): {
            "required_param": "value",
            "optional_param": "default"
        }
    
    Returns:
        dict: {"status": "success", "data": {...}}
    """
    # Your implementation
    return {"status": "success"}
```

**Step 2: Add to command metadata**
```python
COMMAND_METADATA = {
    "my_new_command": {
        "function": my_new_command,
        "security_level": "MEDIUM",
        "required_params": ["required_param"],
        "optional_params": ["optional_param"]
    }
}
```

**Step 3: Document in `docs/COMMANDS.md`**

**Step 4: Write tests**
```python
def test_my_new_command():
    result = my_new_command({"required_param": "test"})
    assert result["status"] == "success"
```

---

## 🗺️ Roadmap

### ✅ Version 1.0 (Current)
- [x] Basic command execution
- [x] GUI automation (keyboard, mouse)
- [x] Image recognition
- [x] File operations
- [x] 4-tier security system
- [x] Macro support

### 🚧 Version 1.5 (Next 2 months)
- [ ] Advanced file operations (sync, compare)
- [ ] System commands (registry, scheduled tasks)
- [ ] Git integration
- [ ] Docker support
- [ ] NPM/Node.js commands
- [ ] Enhanced macro system (if/else, loops)

### 🔮 Version 2.0 (Future)
- [ ] Plugin system for custom commands
- [ ] Web dashboard for monitoring
- [ ] Multi-agent coordination
- [ ] Voice command integration
- [ ] Cloud sync (optional, secure)
- [ ] Mobile app for remote control

### 💡 Ideas for 3.0+
- Natural language command parsing
- AI-powered workflow suggestions
- Cross-platform support (Linux, macOS)
- Blockchain-based audit logs
- Quantum-resistant encryption

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Reporting Bugs
1. Check existing issues
2. Create new issue with:
   - OS version
   - Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error logs

### Suggesting Features
1. Open discussion in Issues
2. Describe use case
3. Provide examples
4. Wait for community feedback

### Pull Requests
1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes with tests
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open Pull Request

### Code Standards
- **Style**: PEP 8
- **Docstrings**: Google style
- **Tests**: pytest with >80% coverage
- **Commits**: Conventional Commits format

---

## 📜 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Bogdan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **OpenCV Team** - For incredible image recognition library
- **PyAutoGUI Contributors** - For GUI automation foundation
- **Windows API Developers** - For system integration capabilities
- **Python Community** - For amazing ecosystem
- **You** - For using LocalAgent! ❤️

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/LocalAgent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/LocalAgent/discussions)
- **Email**: your.email@example.com
- **Twitter**: [@yourusername](https://twitter.com/yourusername)

---

## 🌟 Star History

If LocalAgent helped you, please consider giving it a ⭐!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/LocalAgent&type=Date)](https://star-history.com/#yourusername/LocalAgent&Date)

---

## 📊 Statistics

![GitHub stars](https://img.shields.io/github/stars/yourusername/LocalAgent?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/LocalAgent?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/LocalAgent)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/LocalAgent)

---

<div align="center">

**Made with ❤️ by Bogdan**

**Bridging Human Intelligence and Artificial Intelligence**

[⬆ Back to Top](#-localagent)

</div>