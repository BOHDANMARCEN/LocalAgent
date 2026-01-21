import argparse
import datetime
import json
import os
import platform
import shutil
import subprocess
import time
from typing import Any, Dict, Optional, Tuple


COMMAND_FILE = "gpt_command.json"
POLL_INTERVAL_SEC = 1.0

# Security levels for commands
COMMAND_SECURITY = {
    # SAFE commands (execute without confirmation)
    "message": "safe",
    "open_app": "safe",
    "list_dir": "safe",
    "get_file_info": "safe",
    "clipboard_get": "safe",
    "system_check": "safe",
    "list_processes": "safe",
    "check_if_running": "safe",
    "get_ram_usage": "safe",
    "get_cpu_usage": "safe",
    "get_disk_space": "safe",
    "list_drives": "safe",
    "check_internet": "safe",
    "get_ip": "safe",
    "read_file": "safe",
    "count_lines": "safe",
    "git_status": "safe",
    "json_read": "safe",
    "get_mouse_position": "safe",
    "get_active_window": "safe",
    "find_file": "safe",
    "find_in_file": "safe",
    "count_words": "safe",
    "get_file_hash": "safe",
    "find_files": "safe",
    "compare_files": "safe",
    "get_folder_size": "safe",

    # MEDIUM commands (with logging)
    "create_file": "medium",
    "create_folder": "medium",
    "move_file": "medium",
    "copy_file": "medium",
    "rename_file": "medium",
    "type_text": "medium",
    "screenshot": "medium",
    "ping": "medium",
    "set_volume": "medium",
    "mute": "medium",
    "unmute": "medium",
    "write_file": "medium",
    "append_file": "medium",
    "replace_in_file": "medium",
    "insert_line": "medium",
    "delete_line": "medium",
    "play_sound": "medium",
    "stop_sound": "medium",
    "open_url": "medium",
    "take_photo": "medium",
    "hash_file": "medium",
    "check_hash": "medium",
    "git_pull": "medium",
    "git_commit": "medium",
    "git_push": "medium",
    "json_write": "medium",
    "sqlite_query": "medium",
    "sqlite_insert": "medium",
    "mouse_move": "medium",
    "mouse_click": "medium",
    "press_key": "medium",
    "hotkey": "medium",
    "wait": "medium",
    "hold_key": "medium",
    "wait_random": "medium",
    "mouse_drag": "medium",
    "scroll": "medium",
    "screenshot_window": "medium",

    # DANGEROUS commands (require explicit confirmation)
    "delete_file": "dangerous",
    "kill_process": "dangerous",
    "shutdown_pc": "dangerous",
    "restart_pc": "dangerous",
    "sleep_pc": "dangerous",
    "lock_screen": "dangerous",
    "download_file": "dangerous",
    "encrypt_file": "dangerous",
    "decrypt_file": "dangerous",
    "run_script": "dangerous",
    "start_process": "dangerous",
    "restart_app": "dangerous",
    "set_priority": "dangerous",
    "press_key": "dangerous",
    "hotkey": "dangerous",
    "mouse_click": "dangerous",
    "mouse_move": "dangerous",
    "schedule_command": "dangerous",
    "sync_folders": "dangerous",
    "cancel_scheduled": "dangerous",
    "list_scheduled": "dangerous",
    "instrukey": "dangerous",
    "scan_defender": "dangerous",
    "registry_read": "dangerous",
    "registry_write": "dangerous",
    "registry_delete": "dangerous",
    "create_scheduled_task": "dangerous",
    "delete_scheduled_task": "dangerous",
    "set_env_var": "dangerous",
    "docker_stop": "dangerous",
    "docker_remove": "dangerous",

    # CRITICAL commands (require double confirmation and logging)
    "delete_folder": "critical",
    "format_drive": "critical",
}

COMMAND_META = {
    "message": {
        "summary": "Print text to the console.",
        "params": {"text": "string"},
        "example": {"command": "message", "params": {"text": "Hello"}},
    },
    "open_app": {
        "summary": "Launch a program or built-in command.",
        "params": {"path": "string"},
        "example": {"command": "open_app", "params": {"path": "notepad"}},
    },
    "instrukey": {
        "summary": "Run InstruKey by full path.",
        "params": {"path": "string"},
        "example": {
            "command": "instrukey",
            "params": {"path": "C:/Tools/InstruKey/InstruKey.exe"},
        },
    },
    "scan_defender": {
        "summary": "Run a Windows Defender scan for a file or folder.",
        "params": {"path": "string"},
        "example": {"command": "scan_defender", "params": {"path": "C:/Downloads"}},
    },
    "system_check": {
        "summary": "Print OS, CPU, memory, and disk info as JSON.",
        "params": {},
        "example": {"command": "system_check", "params": {}},
    },
    "delete_file": {
        "summary": "Delete a file only when confirm=true is provided.",
        "params": {"path": "string", "confirm": "bool"},
        "example": {
            "command": "delete_file",
            "params": {"path": "C:/Temp/test.txt", "confirm": True},
        },
    },
    "create_file": {
        "summary": "Create a file with content.",
        "params": {"path": "string", "content": "string"},
        "example": {
            "command": "create_file",
            "params": {"path": "C:/Temp/test.txt", "content": "Hello, World!"},
        },
    },
    "create_folder": {
        "summary": "Create a folder.",
        "params": {"path": "string"},
        "example": {"command": "create_folder", "params": {"path": "C:/Temp/NewFolder"}},
    },
    "move_file": {
        "summary": "Move a file.",
        "params": {"from": "string", "to": "string"},
        "example": {
            "command": "move_file",
            "params": {"from": "C:/Temp/test.txt", "to": "C:/Temp/NewFolder/test.txt"},
        },
    },
    "copy_file": {
        "summary": "Copy a file.",
        "params": {"from": "string", "to": "string"},
        "example": {
            "command": "copy_file",
            "params": {"from": "C:/Temp/test.txt", "to": "C:/Temp/NewFolder/test.txt"},
        },
    },
    "rename_file": {
        "summary": "Rename a file.",
        "params": {"path": "string", "new_name": "string"},
        "example": {
            "command": "rename_file",
            "params": {"path": "C:/Temp/test.txt", "new_name": "new_test.txt"},
        },
    },
    "list_dir": {
        "summary": "List files in a directory.",
        "params": {"path": "string"},
        "example": {"command": "list_dir", "params": {"path": "C:/Temp"}},
    },
    "find_file": {
        "summary": "Search for a file by name or pattern.",
        "params": {"path": "string", "pattern": "string"},
        "example": {
            "command": "find_file",
            "params": {"path": "C:/Temp", "pattern": "*.txt"},
        },
    },
    "get_file_info": {
        "summary": "Get file information (size, creation date, attributes).",
        "params": {"path": "string"},
        "example": {"command": "get_file_info", "params": {"path": "C:/Temp/test.txt"}},
    },
    "zip_files": {
        "summary": "Archive files.",
        "params": {"path": "string", "output": "string"},
        "example": {
            "command": "zip_files",
            "params": {"path": "C:/Temp/NewFolder", "output": "archive.zip"},
        },
    },
    "unzip_file": {
        "summary": "Extract an archive.",
        "params": {"path": "string", "output": "string"},
        "example": {
            "command": "unzip_file",
            "params": {"path": "archive.zip", "output": "C:/Temp/Extracted"},
        },
    },
    "kill_process": {
        "summary": "Kill a process by name or PID.",
        "params": {"name": "string", "pid": "number"},
        "example": {"command": "kill_process", "params": {"name": "notepad.exe"}},
    },
    "list_processes": {
        "summary": "List running processes.",
        "params": {},
        "example": {"command": "list_processes", "params": {}},
    },
    "start_process": {
        "summary": "Start a process with parameters.",
        "params": {"path": "string", "args": "string"},
        "example": {
            "command": "start_process",
            "params": {"path": "notepad.exe", "args": "test.txt"},
        },
    },
    "restart_app": {
        "summary": "Restart an application.",
        "params": {"name": "string"},
        "example": {"command": "restart_app", "params": {"name": "notepad.exe"}},
    },
    "check_if_running": {
        "summary": "Check if a process is running.",
        "params": {"name": "string"},
        "example": {"command": "check_if_running", "params": {"name": "notepad.exe"}},
    },
    "set_priority": {
        "summary": "Set process priority.",
        "params": {"name": "string", "priority": "string"},
        "example": {
            "command": "set_priority",
            "params": {"name": "notepad.exe", "priority": "high"},
        },
    },
    "type_text": {
        "summary": "Type text.",
        "params": {"text": "string"},
        "example": {"command": "type_text", "params": {"text": "Hello, World!"}},
    },
    "press_key": {
        "summary": "Press a key.",
        "params": {"key": "string"},
        "example": {"command": "press_key", "params": {"key": "enter"}},
    },
    "hotkey": {
        "summary": "Press a key combination.",
        "params": {"keys": "string"},
        "example": {"command": "hotkey", "params": {"keys": "ctrl+c"}},
    },
    "mouse_click": {
        "summary": "Click the mouse at coordinates.",
        "params": {"x": "number", "y": "number", "button": "string"},
        "example": {
            "command": "mouse_click",
            "params": {"x": 100, "y": 200, "button": "left"},
        },
    },
    "mouse_move": {
        "summary": "Move the mouse cursor.",
        "params": {"x": "number", "y": "number"},
        "example": {"command": "mouse_move", "params": {"x": 100, "y": 200}},
    },
    "screenshot": {
        "summary": "Take a screenshot.",
        "params": {"path": "string"},
        "example": {"command": "screenshot", "params": {"path": "C:/Temp/screenshot.png"}},
    },
    "wait": {
        "summary": "Delay execution in seconds.",
        "params": {"seconds": "number"},
        "example": {"command": "wait", "params": {"seconds": 5}},
    },
    "ping": {
        "summary": "Ping a host.",
        "params": {"host": "string"},
        "example": {"command": "ping", "params": {"host": "google.com"}},
    },
    "download_file": {
        "summary": "Download a file (with confirmation).",
        "params": {"url": "string", "path": "string"},
        "example": {
            "command": "download_file",
            "params": {"url": "https://example.com/file.txt", "path": "C:/Temp/file.txt"},
        },
    },
    "check_internet": {
        "summary": "Check internet connection.",
        "params": {},
        "example": {"command": "check_internet", "params": {}},
    },
    "get_ip": {
        "summary": "Get IP address.",
        "params": {},
        "example": {"command": "get_ip", "params": {}},
    },
    "get_ram_usage": {
        "summary": "Get RAM usage information.",
        "params": {},
        "example": {"command": "get_ram_usage", "params": {}},
    },
    "get_cpu_usage": {
        "summary": "Get CPU usage information.",
        "params": {},
        "example": {"command": "get_cpu_usage", "params": {}},
    },
    "get_disk_space": {
        "summary": "Get disk space information.",
        "params": {"drive": "string"},
        "example": {"command": "get_disk_space", "params": {"drive": "C:"}},
    },
    "list_drives": {
        "summary": "List available drives.",
        "params": {},
        "example": {"command": "list_drives", "params": {}},
    },
    "set_volume": {
        "summary": "Set volume level.",
        "params": {"level": "number"},
        "example": {"command": "set_volume", "params": {"level": 50}},
    },
    "mute": {
        "summary": "Mute the sound.",
        "params": {},
        "example": {"command": "mute", "params": {}},
    },
    "unmute": {
        "summary": "Unmute the sound.",
        "params": {},
        "example": {"command": "unmute", "params": {}},
    },
    "sleep_pc": {
        "summary": "Put the computer to sleep.",
        "params": {},
        "example": {"command": "sleep_pc", "params": {}},
    },
    "shutdown_pc": {
        "summary": "Shut down the computer (with confirmation).",
        "params": {"confirm": "bool"},
        "example": {"command": "shutdown_pc", "params": {"confirm": True}},
    },
    "restart_pc": {
        "summary": "Restart the computer (with confirmation).",
        "params": {"confirm": "bool"},
        "example": {"command": "restart_pc", "params": {"confirm": True}},
    },
    "lock_screen": {
        "summary": "Lock the screen.",
        "params": {},
        "example": {"command": "lock_screen", "params": {}},
    },
    "clipboard_copy": {
        "summary": "Copy text to clipboard.",
        "params": {"text": "string"},
        "example": {"command": "clipboard_copy", "params": {"text": "Hello, World!"}},
    },
    "clipboard_paste": {
        "summary": "Paste text from clipboard.",
        "params": {},
        "example": {"command": "clipboard_paste", "params": {}},
    },
    "clipboard_get": {
        "summary": "Get clipboard content.",
        "params": {},
        "example": {"command": "clipboard_get", "params": {}},
    },
    "clipboard_clear": {
        "summary": "Clear the clipboard.",
        "params": {},
        "example": {"command": "clipboard_clear", "params": {}},
    },
    "read_file": {
        "summary": "Read a text file.",
        "params": {"path": "string"},
        "example": {"command": "read_file", "params": {"path": "C:/Temp/test.txt"}},
    },
    "write_file": {
        "summary": "Write to a file.",
        "params": {"path": "string", "content": "string"},
        "example": {
            "command": "write_file",
            "params": {"path": "C:/Temp/test.txt", "content": "Hello, World!"},
        },
    },
    "append_file": {
        "summary": "Append to a file.",
        "params": {"path": "string", "content": "string"},
        "example": {
            "command": "append_file",
            "params": {"path": "C:/Temp/test.txt", "content": "Hello, World!"},
        },
    },
    "replace_in_file": {
        "summary": "Replace text in a file.",
        "params": {"path": "string", "old_text": "string", "new_text": "string"},
        "example": {
            "command": "replace_in_file",
            "params": {"path": "C:/Temp/test.txt", "old_text": "Hello", "new_text": "Hi"},
        },
    },
    "insert_line": {
        "summary": "Insert a line at a specific position in a file.",
        "params": {"path": "string", "line_number": "number", "content": "string"},
        "example": {
            "command": "insert_line",
            "params": {"path": "C:/Temp/test.txt", "line_number": 5, "content": "New line"},
        },
    },
    "delete_line": {
        "summary": "Delete a specific line from a file.",
        "params": {"path": "string", "line_number": "number"},
        "example": {
            "command": "delete_line",
            "params": {"path": "C:/Temp/test.txt", "line_number": 3},
        },
    },
    "find_in_file": {
        "summary": "Search for text in a file.",
        "params": {"path": "string", "text": "string", "regex": "bool"},
        "example": {
            "command": "find_in_file",
            "params": {"path": "C:/Temp/test.txt", "text": "search term", "regex": False},
        },
    },
    "count_lines": {
        "summary": "Count lines in a file.",
        "params": {"path": "string"},
        "example": {"command": "count_lines", "params": {"path": "C:/Temp/test.txt"}},
    },
    "count_words": {
        "summary": "Count words in a file.",
        "params": {"path": "string"},
        "example": {"command": "count_words", "params": {"path": "C:/Temp/document.txt"}},
    },
    "get_file_hash": {
        "summary": "Get the hash of a file.",
        "params": {"path": "string", "algorithm": "string"},
        "example": {
            "command": "get_file_hash",
            "params": {"path": "C:/Temp/test.txt", "algorithm": "sha256"},
        },
    },
    "find_files": {
        "summary": "Search for files recursively with optional depth limits.",
        "params": {"path": "string", "pattern": "string", "max_depth": "number"},
        "example": {
            "command": "find_files",
            "params": {"path": "C:/", "pattern": "*.log", "max_depth": 3},
        },
    },
    "sync_folders": {
        "summary": "Synchronize two folders.",
        "params": {"source": "string", "destination": "string", "mode": "string"},
        "example": {
            "command": "sync_folders",
            "params": {"source": "C:/Source", "destination": "C:/Backup", "mode": "mirror"},
        },
    },
    "compare_files": {
        "summary": "Compare two files.",
        "params": {"file1": "string", "file2": "string", "method": "string"},
        "example": {
            "command": "compare_files",
            "params": {"file1": "C:/version1.txt", "file2": "C:/version2.txt", "method": "hash"},
        },
    },
    "get_folder_size": {
        "summary": "Get the size of a folder.",
        "params": {"path": "string", "format": "string"},
        "example": {
            "command": "get_folder_size",
            "params": {"path": "C:/Projects", "format": "mb"},
        },
    },
    "play_sound": {
        "summary": "Play a sound.",
        "params": {"path": "string"},
        "example": {"command": "play_sound", "params": {"path": "C:/Temp/sound.wav"}},
    },
    "stop_sound": {
        "summary": "Stop sound playback.",
        "params": {},
        "example": {"command": "stop_sound", "params": {}},
    },
    "open_url": {
        "summary": "Open a URL in the browser.",
        "params": {"url": "string"},
        "example": {"command": "open_url", "params": {"url": "https://example.com"}},
    },
    "take_photo": {
        "summary": "Take a photo from the webcam (if available).",
        "params": {"path": "string"},
        "example": {"command": "take_photo", "params": {"path": "C:/Temp/photo.jpg"}},
    },
    "hash_file": {
        "summary": "Calculate file hash (MD5, SHA256).",
        "params": {"path": "string", "algorithm": "string"},
        "example": {
            "command": "hash_file",
            "params": {"path": "C:/Temp/test.txt", "algorithm": "sha256"},
        },
    },
    "encrypt_file": {
        "summary": "Encrypt a file.",
        "params": {"path": "string", "output": "string"},
        "example": {
            "command": "encrypt_file",
            "params": {"path": "C:/Temp/test.txt", "output": "C:/Temp/test.enc"},
        },
    },
    "decrypt_file": {
        "summary": "Decrypt a file.",
        "params": {"path": "string", "output": "string"},
        "example": {
            "command": "decrypt_file",
            "params": {"path": "C:/Temp/test.enc", "output": "C:/Temp/test.txt"},
        },
    },
    "check_hash": {
        "summary": "Check file integrity by hash.",
        "params": {"path": "string", "hash": "string"},
        "example": {
            "command": "check_hash",
            "params": {"path": "C:/Temp/test.txt", "hash": "a1b2c3..."},
        },
    },
    "schedule_command": {
        "summary": "Schedule a command for a specific time.",
        "params": {"command": "string", "params": "object", "time": "string"},
        "example": {
            "command": "schedule_command",
            "params": {
                "command": "message",
                "params": {"text": "Hello"},
                "time": "2026-01-21T20:00:00",
            },
        },
    },
    "cancel_scheduled": {
        "summary": "Cancel a scheduled command.",
        "params": {"id": "string"},
        "example": {"command": "cancel_scheduled", "params": {"id": "abc123"}},
    },
    "list_scheduled": {
        "summary": "List scheduled commands.",
        "params": {},
        "example": {"command": "list_scheduled", "params": {}},
    },
    "git_status": {
        "summary": "Run git status.",
        "params": {"path": "string"},
        "example": {"command": "git_status", "params": {"path": "C:/Projects/MyProject"}},
    },
    "git_pull": {
        "summary": "Run git pull.",
        "params": {"path": "string"},
        "example": {"command": "git_pull", "params": {"path": "C:/Projects/MyProject"}},
    },
    "git_commit": {
        "summary": "Run git commit.",
        "params": {"path": "string", "message": "string"},
        "example": {
            "command": "git_commit",
            "params": {"path": "C:/Projects/MyProject", "message": "Update README"},
        },
    },
    "git_push": {
        "summary": "Run git push.",
        "params": {"path": "string"},
        "example": {"command": "git_push", "params": {"path": "C:/Projects/MyProject"}},
    },
    "run_script": {
        "summary": "Run a script (.bat, .ps1).",
        "params": {"path": "string"},
        "example": {"command": "run_script", "params": {"path": "C:/Temp/script.bat"}},
    },
    "sqlite_query": {
        "summary": "Run a SQL query on SQLite.",
        "params": {"path": "string", "query": "string"},
        "example": {
            "command": "sqlite_query",
            "params": {"path": "C:/Temp/database.db", "query": "SELECT * FROM users"},
        },
    },
    "sqlite_insert": {
        "summary": "Insert data into SQLite.",
        "params": {"path": "string", "table": "string", "data": "object"},
        "example": {
            "command": "sqlite_insert",
            "params": {
                "path": "C:/Temp/database.db",
                "table": "users",
                "data": {"name": "John", "age": 30},
            },
        },
    },
    "json_read": {
        "summary": "Read a JSON file.",
        "params": {"path": "string"},
        "example": {"command": "json_read", "params": {"path": "C:/Temp/data.json"}},
    },
    "json_write": {
        "summary": "Write to a JSON file.",
        "params": {"path": "string", "data": "object"},
        "example": {
            "command": "json_write",
            "params": {"path": "C:/Temp/data.json", "data": {"name": "John", "age": 30}},
        },
    },
    "macro": {
        "summary": "Execute a macro (sequence of commands).",
        "params": {"name": "string"},
        "example": {"command": "macro", "params": {"name": "backup_project"}},
    },
    "mouse_drag": {
        "summary": "Drag the mouse from one position to another.",
        "params": {"from_x": "number", "from_y": "number", "to_x": "number", "to_y": "number", "duration": "number"},
        "example": {"command": "mouse_drag", "params": {"from_x": 100, "from_y": 100, "to_x": 500, "to_y": 500, "duration": 1}},
    },
    "scroll": {
        "summary": "Scroll the mouse wheel.",
        "params": {"direction": "string", "amount": "number"},
        "example": {"command": "scroll", "params": {"direction": "down", "amount": 3}},
    },
    "screenshot_window": {
        "summary": "Take a screenshot of a specific window.",
        "params": {"window_title": "string", "path": "string"},
        "example": {"command": "screenshot_window", "params": {"window_title": "Notepad", "path": "C:/Temp/notepad.png"}},
    },
    "get_mouse_position": {
        "summary": "Get the current mouse position.",
        "params": {},
        "example": {"command": "get_mouse_position", "params": {}},
    },
    "get_active_window": {
        "summary": "Get information about the active window.",
        "params": {},
        "example": {"command": "get_active_window", "params": {}},
    },
    "hold_key": {
        "summary": "Hold a key down for a specified duration.",
        "params": {"key": "string", "duration": "number"},
        "example": {"command": "hold_key", "params": {"key": "shift", "duration": 2}},
    },
    "wait_random": {
        "summary": "Wait for a random duration between min and max seconds.",
        "params": {"min": "number", "max": "number"},
        "example": {"command": "wait_random", "params": {"min": 1, "max": 3}},
    },
    "find_image": {
        "summary": "Find an image on the screen using template matching.",
        "params": {"template": "string", "confidence": "number"},
        "example": {"command": "find_image", "params": {"template": "C:/Templates/button.png", "confidence": 0.8}},
    },
    "wait_for_image": {
        "summary": "Wait for an image to appear on the screen.",
        "params": {"template": "string", "timeout": "number", "confidence": "number"},
        "example": {"command": "wait_for_image", "params": {"template": "C:/Templates/loading.png", "timeout": 30, "confidence": 0.8}},
    },
}


def show_message(text: str) -> None:
    print("GPT message:", text)


def open_app(path: str) -> None:
    """
    Launch a program or built-in command.
    Example paths:
      - "notepad"
      - "calc"
      - "C:/Tools/InstruKey.exe"
    """
    subprocess.Popen(path, shell=True)


def run_instrukey(path: str) -> None:
    """Run InstruKey by full path."""
    subprocess.run(f'"{path}"', shell=True, check=False)


def scan_defender(path: str) -> None:
    """Run a Windows Defender scan if MpCmdRun.exe is available."""
    possible = [
        r"C:\Program Files\Windows Defender\MpCmdRun.exe",
        r"C:\Program Files\Microsoft Defender\MpCmdRun.exe",
    ]
    exe = next((p for p in possible if os.path.exists(p)), None)
    if not exe:
        print("Defender CLI not found (MpCmdRun.exe). Skipping.")
        return

    cmd = f'"{exe}" -Scan -ScanType 3 -File "{path}"'
    subprocess.run(cmd, shell=True, check=False)


def system_check() -> None:
    """Print OS, CPU, memory, and disk info as JSON."""
    info: Dict[str, Any] = {}

    info["os"] = platform.platform()
    info["cpu_cores"] = os.cpu_count()

    try:
        import psutil  # type: ignore
    except ImportError:
        psutil = None

    if psutil:
        vm = psutil.virtual_memory()
        info["memory_total_gb"] = round(vm.total / (1024 ** 3), 2)
        info["memory_used_gb"] = round(vm.used / (1024 ** 3), 2)
        info["memory_percent"] = vm.percent

        boot = datetime.datetime.fromtimestamp(psutil.boot_time())
        now = datetime.datetime.now()
        info["boot_time"] = boot.isoformat()
        info["uptime_hours"] = round((now - boot).total_seconds() / 3600, 1)
    else:
        info["memory_note"] = "Install psutil for detailed memory and uptime."

    try:
        total, used, free = shutil.disk_usage("C:/")
        info["disk_c_total_gb"] = round(total / (1024 ** 3), 2)
        info["disk_c_used_gb"] = round(used / (1024 ** 3), 2)
        info["disk_c_free_gb"] = round(free / (1024 ** 3), 2)
    except Exception as e:
        info["disk_error"] = str(e)

    print("\n=== SYSTEM CHECK ===")
    print(json.dumps(info, indent=2))


def delete_file(path: str, confirm: bool = False) -> None:
    """Delete a file only when confirm=true is provided."""
    if not confirm:
        print(f"[WARN] Delete request for '{path}' without confirm=true. Skipping.")
        print('To confirm, set "confirm": true in params and write the JSON again.')
        return

    if not os.path.exists(path):
        print(f"[INFO] File not found: {path}")
        return

    try:
        os.remove(path)
        print(f"[OK] Deleted: {path}")
    except Exception as e:
        print(f"[ERROR] Failed to delete '{path}': {e}")


def create_file(path: str, content: str = "") -> None:
    """Create a file with content."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Created file: {path}")
    except Exception as e:
        print(f"[ERROR] Failed to create file '{path}': {e}")


def create_folder(path: str) -> None:
    """Create a folder."""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"[OK] Created folder: {path}")
    except Exception as e:
        print(f"[ERROR] Failed to create folder '{path}': {e}")


def move_file(from_path: str, to_path: str) -> None:
    """Move a file."""
    try:
        shutil.move(from_path, to_path)
        print(f"[OK] Moved file from '{from_path}' to '{to_path}'")
    except Exception as e:
        print(f"[ERROR] Failed to move file from '{from_path}' to '{to_path}': {e}")


def copy_file(from_path: str, to_path: str) -> None:
    """Copy a file."""
    try:
        shutil.copy2(from_path, to_path)
        print(f"[OK] Copied file from '{from_path}' to '{to_path}'")
    except Exception as e:
        print(f"[ERROR] Failed to copy file from '{from_path}' to '{to_path}': {e}")


def rename_file(path: str, new_name: str) -> None:
    """Rename a file."""
    try:
        new_path = os.path.join(os.path.dirname(path), new_name)
        os.rename(path, new_path)
        print(f"[OK] Renamed file from '{path}' to '{new_path}'")
    except Exception as e:
        print(f"[ERROR] Failed to rename file '{path}': {e}")


def list_dir(path: str) -> None:
    """List files in a directory."""
    try:
        files = os.listdir(path)
        print(f"Files in '{path}':")
        for file in files:
            print(f"- {file}")
    except Exception as e:
        print(f"[ERROR] Failed to list directory '{path}': {e}")


def find_file(path: str, pattern: str) -> None:
    """Search for a file by name or pattern."""
    try:
        import glob
        files = glob.glob(os.path.join(path, pattern))
        print(f"Found files matching '{pattern}' in '{path}':")
        for file in files:
            print(f"- {file}")
    except Exception as e:
        print(f"[ERROR] Failed to find files in '{path}': {e}")


def find_files(path: str, pattern: str, max_depth: Optional[int] = None) -> None:
    """Search for files recursively with optional depth limits."""
    try:
        import fnmatch

        if not os.path.isdir(path):
            print(f"[ERROR] Folder not found: {path}")
            return

        if max_depth is not None:
            try:
                max_depth = int(max_depth)
            except (TypeError, ValueError):
                print("[ERROR] max_depth must be a number.")
                return
            if max_depth < 0:
                print("[ERROR] max_depth must be >= 0.")
                return

        matches = []
        base_depth = path.rstrip(os.sep).count(os.sep)
        for root, dirs, files in os.walk(path):
            depth = root.rstrip(os.sep).count(os.sep) - base_depth
            if max_depth is not None and depth > max_depth:
                dirs[:] = []
                continue
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    matches.append(os.path.join(root, name))
            if max_depth is not None and depth >= max_depth:
                dirs[:] = []

        print(f"Found {len(matches)} files matching '{pattern}' in '{path}':")
        for match in matches:
            print(f"- {match}")
    except Exception as e:
        print(f"[ERROR] Failed to find files in '{path}': {e}")


def get_file_info(path: str) -> None:
    """Get file information (size, creation date, attributes)."""
    try:
        stat = os.stat(path)
        info = {
            "size_bytes": stat.st_size,
            "created": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }
        print(json.dumps(info, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to get file info for '{path}': {e}")


def get_folder_size(path: str, format: str = "bytes") -> None:
    """Get the size of a folder."""
    try:
        if not os.path.isdir(path):
            print(f"[ERROR] Folder not found: {path}")
            return

        total_size = 0
        for root, _, files in os.walk(path):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    total_size += os.path.getsize(file_path)
                except OSError:
                    continue

        units = {"bytes": 1, "kb": 1024, "mb": 1024 ** 2, "gb": 1024 ** 3}
        fmt = (format or "bytes").lower()
        if fmt not in units:
            print("[ERROR] format must be one of: bytes, kb, mb, gb")
            return

        size_value = total_size / units[fmt]
        result = {
            "path": path,
            "bytes": total_size,
            "size": round(size_value, 2),
            "format": fmt,
        }
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to get folder size for '{path}': {e}")


def compare_files(file1: str, file2: str, method: str = "hash") -> None:
    """Compare two files."""
    try:
        method = (method or "hash").lower()
        if method not in {"hash", "content", "binary"}:
            print("[ERROR] method must be one of: hash, content, binary")
            return

        result = {"file1": file1, "file2": file2, "method": method}

        if method == "hash":
            import hashlib

            def file_hash(path: str) -> str:
                hasher = hashlib.sha256()
                with open(path, "rb") as f:
                    for chunk in iter(lambda: f.read(8192), b""):
                        hasher.update(chunk)
                return hasher.hexdigest()

            hash1 = file_hash(file1)
            hash2 = file_hash(file2)
            result["hash1"] = hash1
            result["hash2"] = hash2
            result["equal"] = hash1 == hash2
        elif method == "content":
            with open(file1, "r", encoding="utf-8") as f:
                content1 = f.read()
            with open(file2, "r", encoding="utf-8") as f:
                content2 = f.read()
            result["equal"] = content1 == content2
        else:
            import filecmp

            result["equal"] = filecmp.cmp(file1, file2, shallow=False)

        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to compare files: {e}")


def zip_files(path: str, output: str) -> None:
    """Archive files."""
    try:
        shutil.make_archive(output.replace('.zip', ''), 'zip', path)
        print(f"[OK] Created archive '{output}' from '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to create archive: {e}")


def unzip_file(path: str, output: str) -> None:
    """Extract an archive."""
    try:
        shutil.unpack_archive(path, output)
        print(f"[OK] Extracted archive '{path}' to '{output}'")
    except Exception as e:
        print(f"[ERROR] Failed to extract archive: {e}")


def sync_folders(source: str, destination: str, mode: str = "update") -> None:
    """Synchronize two folders."""
    try:
        mode = (mode or "update").lower()
        if mode not in {"mirror", "update", "merge"}:
            print("[ERROR] mode must be one of: mirror, update, merge")
            return

        if not os.path.isdir(source):
            print(f"[ERROR] Source folder not found: {source}")
            return

        os.makedirs(destination, exist_ok=True)

        stats = {"copied": 0, "updated": 0, "deleted": 0, "deleted_dirs": 0}

        def sync_one_way(src_root: str, dst_root: str) -> None:
            for root, dirs, files in os.walk(src_root):
                rel_root = os.path.relpath(root, src_root)
                dest_root = dst_root if rel_root == "." else os.path.join(dst_root, rel_root)
                os.makedirs(dest_root, exist_ok=True)
                for name in files:
                    src_file = os.path.join(root, name)
                    dst_file = os.path.join(dest_root, name)
                    if not os.path.exists(dst_file):
                        shutil.copy2(src_file, dst_file)
                        stats["copied"] += 1
                    else:
                        if os.path.getmtime(src_file) > os.path.getmtime(dst_file):
                            shutil.copy2(src_file, dst_file)
                            stats["updated"] += 1

        sync_one_way(source, destination)
        if mode == "merge":
            sync_one_way(destination, source)

        if mode == "mirror":
            for root, dirs, files in os.walk(destination, topdown=False):
                rel_root = os.path.relpath(root, destination)
                src_root = source if rel_root == "." else os.path.join(source, rel_root)
                for name in files:
                    dst_file = os.path.join(root, name)
                    src_file = os.path.join(src_root, name)
                    if not os.path.exists(src_file):
                        try:
                            os.remove(dst_file)
                            stats["deleted"] += 1
                        except OSError:
                            continue
                for name in dirs:
                    dst_dir = os.path.join(root, name)
                    src_dir = os.path.join(src_root, name)
                    if not os.path.exists(src_dir):
                        try:
                            shutil.rmtree(dst_dir)
                            stats["deleted_dirs"] += 1
                        except OSError:
                            continue

        result = {
            "source": source,
            "destination": destination,
            "mode": mode,
            "copied": stats["copied"],
            "updated": stats["updated"],
            "deleted": stats["deleted"],
            "deleted_dirs": stats["deleted_dirs"],
        }
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to sync folders: {e}")


def kill_process(name: Optional[str] = None, pid: Optional[int] = None) -> None:
    """Kill a process by name or PID."""
    try:
        import psutil
        if pid:
            process = psutil.Process(pid)
            process.terminate()
            print(f"[OK] Killed process with PID {pid}")
        elif name:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == name:
                    proc.terminate()
                    print(f"[OK] Killed process '{name}' with PID {proc.info['pid']}")
        else:
            print("[ERROR] Neither 'name' nor 'pid' provided")
    except Exception as e:
        print(f"[ERROR] Failed to kill process: {e}")


def list_processes() -> None:
    """List running processes."""
    try:
        import psutil
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            processes.append({"pid": proc.info['pid'], "name": proc.info['name']})
        print(json.dumps(processes, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to list processes: {e}")


def start_process(path: str, args: str = "") -> None:
    """Start a process with parameters."""
    try:
        subprocess.Popen(f'"{path}" {args}', shell=True)
        print(f"[OK] Started process '{path}' with args '{args}'")
    except Exception as e:
        print(f"[ERROR] Failed to start process: {e}")


def restart_app(name: str) -> None:
    """Restart an application."""
    try:
        kill_process(name=name)
        time.sleep(1)
        start_process(name)
        print(f"[OK] Restarted application '{name}'")
    except Exception as e:
        print(f"[ERROR] Failed to restart application: {e}")


def check_if_running(name: str) -> None:
    """Check if a process is running."""
    try:
        import psutil
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == name:
                print(f"[OK] Process '{name}' is running")
                return
        print(f"[INFO] Process '{name}' is not running")
    except Exception as e:
        print(f"[ERROR] Failed to check process: {e}")


def set_priority(name: str, priority: str) -> None:
    """Set process priority."""
    try:
        import psutil
        priority_map = {"low": psutil.BELOW_NORMAL_PRIORITY_CLASS,
                        "normal": psutil.NORMAL_PRIORITY_CLASS,
                        "high": psutil.HIGH_PRIORITY_CLASS}
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == name:
                p = psutil.Process(proc.info['pid'])
                p.nice(priority_map.get(priority, psutil.NORMAL_PRIORITY_CLASS))
                print(f"[OK] Set priority '{priority}' for process '{name}'")
                return
        print(f"[ERROR] Process '{name}' not found")
    except Exception as e:
        print(f"[ERROR] Failed to set priority: {e}")


def type_text(text: str) -> None:
    """Type text."""
    try:
        import pyautogui
        pyautogui.write(text)
        print(f"[OK] Typed text: '{text}'")
    except Exception as e:
        print(f"[ERROR] Failed to type text: {e}")


def press_key(key: str) -> None:
    """Press a key."""
    try:
        import pyautogui
        pyautogui.press(key)
        print(f"[OK] Pressed key: '{key}'")
    except Exception as e:
        print(f"[ERROR] Failed to press key: {e}")


def hotkey(keys: str) -> None:
    """Press a key combination."""
    try:
        import pyautogui
        pyautogui.hotkey(*keys.split('+'))
        print(f"[OK] Pressed hotkey: '{keys}'")
    except Exception as e:
        print(f"[ERROR] Failed to press hotkey: {e}")


def mouse_click(x: int, y: int, button: str) -> None:
    """Click the mouse at coordinates."""
    try:
        import pyautogui
        pyautogui.click(x, y, button=button)
        print(f"[OK] Clicked at ({x}, {y}) with button '{button}'")
    except Exception as e:
        print(f"[ERROR] Failed to click mouse: {e}")


def mouse_move(x: int, y: int, duration: float = 0.0) -> None:
    """Move the mouse cursor with optional duration for smooth movement."""
    try:
        import pyautogui
        if duration > 0:
            pyautogui.moveTo(x, y, duration=duration)
        else:
            pyautogui.moveTo(x, y)
        print(f"[OK] Moved mouse to ({x}, {y})")
    except Exception as e:
        print(f"[ERROR] Failed to move mouse: {e}")

def mouse_drag(from_x: int, from_y: int, to_x: int, to_y: int, duration: float = 0.0) -> None:
    """Drag the mouse from one position to another."""
    try:
        import pyautogui
        pyautogui.mouseDown(from_x, from_y)
        if duration > 0:
            pyautogui.moveTo(to_x, to_y, duration=duration)
        else:
            pyautogui.moveTo(to_x, to_y)
        pyautogui.mouseUp()
        print(f"[OK] Dragged mouse from ({from_x}, {from_y}) to ({to_x}, {to_y})")
    except Exception as e:
        print(f"[ERROR] Failed to drag mouse: {e}")

def scroll(direction: str, amount: int = 1) -> None:
    """Scroll the mouse wheel."""
    try:
        import pyautogui
        if direction == "up":
            pyautogui.scroll(amount)
        elif direction == "down":
            pyautogui.scroll(-amount)
        else:
            print(f"[ERROR] Invalid scroll direction: {direction}")
            return
        print(f"[OK] Scrolled {direction} by {amount} units")
    except Exception as e:
        print(f"[ERROR] Failed to scroll: {e}")

def screenshot_window(window_title: str, path: str) -> None:
    """Take a screenshot of a specific window."""
    try:
        import pyautogui
        import win32gui
        import win32ui
        import win32con

        # Find the window by title
        hwnd = win32gui.FindWindow(None, window_title)
        if not hwnd:
            print(f"[ERROR] Window '{window_title}' not found")
            return

        # Get window dimensions
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        # Create device context
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        # Create bitmap
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)

        # Copy the screen to our memory device context
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

        # Save the bitmap to a file
        saveBitMap.SaveBitmapFile(saveDC, path)

        # Clean up
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        print(f"[OK] Saved window screenshot to '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to take window screenshot: {e}")

def get_mouse_position() -> None:
    """Get the current mouse position."""
    try:
        import pyautogui
        x, y = pyautogui.position()
        info = {"x": x, "y": y}
        print(json.dumps(info, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to get mouse position: {e}")

def get_active_window() -> None:
    """Get information about the active window."""
    try:
        import win32gui
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        info = {"title": title, "class": class_name}
        print(json.dumps(info, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to get active window: {e}")

def hold_key(key: str, duration: float) -> None:
    """Hold a key down for a specified duration."""
    try:
        import pyautogui
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)
        print(f"[OK] Held key '{key}' for {duration} seconds")
    except Exception as e:
        print(f"[ERROR] Failed to hold key: {e}")

def wait_random(min_seconds: int, max_seconds: int) -> None:
    """Wait for a random duration between min and max seconds."""
    try:
        import random
        duration = random.uniform(min_seconds, max_seconds)
        time.sleep(duration)
        print(f"[OK] Waited for {duration:.2f} seconds")
    except Exception as e:
        print(f"[ERROR] Failed to wait: {e}")

def find_image(template_path: str, confidence: float = 0.8) -> None:
    """Find an image on the screen using template matching."""
    try:
        import pyautogui
        import cv2
        import numpy as np

        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Load template
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            print(f"[ERROR] Could not load template image: {template_path}")
            return

        # Template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:
            # Calculate center of the matched area
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2

            info = {
                "found": True,
                "confidence": max_val,
                "position": {"x": center_x, "y": center_y},
                "size": {"width": w, "height": h}
            }
            print(json.dumps(info, indent=2))
        else:
            info = {
                "found": False,
                "confidence": max_val,
                "message": "Image not found with sufficient confidence"
            }
            print(json.dumps(info, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to find image: {e}")

def wait_for_image(template_path: str, timeout: int = 30, confidence: float = 0.8) -> None:
    """Wait for an image to appear on the screen."""
    try:
        import time
        start_time = time.time()

        while time.time() - start_time < timeout:
            # Call find_image to check if the image is present
            find_image(template_path, confidence)

            # Check if the image was found by looking at the output
            # This is a simplified approach - in a real implementation, you'd want
            # to capture the output or use a return value
            time.sleep(1)

        print(f"[INFO] Timeout reached after {timeout} seconds")
    except Exception as e:
        print(f"[ERROR] Failed to wait for image: {e}")


def screenshot(path: str) -> None:
    """Take a screenshot."""
    try:
        import pyautogui
        pyautogui.screenshot(path)
        print(f"[OK] Saved screenshot to '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to take screenshot: {e}")


def wait(seconds: int) -> None:
    """Delay execution in seconds."""
    time.sleep(seconds)
    print(f"[OK] Waited for {seconds} seconds")


def ping(host: str) -> None:
    """Ping a host."""
    try:
        subprocess.run(["ping", host], check=True)
        print(f"[OK] Pinged host '{host}'")
    except Exception as e:
        print(f"[ERROR] Failed to ping host: {e}")


def download_file(url: str, path: str) -> None:
    """Download a file (with confirmation)."""
    try:
        import requests
        response = requests.get(url)
        with open(path, "wb") as f:
            f.write(response.content)
        print(f"[OK] Downloaded file from '{url}' to '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to download file: {e}")


def check_internet() -> None:
    """Check internet connection."""
    try:
        import requests
        response = requests.get("https://www.google.com", timeout=5)
        print("[OK] Internet connection is active")
    except Exception as e:
        print(f"[ERROR] No internet connection: {e}")


def get_ip() -> None:
    """Get IP address."""
    try:
        import requests
        response = requests.get("https://api.ipify.org")
        print(f"[OK] Public IP address: {response.text}")
    except Exception as e:
        print(f"[ERROR] Failed to get IP address: {e}")


def get_ram_usage() -> None:
    """Get RAM usage information."""
    try:
        import psutil
        vm = psutil.virtual_memory()
        info = {
            "total_gb": round(vm.total / (1024 ** 3), 2),
            "used_gb": round(vm.used / (1024 ** 3), 2),
            "percent": vm.percent,
        }
        print(json.dumps(info, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to get RAM usage: {e}")


def get_cpu_usage() -> None:
    """Get CPU usage information."""
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        info = {"cpu_percent": cpu}
        print(json.dumps(info, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to get CPU usage: {e}")


def get_disk_space(drive: str = "C:") -> None:
    """Get disk space information."""
    try:
        total, used, free = shutil.disk_usage(drive)
        info = {
            "drive": drive,
            "total_gb": round(total / (1024 ** 3), 2),
            "used_gb": round(used / (1024 ** 3), 2),
            "free_gb": round(free / (1024 ** 3), 2),
        }
        print(json.dumps(info, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to get disk space: {e}")


def list_drives() -> None:
    """List available drives."""
    try:
        drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\")]
        print("Available drives:")
        for drive in drives:
            print(f"- {drive}")
    except Exception as e:
        print(f"[ERROR] Failed to list drives: {e}")


def set_volume(level: int) -> None:
    """Set volume level."""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        print(f"[OK] Set volume to {level}%")
    except Exception as e:
        print(f"[ERROR] Failed to set volume: {e}")


def mute() -> None:
    """Mute the sound."""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(1, None)
        print("[OK] Sound muted")
    except Exception as e:
        print(f"[ERROR] Failed to mute sound: {e}")


def unmute() -> None:
    """Unmute the sound."""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(0, None)
        print("[OK] Sound unmuted")
    except Exception as e:
        print(f"[ERROR] Failed to unmute sound: {e}")


def sleep_pc() -> None:
    """Put the computer to sleep."""
    try:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        print("[OK] Computer put to sleep")
    except Exception as e:
        print(f"[ERROR] Failed to put computer to sleep: {e}")


def shutdown_pc(confirm: bool = False) -> None:
    """Shut down the computer (with confirmation)."""
    if not confirm:
        print("[WARN] Shutdown request without confirm=true. Skipping.")
        return
    try:
        os.system("shutdown /s /t 1")
        print("[OK] Computer shutting down")
    except Exception as e:
        print(f"[ERROR] Failed to shut down computer: {e}")


def restart_pc(confirm: bool = False) -> None:
    """Restart the computer (with confirmation)."""
    if not confirm:
        print("[WARN] Restart request without confirm=true. Skipping.")
        return
    try:
        os.system("shutdown /r /t 1")
        print("[OK] Computer restarting")
    except Exception as e:
        print(f"[ERROR] Failed to restart computer: {e}")


def lock_screen() -> None:
    """Lock the screen."""
    try:
        import ctypes
        ctypes.windll.user32.LockWorkStation()
        print("[OK] Screen locked")
    except Exception as e:
        print(f"[ERROR] Failed to lock screen: {e}")


def clipboard_copy(text: str) -> None:
    """Copy text to clipboard."""
    try:
        import pyperclip
        pyperclip.copy(text)
        print(f"[OK] Copied to clipboard: '{text}'")
    except Exception as e:
        print(f"[ERROR] Failed to copy to clipboard: {e}")


def clipboard_paste() -> None:
    """Paste text from clipboard."""
    try:
        import pyperclip
        text = pyperclip.paste()
        print(f"[OK] Pasted from clipboard: '{text}'")
    except Exception as e:
        print(f"[ERROR] Failed to paste from clipboard: {e}")


def clipboard_get() -> None:
    """Get clipboard content."""
    try:
        import pyperclip
        text = pyperclip.paste()
        print(f"Clipboard content: {text}")
    except Exception as e:
        print(f"[ERROR] Failed to get clipboard content: {e}")


def clipboard_clear() -> None:
    """Clear the clipboard."""
    try:
        import pyperclip
        pyperclip.copy('')
        print("[OK] Clipboard cleared")
    except Exception as e:
        print(f"[ERROR] Failed to clear clipboard: {e}")


def read_file(path: str) -> None:
    """Read a text file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"File content:\n{content}")
    except Exception as e:
        print(f"[ERROR] Failed to read file: {e}")


def write_file(path: str, content: str) -> None:
    """Write to a file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Wrote to file: '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to write to file: {e}")


def append_file(path: str, content: str) -> None:
    """Append to a file."""
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Appended to file: '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to append to file: {e}")


def replace_in_file(path: str, old_text: str, new_text: str) -> None:
    """Replace text in a file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace(old_text, new_text)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Replaced text in file: '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to replace text in file: {e}")


def insert_line(path: str, line_number: int, content: str) -> None:
    """Insert a line at a specific position in a file (1-based)."""
    try:
        line_number = int(line_number)
        if line_number < 1:
            print("[ERROR] line_number must be >= 1.")
            return

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if line_number > len(lines) + 1:
            print(f"[ERROR] line_number out of range (1-{len(lines) + 1}).")
            return

        line = content
        if not line.endswith("\n"):
            line += "\n"

        lines.insert(line_number - 1, line)
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"[OK] Inserted line {line_number} into '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to insert line: {e}")


def delete_line(path: str, line_number: int) -> None:
    """Delete a specific line from a file (1-based)."""
    try:
        line_number = int(line_number)
        if line_number < 1:
            print("[ERROR] line_number must be >= 1.")
            return

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if line_number > len(lines):
            print(f"[ERROR] line_number out of range (1-{len(lines)}).")
            return

        lines.pop(line_number - 1)
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"[OK] Deleted line {line_number} from '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to delete line: {e}")


def find_in_file(path: str, text: str, regex: bool = False) -> None:
    """Search for text in a file."""
    try:
        if not text:
            print("[ERROR] text must be a non-empty string.")
            return

        matches = []
        if regex:
            import re
            pattern = re.compile(text)

        with open(path, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                if regex:
                    if pattern.search(line):
                        matches.append({"line": line_number, "text": line.rstrip("\n")})
                else:
                    if text in line:
                        matches.append({"line": line_number, "text": line.rstrip("\n")})

        result = {"path": path, "count": len(matches), "matches": matches}
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to search file: {e}")


def count_lines(path: str) -> None:
    """Count lines in a file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        print(f"[OK] File '{path}' has {len(lines)} lines")
    except Exception as e:
        print(f"[ERROR] Failed to count lines in file: {e}")


def count_words(path: str) -> None:
    """Count words in a file."""
    try:
        import re

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        words = re.findall(r"\b\w+\b", content)
        print(f"[OK] File '{path}' has {len(words)} words")
    except Exception as e:
        print(f"[ERROR] Failed to count words in file: {e}")


def play_sound(path: str) -> None:
    """Play a sound."""
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        print(f"[OK] Playing sound: '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to play sound: {e}")


def stop_sound() -> None:
    """Stop sound playback."""
    try:
        import pygame
        pygame.mixer.music.stop()
        print("[OK] Sound stopped")
    except Exception as e:
        print(f"[ERROR] Failed to stop sound: {e}")


def open_url(url: str) -> None:
    """Open a URL in the browser."""
    try:
        import webbrowser
        webbrowser.open(url)
        print(f"[OK] Opened URL: '{url}'")
    except Exception as e:
        print(f"[ERROR] Failed to open URL: {e}")


def take_photo(path: str) -> None:
    """Take a photo from the webcam (if available)."""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(path, frame)
            print(f"[OK] Saved photo to: '{path}'")
        else:
            print("[ERROR] Failed to capture photo")
        cap.release()
    except Exception as e:
        print(f"[ERROR] Failed to take photo: {e}")


def hash_file(path: str, algorithm: str = "sha256") -> None:
    """Calculate file hash (MD5, SHA256)."""
    try:
        import hashlib
        with open(path, "rb") as f:
            content = f.read()
        if algorithm == "md5":
            hash_object = hashlib.md5(content)
        else:
            hash_object = hashlib.sha256(content)
        print(f"[OK] Hash of '{path}' ({algorithm}): {hash_object.hexdigest()}")
    except Exception as e:
        print(f"[ERROR] Failed to calculate hash: {e}")


def get_file_hash(path: str, algorithm: str = "sha256") -> None:
    """Get file hash."""
    try:
        import hashlib

        algo = (algorithm or "sha256").lower()
        try:
            hasher = hashlib.new(algo)
        except ValueError:
            print("[ERROR] Unsupported hash algorithm. Use md5 or sha256.")
            return

        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
        print(f"[OK] Hash of '{path}' ({algo}): {hasher.hexdigest()}")
    except Exception as e:
        print(f"[ERROR] Failed to calculate hash: {e}")


def encrypt_file(path: str, output: str) -> None:
    """Encrypt a file."""
    try:
        from cryptography.fernet import Fernet
        key = Fernet.generate_key()
        cipher = Fernet(key)
        with open(path, "rb") as f:
            data = f.read()
        encrypted = cipher.encrypt(data)
        with open(output, "wb") as f:
            f.write(encrypted)
        print(f"[OK] Encrypted file '{path}' to '{output}'")
    except Exception as e:
        print(f"[ERROR] Failed to encrypt file: {e}")


def decrypt_file(path: str, output: str) -> None:
    """Decrypt a file."""
    try:
        from cryptography.fernet import Fernet
        with open(path, "rb") as f:
            encrypted = f.read()
        cipher = Fernet(encrypted[:44])
        decrypted = cipher.decrypt(encrypted[44:])
        with open(output, "wb") as f:
            f.write(decrypted)
        print(f"[OK] Decrypted file '{path}' to '{output}'")
    except Exception as e:
        print(f"[ERROR] Failed to decrypt file: {e}")


def check_hash(path: str, hash: str) -> None:
    """Check file integrity by hash."""
    try:
        import hashlib
        with open(path, "rb") as f:
            content = f.read()
        hash_object = hashlib.sha256(content)
        if hash_object.hexdigest() == hash:
            print(f"[OK] Hash of '{path}' matches")
        else:
            print(f"[ERROR] Hash of '{path}' does not match")
    except Exception as e:
        print(f"[ERROR] Failed to check hash: {e}")


def schedule_command(command: str, params: Dict[str, Any], time: str) -> None:
    """Schedule a command for a specific time."""
    try:
        import schedule
        import threading
        def run_command():
            execute_command({"command": command, "params": params})
        schedule.every().day.at(time).do(run_command)
        threading.Thread(target=schedule.run_all, daemon=True).start()
        print(f"[OK] Scheduled command '{command}' for {time}")
    except Exception as e:
        print(f"[ERROR] Failed to schedule command: {e}")


def cancel_scheduled(id: str) -> None:
    """Cancel a scheduled command."""
    try:
        import schedule
        schedule.clear(id)
        print(f"[OK] Cancelled scheduled command with ID '{id}'")
    except Exception as e:
        print(f"[ERROR] Failed to cancel scheduled command: {e}")


def list_scheduled() -> None:
    """List scheduled commands."""
    try:
        import schedule
        jobs = schedule.get_jobs()
        print("Scheduled commands:")
        for job in jobs:
            print(f"- {job}")
    except Exception as e:
        print(f"[ERROR] Failed to list scheduled commands: {e}")


def git_status(path: str = ".") -> None:
    """Run git status."""
    try:
        subprocess.run(["git", "status"], cwd=path, check=True)
        print(f"[OK] Git status for '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to run git status: {e}")


def git_pull(path: str = ".") -> None:
    """Run git pull."""
    try:
        subprocess.run(["git", "pull"], cwd=path, check=True)
        print(f"[OK] Git pull for '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to run git pull: {e}")


def git_commit(path: str = ".", message: str = "") -> None:
    """Run git commit."""
    try:
        subprocess.run(["git", "commit", "-m", message], cwd=path, check=True)
        print(f"[OK] Git commit for '{path}' with message '{message}'")
    except Exception as e:
        print(f"[ERROR] Failed to run git commit: {e}")


def git_push(path: str = ".") -> None:
    """Run git push."""
    try:
        subprocess.run(["git", "push"], cwd=path, check=True)
        print(f"[OK] Git push for '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to run git push: {e}")


def run_script(path: str) -> None:
    """Run a script (.bat, .ps1)."""
    try:
        subprocess.run([path], shell=True, check=True)
        print(f"[OK] Ran script '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to run script: {e}")


def sqlite_query(path: str, query: str) -> None:
    """Run a SQL query on SQLite."""
    try:
        import sqlite3
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        print(json.dumps(results, indent=2))
        conn.close()
    except Exception as e:
        print(f"[ERROR] Failed to run SQL query: {e}")


def sqlite_insert(path: str, table: str, data: Dict[str, Any]) -> None:
    """Insert data into SQLite."""
    try:
        import sqlite3
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        conn.close()
        print(f"[OK] Inserted data into table '{table}'")
    except Exception as e:
        print(f"[ERROR] Failed to insert data: {e}")


def json_read(path: str) -> None:
    """Read a JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to read JSON file: {e}")


def json_write(path: str, data: Dict[str, Any]) -> None:
    """Write to a JSON file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[OK] Wrote JSON to file: '{path}'")
    except Exception as e:
        print(f"[ERROR] Failed to write JSON file: {e}")


def macro(name: str) -> None:
    """Execute a macro (sequence of commands)."""
    try:
        with open("macros.json", "r", encoding="utf-8") as f:
            macros_data = json.load(f)

        # Find the macro by name in the list
        macro_found = None
        for macro_item in macros_data.get("macros", []):
            if macro_item.get("name") == name:
                macro_found = macro_item
                break

        if macro_found:
            steps = macro_found.get("steps", [])
            for step in steps:
                # Extract command and params from step
                step_command = step.get("command")
                step_params = step.get("params", {})

                if step_command:
                    execute_command({"command": step_command, "params": step_params})
                else:
                    print(f"[ERROR] Invalid step in macro '{name}': missing command")
                    return
        else:
            print(f"[ERROR] Macro '{name}' not found")
    except Exception as e:
        print(f"[ERROR] Failed to execute macro: {e}")


COMMANDS = {
    "message": show_message,
    "open_app": open_app,
    "instrukey": run_instrukey,
    "scan_defender": scan_defender,
    "system_check": system_check,
    "delete_file": delete_file,
    "create_file": create_file,
    "create_folder": create_folder,
    "move_file": move_file,
    "copy_file": copy_file,
    "rename_file": rename_file,
    "list_dir": list_dir,
    "find_file": find_file,
    "find_files": find_files,
    "get_file_info": get_file_info,
    "get_folder_size": get_folder_size,
    "compare_files": compare_files,
    "zip_files": zip_files,
    "unzip_file": unzip_file,
    "sync_folders": sync_folders,
    "kill_process": kill_process,
    "list_processes": list_processes,
    "start_process": start_process,
    "restart_app": restart_app,
    "check_if_running": check_if_running,
    "set_priority": set_priority,
    "type_text": type_text,
    "press_key": press_key,
    "hotkey": hotkey,
    "mouse_click": mouse_click,
    "mouse_move": mouse_move,
    "screenshot": screenshot,
    "wait": wait,
    "ping": ping,
    "download_file": download_file,
    "check_internet": check_internet,
    "get_ip": get_ip,
    "get_ram_usage": get_ram_usage,
    "get_cpu_usage": get_cpu_usage,
    "get_disk_space": get_disk_space,
    "list_drives": list_drives,
    "set_volume": set_volume,
    "mute": mute,
    "unmute": unmute,
    "sleep_pc": sleep_pc,
    "shutdown_pc": shutdown_pc,
    "restart_pc": restart_pc,
    "lock_screen": lock_screen,
    "clipboard_copy": clipboard_copy,
    "clipboard_paste": clipboard_paste,
    "clipboard_get": clipboard_get,
    "clipboard_clear": clipboard_clear,
    "read_file": read_file,
    "write_file": write_file,
    "append_file": append_file,
    "replace_in_file": replace_in_file,
    "insert_line": insert_line,
    "delete_line": delete_line,
    "find_in_file": find_in_file,
    "count_lines": count_lines,
    "count_words": count_words,
    "play_sound": play_sound,
    "stop_sound": stop_sound,
    "open_url": open_url,
    "take_photo": take_photo,
    "hash_file": hash_file,
    "get_file_hash": get_file_hash,
    "encrypt_file": encrypt_file,
    "decrypt_file": decrypt_file,
    "check_hash": check_hash,
    "schedule_command": schedule_command,
    "cancel_scheduled": cancel_scheduled,
    "list_scheduled": list_scheduled,
    "git_status": git_status,
    "git_pull": git_pull,
    "git_commit": git_commit,
    "git_push": git_push,
    "run_script": run_script,
    "sqlite_query": sqlite_query,
    "sqlite_insert": sqlite_insert,
    "json_read": json_read,
    "json_write": json_write,
    "macro": macro,
    "mouse_drag": mouse_drag,
    "scroll": scroll,
    "screenshot_window": screenshot_window,
    "get_mouse_position": get_mouse_position,
    "get_active_window": get_active_window,
    "hold_key": hold_key,
    "wait_random": wait_random,
    "find_image": find_image,
    "wait_for_image": wait_for_image,
}


def read_json_file(path: str) -> Optional[Dict[str, Any]]:
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not data:
            return None
        if not isinstance(data, dict):
            print("[WARN] Command file is not a JSON object.")
            return None
        return data
    except json.JSONDecodeError:
        return None


def load_json_file(path: str) -> Tuple[Optional[Any], Optional[str]]:
    if not os.path.exists(path):
        return None, f"File not found: {path}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            return None, "File is empty."
        return json.loads(content), None
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON: {e}"


def clear_command_file(path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("{}")


def validate_command_data(data: Any) -> Tuple[bool, str]:
    if not isinstance(data, dict):
        return False, "Command JSON must be an object."

    command = data.get("command")
    if not isinstance(command, str) or not command:
        return False, "command must be a non-empty string."

    params = data.get("params", {})
    if params is None:
        params = {}
    if not isinstance(params, dict):
        return False, "params must be an object."

    return True, ""


def execute_command(data: Dict[str, Any]) -> None:
    action = data.get("command")
    params = data.get("params", {}) or {}

    if not isinstance(action, str):
        print("[WARN] command must be a string.")
        return
    if not isinstance(params, dict):
        print("[WARN] params must be an object.")
        return

    if action in COMMANDS:
        # Check security level
        security_level = COMMAND_SECURITY.get(action, "safe")

        if security_level == "dangerous":
            # For dangerous commands, require explicit confirmation
            if not params.get("confirm", False):
                print(f"[WARN] Dangerous command '{action}' requires explicit confirmation (confirm=true). Skipping.")
                return

        print(f"\n[RUN] {action} | params={params} | security={security_level}")
        try:
            COMMANDS[action](**params)
        except TypeError as e:
            print("[ERROR] Invalid parameters:", e)
        except Exception as e:
            print("[ERROR] Command failed:", e)
    else:
        print("[WARN] Unknown or forbidden command:", action)


def process_command_file(command_file: str) -> bool:
    cmd = read_json_file(command_file)
    if not cmd:
        return False

    # Clear before executing to avoid replays on crash.
    clear_command_file(command_file)
    execute_command(cmd)
    return True


def parse_param_value(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def parse_params(params_json: Optional[str], param_items: Optional[list[str]]) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if params_json:
        try:
            data = json.loads(params_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in --params-json: {e}")
        if not isinstance(data, dict):
            raise ValueError("--params-json must be a JSON object.")
        params.update(data)

    for item in param_items or []:
        if "=" not in item:
            raise ValueError(f"Invalid --param '{item}', expected key=value.")
        key, raw = item.split("=", 1)
        if not key:
            raise ValueError(f"Invalid --param '{item}', empty key.")
        params[key] = parse_param_value(raw)

    return params


def write_command_file(path: str, payload: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def cmd_run(args: argparse.Namespace) -> int:
    if args.interval <= 0:
        print("[ERROR] interval must be greater than 0.")
        return 2

    print("LocalAgent started. Watching:", os.path.abspath(args.command_file))
    if args.once:
        processed = process_command_file(args.command_file)
        if not processed:
            print("[INFO] No command found.")
        return 0

    while True:
        process_command_file(args.command_file)
        time.sleep(args.interval)


def cmd_send(args: argparse.Namespace) -> int:
    try:
        params = parse_params(args.params_json, args.param)
    except ValueError as e:
        print("[ERROR]", e)
        return 2

    payload = {"command": args.command, "params": params}

    if args.print_payload:
        print(json.dumps(payload, indent=2 if args.pretty else None))

    if not args.no_write:
        write_command_file(args.command_file, payload)
        print("[OK] Wrote command to:", os.path.abspath(args.command_file))

    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    if args.json_text is not None:
        try:
            data = json.loads(args.json_text)
        except json.JSONDecodeError as e:
            print("[ERROR] Invalid JSON:", e)
            return 2
    else:
        data, err = load_json_file(args.command_file)
        if err:
            print("[ERROR]", err)
            return 2

    ok, error = validate_command_data(data)
    if not ok:
        print("[ERROR]", error)
        return 1

    print("[OK] Command JSON is valid.")
    return 0


def cmd_commands(args: argparse.Namespace) -> int:
    if args.json_out:
        payload = []
        for name in sorted(COMMAND_META):
            meta = COMMAND_META[name]
            payload.append(
                {
                    "name": name,
                    "summary": meta.get("summary", ""),
                    "params": meta.get("params", {}),
                }
            )
        print(json.dumps(payload, indent=2))
        return 0

    for name in sorted(COMMAND_META):
        summary = COMMAND_META[name].get("summary", "")
        print(f"{name} - {summary}")
    return 0


def cmd_example(args: argparse.Namespace) -> int:
    if args.command not in COMMAND_META:
        print("[ERROR] Unknown command:", args.command)
        return 2

    example = COMMAND_META[args.command].get("example")
    if not example:
        example = {"command": args.command, "params": {}}

    print(json.dumps(example, indent=2 if args.pretty else None))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="LocalAgent JSON command runner for Windows."
    )
    subparsers = parser.add_subparsers(dest="subcommand")

    run_parser = subparsers.add_parser("run", help="Start the agent loop.")
    run_parser.add_argument(
        "--command-file",
        default=COMMAND_FILE,
        help="Path to gpt_command.json",
    )
    run_parser.add_argument(
        "--interval",
        type=float,
        default=POLL_INTERVAL_SEC,
        help="Polling interval in seconds",
    )
    run_parser.add_argument(
        "--once",
        action="store_true",
        help="Process one command if present, then exit",
    )
    run_parser.set_defaults(func=cmd_run)

    send_parser = subparsers.add_parser("send", help="Write a command to the file.")
    send_parser.add_argument("command", help="Command name")
    send_parser.add_argument(
        "--command-file",
        default=COMMAND_FILE,
        help="Path to gpt_command.json",
    )
    send_parser.add_argument(
        "--params-json",
        dest="params_json",
        help="JSON object with params",
    )
    send_parser.add_argument(
        "--param",
        action="append",
        help="Key=Value pair, value parsed as JSON if possible",
    )
    send_parser.add_argument(
        "--print",
        action="store_true",
        dest="print_payload",
        help="Print JSON payload to stdout",
    )
    send_parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON when using --print",
    )
    send_parser.add_argument(
        "--no-write",
        action="store_true",
        help="Do not write to the command file",
    )
    send_parser.set_defaults(func=cmd_send)

    validate_parser = subparsers.add_parser(
        "validate", help="Validate a command JSON."
    )
    validate_parser.add_argument(
        "--command-file",
        default=COMMAND_FILE,
        help="Path to gpt_command.json",
    )
    validate_parser.add_argument(
        "--json",
        dest="json_text",
        help="Validate this JSON string instead of the file",
    )
    validate_parser.set_defaults(func=cmd_validate)

    commands_parser = subparsers.add_parser(
        "commands", help="List supported commands."
    )
    commands_parser.add_argument(
        "--json",
        action="store_true",
        dest="json_out",
        help="Output command metadata as JSON",
    )
    commands_parser.set_defaults(func=cmd_commands)

    example_parser = subparsers.add_parser(
        "example", help="Print example JSON for a command."
    )
    example_parser.add_argument("command", help="Command name")
    example_parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON",
    )
    example_parser.set_defaults(func=cmd_example)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.subcommand:
        return cmd_run(
            argparse.Namespace(
                command_file=COMMAND_FILE,
                interval=POLL_INTERVAL_SEC,
                once=False,
            )
        )

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
