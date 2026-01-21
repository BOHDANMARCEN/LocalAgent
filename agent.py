import argparse
import datetime
import inspect
import json
import logging
import os
import platform
import shutil
import subprocess
import sys
import time
from typing import Any, Callable, Dict, Optional, Tuple

# ==============================================================================
# Constants
# ==============================================================================

# Determine the script's directory to make file paths relative
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

COMMAND_FILE_NAME = "gpt_command.json"
LOG_FILE_NAME = "agent.log"
COMMAND_FILE_PATH = os.path.join(SCRIPT_DIR, COMMAND_FILE_NAME)
LOG_PATH = os.path.join(SCRIPT_DIR, LOG_FILE_NAME)

DEFAULT_POLL_INTERVAL_SEC = 1.0

PROTECTED_PROCESS_NAMES = {
    "csrss.exe",
    "wininit.exe",
    "winlogon.exe",
    "services.exe",
    "smss.exe",
    "lsass.exe",
    "svchost.exe",
    "system",
}

# ==============================================================================
# Logger Setup
# ==============================================================================

def setup_logger() -> logging.Logger:
    """Sets up the global logger for the agent."""
    logger = logging.getLogger("LocalAgent")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger

LOGGER = setup_logger()

# ==============================================================================
# Command Functions
# ==============================================================================

def show_message(text: str) -> None:
    LOGGER.info(f"GPT message: {text}")


def open_app(path: str) -> None:
    """Launches a program. For security, avoids shell=True."""
    try:
        subprocess.Popen([path])
        LOGGER.info(f"Successfully launched application: {path}")
    except FileNotFoundError:
        LOGGER.error(f"Application not found at path: {path}")
    except Exception as e:
        LOGGER.error(f"Failed to launch application '{path}': {e}", exc_info=True)

def run_powershell_script(script: str) -> None:
    """Executes a PowerShell script string safely."""
    try:
        LOGGER.info(f"Executing PowerShell script: {script}")
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            LOGGER.info(f"PowerShell stdout:\n{result.stdout}")
        if result.stderr:
            LOGGER.warning(f"PowerShell stderr:\n{result.stderr}")
        LOGGER.info(f"PowerShell script finished with exit code {result.returncode}")
    except Exception as e:
        LOGGER.error(f"Failed to run PowerShell script: {e}", exc_info=True)

def system_check() -> None:
    """Logs OS, CPU, memory, and disk info as a JSON object."""
    info: Dict[str, Any] = {}
    info["os"] = platform.platform()
    info["cpu_cores"] = os.cpu_count()

    try:
        import psutil
        vm = psutil.virtual_memory()
        info["memory_total_gb"] = round(vm.total / (1024**3), 2)
        info["memory_used_gb"] = round(vm.used / (1024**3), 2)
        info["memory_percent"] = vm.percent
    except ImportError:
        info["memory_note"] = "psutil not installed, cannot get detailed memory info."
    except Exception as e:
        info["memory_error"] = str(e)

    try:
        total, used, free = shutil.disk_usage("C:/")
        info["disk_c_total_gb"] = round(total / (1024**3), 2)
        info["disk_c_used_gb"] = round(used / (1024**3), 2)
        info["disk_c_free_gb"] = round(free / (1024**3), 2)
    except Exception as e:
        info["disk_error"] = str(e)

    LOGGER.info(f"System Check Results:\n{json.dumps(info, indent=2)}")

def delete_file(path: str, confirm: bool = False) -> None:
    """Deletes a file, but only if 'confirm' is explicitly True."""
    if not confirm:
        LOGGER.warning(f"delete_file called without confirm=True for '{path}'. Skipping.")
        return

    if not os.path.exists(path):
        LOGGER.warning(f"File not found for deletion: {path}")
        return

    try:
        os.remove(path)
        LOGGER.info(f"Successfully deleted file: {path}")
    except Exception as e:
        LOGGER.error(f"Failed to delete file '{path}': {e}", exc_info=True)

def kill_process_by_name(name: str) -> None:
    """Terminates a process by its name with safety checks."""
    if not name:
        LOGGER.error("kill_process_by_name requires a 'name'.")
        return

    if name.lower() in PROTECTED_PROCESS_NAMES:
        LOGGER.warning(f"Refusing to kill protected process: {name}")
        return

    try:
        import psutil
    except ImportError:
        LOGGER.error("psutil is required for process management. Please install it.")
        return

    killed_count = 0
    for proc in psutil.process_iter(["pid", "name"]):
        if proc.info["name"].lower() == name.lower():
            try:
                p = psutil.Process(proc.info["pid"])
                p.terminate()
                LOGGER.info(f"Terminated process '{name}' with PID {proc.info['pid']}")
                killed_count += 1
            except psutil.NoSuchProcess:
                LOGGER.warning(f"Process '{name}' with PID {proc.info['pid']} disappeared before it could be killed.")
            except psutil.AccessDenied:
                LOGGER.error(f"Access denied to kill process '{name}' with PID {proc.info['pid']}.")
            except Exception as e:
                LOGGER.error(f"Failed to kill process '{name}' with PID {proc.info['pid']}': {e}", exc_info=True)

    if killed_count == 0:
        LOGGER.info(f"No processes named '{name}' found running.")


def create_file(path: str, content: str = "") -> None:
    """Create a file with content."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        LOGGER.info(f"Created file: {path}")
    except Exception as e:
        LOGGER.error(f"Failed to create file '{path}': {e}", exc_info=True)


def create_folder(path: str) -> None:
    """Create a folder."""
    try:
        os.makedirs(path, exist_ok=True)
        LOGGER.info(f"Created folder: {path}")
    except Exception as e:
        LOGGER.error(f"Failed to create folder '{path}': {e}", exc_info=True)


def move_file(from_path: str, to_path: str) -> None:
    """Move a file."""
    try:
        shutil.move(from_path, to_path)
        LOGGER.info(f"Moved file from '{from_path}' to '{to_path}'")
    except Exception as e:
        LOGGER.error(f"Failed to move file from '{from_path}' to '{to_path}': {e}", exc_info=True)


def copy_file(from_path: str, to_path: str) -> None:
    """Copy a file."""
    try:
        shutil.copy2(from_path, to_path)
        LOGGER.info(f"Copied file from '{from_path}' to '{to_path}'")
    except Exception as e:
        LOGGER.error(f"Failed to copy file from '{from_path}' to '{to_path}': {e}", exc_info=True)


def rename_file(path: str, new_name: str) -> None:
    """Rename a file."""
    try:
        new_path = os.path.join(os.path.dirname(path), new_name)
        os.rename(path, new_path)
        LOGGER.info(f"Renamed file from '{path}' to '{new_path}'")
    except Exception as e:
        LOGGER.error(f"Failed to rename file '{path}': {e}", exc_info=True)


def list_dir(path: str) -> None:
    """List files in a directory."""
    try:
        files = os.listdir(path)
        LOGGER.info(f"Files in '{path}':\n- " + "\n- ".join(files))
    except Exception as e:
        LOGGER.error(f"Failed to list directory '{path}': {e}", exc_info=True)


def read_file(path: str) -> None:
    """Read a text file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        LOGGER.info(f"File content of '{path}':\n{content}")
    except Exception as e:
        LOGGER.error(f"Failed to read file '{path}': {e}", exc_info=True)


def write_file(path: str, content: str) -> None:
    """Write to a file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        LOGGER.info(f"Wrote to file: '{path}'")
    except Exception as e:
        LOGGER.error(f"Failed to write to file '{path}': {e}", exc_info=True)


def append_file(path: str, content: str) -> None:
    """Append to a file."""
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        LOGGER.info(f"Appended to file: '{path}'")
    except Exception as e:
        LOGGER.error(f"Failed to append to file '{path}': {e}", exc_info=True)


def run_instrukey(path: str) -> None:
    """Run InstruKey by full path."""
    try:
        subprocess.run(f'"{path}"', shell=True, check=False)
        LOGGER.info(f"Successfully ran InstruKey: {path}")
    except Exception as e:
        LOGGER.error(f"Failed to run InstruKey '{path}': {e}", exc_info=True)

def scan_defender(path: str) -> None:
    """Run a Windows Defender scan if MpCmdRun.exe is available."""
    possible = [
        r"C:\Program Files\Windows Defender\MpCmdRun.exe",
        r"C:\Program Files\Microsoft Defender\MpCmdRun.exe",
    ]
    exe = next((p for p in possible if os.path.exists(p)), None)
    if not exe:
        LOGGER.warning("Defender CLI not found (MpCmdRun.exe). Skipping scan.")
        return

    try:
        cmd = f'"{exe}" -Scan -ScanType 3 -File "{path}"'
        subprocess.run(cmd, shell=True, check=False)
        LOGGER.info(f"Started Defender scan for: {path}")
    except Exception as e:
        LOGGER.error(f"Failed to start Defender scan for '{path}': {e}", exc_info=True)

def list_processes() -> None:
    """List running processes."""
    try:
        import psutil
        processes = [{"pid": p.info['pid'], "name": p.info['name']} for p in psutil.process_iter(['pid', 'name'])]
        LOGGER.info(f"Running processes:\n{json.dumps(processes, indent=2)}")
    except Exception as e:
        LOGGER.error(f"Failed to list processes: {e}", exc_info=True)

def start_process(path: str, args: str = "") -> None:
    """Start a process with parameters."""
    try:
        subprocess.Popen(f'"{path}" {args}', shell=True)
        LOGGER.info(f"Started process '{path}' with args '{args}'")
    except Exception as e:
        LOGGER.error(f"Failed to start process: {e}", exc_info=True)

# ==============================================================================
# Command Dispatcher
# ==============================================================================

COMMANDS: Dict[str, Callable[..., None]] = {
    "message": show_message,
    "open_app": open_app,
    "run_powershell_script": run_powershell_script,
    "system_check": system_check,
    "delete_file": delete_file,
    "kill_process_by_name": kill_process_by_name,
    "create_file": create_file,
    "create_folder": create_folder,
    "move_file": move_file,
    "copy_file": copy_file,
    "rename_file": rename_file,
    "list_dir": list_dir,
    "read_file": read_file,
    "write_file": write_file,
    "append_file": append_file,
    "run_instrukey": run_instrukey,
    "scan_defender": scan_defender,
    "list_processes": list_processes,
    "start_process": start_process,
}

def normalize_and_validate_command(data: Dict[str, Any]) -> Optional[Tuple[str, Dict[str, Any]]]:
    """
    Normalizes the command format and validates it.
    - Implements the backward-compatible adapter for 'params'.
    - Checks if the command is known and valid.
    """
    if not isinstance(data, dict) or not data:
        return None

    # Backward-compatible adapter
    if "params" not in data:
        params = {k: v for k, v in data.items() if k != "command"}
        data["params"] = params

    command_name = data.get("command")
    if not command_name:
        LOGGER.warning("Command file is missing 'command' key.")
        return None

    if command_name not in COMMANDS:
        LOGGER.warning(f"Unknown/forbidden command received: '{command_name}'")
        return None

    params = data.get("params", {}) or {}
    if not isinstance(params, dict):
        LOGGER.warning(f"Command '{command_name}' has invalid 'params'. Expected a dictionary.")
        return None

    return command_name, params

def dispatch_command(command_name: str, params: Dict[str, Any]) -> None:
    """
    Looks up the command and executes it with the given parameters.
    Handles exceptions during command execution.
    """
    action = COMMANDS[command_name]
    LOGGER.info(f"Executing command: '{command_name}' with params: {params}")

    try:
        action(**params)
        LOGGER.info(f"Successfully executed command: '{command_name}'")
    except TypeError as e:
        LOGGER.error(f"Mismatched parameters for command '{command_name}'. "
                     f"Provided: {list(params.keys())}. Error: {e}", exc_info=True)
    except Exception as e:
        LOGGER.error(f"Error executing command '{command_name}': {e}", exc_info=True)

# ==============================================================================
# Main Agent Loop
# ==============================================================================

def process_command_file() -> None:
    """
    Reads the command from the JSON file, dispatches it, and clears the file.
    """
    try:
        if not os.path.exists(COMMAND_FILE_PATH) or os.path.getsize(COMMAND_FILE_PATH) == 0:
            return  # Ignore if file doesn't exist or is empty

        with open(COMMAND_FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return # Ignore if file is empty after stripping whitespace

            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                LOGGER.warning("Invalid JSON in command file. Clearing it.")
                clear_command_file()
                return

        # Normalize, validate, and dispatch the command
        command_tuple = normalize_and_validate_command(data)
        if command_tuple:
            command_name, params = command_tuple
            dispatch_command(command_name, params)

    except Exception as e:
        LOGGER.error(f"An unexpected error occurred in process_command_file: {e}", exc_info=True)
    finally:
        clear_command_file()

def clear_command_file() -> None:
    """Safely clears the content of the command file."""
    try:
        with open(COMMAND_FILE_PATH, "w", encoding="utf-8") as f:
            f.truncate(0)
    except IOError as e:
        LOGGER.error(f"Could not clear command file {COMMAND_FILE_PATH}: {e}", exc_info=True)

def main() -> None:
    """The main entry point and daemon loop for the LocalAgent."""
    parser = argparse.ArgumentParser(description="LocalAgent: A local command runner.")
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=DEFAULT_POLL_INTERVAL_SEC,
        help="The interval in seconds to poll the command file."
    )
    args = parser.parse_args()
    poll_interval = args.poll_interval

    # Ensure command file exists
    if not os.path.exists(COMMAND_FILE_PATH):
        with open(COMMAND_FILE_PATH, "w", encoding="utf-8") as f:
            f.write("{}")
        LOGGER.info(f"Created command file at: {COMMAND_FILE_PATH}")

    LOGGER.info(f"LocalAgent started. Watching {COMMAND_FILE_PATH}")
    LOGGER.info(f"Poll interval set to {poll_interval} seconds.")

    try:
        while True:
            process_command_file()
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        LOGGER.info("LocalAgent shutting down.")
    except Exception as e:
        LOGGER.critical(f"A critical error occurred in the main loop: {e}", exc_info=True)
    finally:
        LOGGER.info("LocalAgent has stopped.")


if __name__ == "__main__":
    main()