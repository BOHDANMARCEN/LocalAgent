# Commands

All commands use the JSON format:

```json
{
  "command": "name",
  "params": { }
}
```

## Security Levels

### SAFE (executed without confirmation)
- `message`, `open_app`, `list_dir`, `get_file_info`, `clipboard_get`, `system_check`, `get_mouse_position`, `get_active_window`, `find_file`, `find_files`, `find_in_file`, `compare_files`, `count_words`, `get_file_hash`, `get_folder_size`, `get_ram_usage`, `get_cpu_usage`, `get_disk_space`, `list_drives`, `check_internet`, `get_ip`, `list_processes`, `git_status`, `json_read`.

### MEDIUM (with logging)
- `create_file`, `move_file`, `type_text`, `screenshot`, `read_file`, `write_file`, `append_file`, `replace_in_file`, `insert_line`, `delete_line`, `create_folder`, `copy_file`, `rename_file`, `mouse_move`, `mouse_click`, `press_key`, `hotkey`, `wait`, `ping`, `set_volume`, `mute`, `unmute`, `git_pull`, `git_commit`, `json_write`, `sqlite_query`.

### DANGEROUS (with mandatory confirmation)
- `delete_file`, `kill_process`, `shutdown_pc`, `restart_pc`, `sleep_pc`, `lock_screen`, `download_file`, `encrypt_file`, `decrypt_file`, `run_script`, `start_process`, `restart_app`, `set_priority`, `git_push`, `schedule_command`, `sync_folders`, `registry_write`, `registry_delete`, `create_scheduled_task`, `delete_scheduled_task`.

### CRITICAL (with double confirmation and logging)
- `delete_folder`, `format_drive`, `set_env_var`, `docker_stop`, `docker_remove`.

## File System (Extended)

### create_file
Creates a file with content.

Params:
- path: string
- content: string (optional)

Example:
```json
{
  "command": "create_file",
  "params": { "path": "C:/Temp/test.txt", "content": "Hello, World!" }
}
```

### create_folder
Creates a folder.

Params:
- path: string

Example:
```json
{
  "command": "create_folder",
  "params": { "path": "C:/Temp/NewFolder" }
}
```

### move_file
Moves a file.

Params:
- from: string
- to: string

Example:
```json
{
  "command": "move_file",
  "params": { "from": "C:/Temp/test.txt", "to": "C:/Temp/NewFolder/test.txt" }
}
```

### copy_file
Copies a file.

Params:
- from: string
- to: string

Example:
```json
{
  "command": "copy_file",
  "params": { "from": "C:/Temp/test.txt", "to": "C:/Temp/NewFolder/test.txt" }
}
```

### rename_file
Renames a file.

Params:
- path: string
- new_name: string

Example:
```json
{
  "command": "rename_file",
  "params": { "path": "C:/Temp/test.txt", "new_name": "new_test.txt" }
}
```

### list_dir
Lists files in a directory.

Params:
- path: string

Example:
```json
{
  "command": "list_dir",
  "params": { "path": "C:/Temp" }
}
```

### find_file
Searches for a file by name or pattern.

Params:
- path: string
- pattern: string

Example:
```json
{
  "command": "find_file",
  "params": { "path": "C:/Temp", "pattern": "*.txt" }
}
```

### get_file_info
Gets file information (size, creation date, attributes).

Params:
- path: string

Example:
```json
{
  "command": "get_file_info",
  "params": { "path": "C:/Temp/test.txt" }
}
```

### zip_files
Archives files.

Params:
- path: string
- output: string

Example:
```json
{
  "command": "zip_files",
  "params": { "path": "C:/Temp/NewFolder", "output": "archive.zip" }
}
```

### unzip_file
Extracts an archive.

Params:
- path: string
- output: string

Example:
```json
{
  "command": "unzip_file",
  "params": { "path": "archive.zip", "output": "C:/Temp/Extracted" }
}
```

### insert_line
Inserts a line at a specific position in a file.

Params:
- path: string
- line_number: number
- content: string

Example:
```json
{
  "command": "insert_line",
  "params": { "path": "C:/Temp/test.txt", "line_number": 5, "content": "New line" }
}
```

### delete_line
Deletes a specific line from a file.

Params:
- path: string
- line_number: number

Example:
```json
{
  "command": "delete_line",
  "params": { "path": "C:/Temp/test.txt", "line_number": 3 }
}
```

### find_in_file
Searches for text in a file.

Params:
- path: string
- text: string
- regex: bool (optional)

Example:
```json
{
  "command": "find_in_file",
  "params": { "path": "C:/Temp/test.txt", "text": "search term", "regex": false }
}
```

### count_words
Counts words in a file.

Params:
- path: string

Example:
```json
{
  "command": "count_words",
  "params": { "path": "C:/Temp/document.txt" }
}
```

### get_file_hash
Gets the hash of a file.

Params:
- path: string
- algorithm: string (optional, default: sha256)

Example:
```json
{
  "command": "get_file_hash",
  "params": { "path": "C:/Temp/test.txt", "algorithm": "md5" }
}
```

### find_files
Searches for files recursively with filters.

Params:
- path: string
- pattern: string
- max_depth: number (optional)

Example:
```json
{
  "command": "find_files",
  "params": { "path": "C:/", "pattern": "*.log", "max_depth": 3 }
}
```

### sync_folders
Synchronizes two folders.

Params:
- source: string
- destination: string
- mode: string (mirror, update, merge)

Example:
```json
{
  "command": "sync_folders",
  "params": { "source": "C:/Source", "destination": "C:/Backup", "mode": "mirror" }
}
```

### compare_files
Compares two files.

Params:
- file1: string
- file2: string
- method: string (hash, content, binary)

Example:
```json
{
  "command": "compare_files",
  "params": { "file1": "C:/version1.txt", "file2": "C:/version2.txt", "method": "hash" }
}
```

### get_folder_size
Gets the size of a folder.

Params:
- path: string
- format: string (bytes, kb, mb, gb)

Example:
```json
{
  "command": "get_folder_size",
  "params": { "path": "C:/Projects", "format": "mb" }
}
```

## Processes and Applications

### kill_process
Kills a process by name or PID.

Params:
- name: string (optional)
- pid: number (optional)

Example:
```json
{
  "command": "kill_process",
  "params": { "name": "notepad.exe" }
}
```

### list_processes
Lists running processes.

Params: none

Example:
```json
{
  "command": "list_processes",
  "params": {}
}
```

### start_process
Starts a process with parameters.

Params:
- path: string
- args: string (optional)

Example:
```json
{
  "command": "start_process",
  "params": { "path": "notepad.exe", "args": "test.txt" }
}
```

### restart_app
Restarts an application.

Params:
- name: string

Example:
```json
{
  "command": "restart_app",
  "params": { "name": "notepad.exe" }
}
```

### check_if_running
Checks if a process is running.

Params:
- name: string

Example:
```json
{
  "command": "check_if_running",
  "params": { "name": "notepad.exe" }
}
```

### set_priority
Sets process priority.

Params:
- name: string
- priority: string (low, normal, high)

Example:
```json
{
  "command": "set_priority",
  "params": { "name": "notepad.exe", "priority": "high" }
}
```

## Automation (Extended)

### type_text
Types text.

Params:
- text: string

Example:
```json
{
  "command": "type_text",
  "params": { "text": "Hello, World!" }
}
```

### press_key
Presses a key.

Params:
- key: string

Example:
```json
{
  "command": "press_key",
  "params": { "key": "enter" }
}
```

### hotkey
Presses a key combination.

Params:
- keys: string

Example:
```json
{
  "command": "hotkey",
  "params": { "keys": "ctrl+c" }
}
```

### mouse_click
Clicks the mouse at coordinates.

Params:
- x: number
- y: number
- button: string (left, right, middle)

Example:
```json
{
  "command": "mouse_click",
  "params": { "x": 100, "y": 200, "button": "left" }
}
```

### mouse_move
Moves the mouse cursor.

Params:
- x: number
- y: number

Example:
```json
{
  "command": "mouse_move",
  "params": { "x": 100, "y": 200 }
}
```

### screenshot
Takes a screenshot.

Params:
- path: string

Example:
```json
{
  "command": "screenshot",
  "params": { "path": "C:/Temp/screenshot.png" }
}
```

### wait
Delays execution in seconds.

Params:
- seconds: number

Example:
```json
{
  "command": "wait",
  "params": { "seconds": 5 }
}
```

## Network and Internet

### ping
Pings a host.

Params:
- host: string

Example:
```json
{
  "command": "ping",
  "params": { "host": "google.com" }
}
```

### download_file
Downloads a file (with confirmation).

Params:
- url: string
- path: string

Example:
```json
{
  "command": "download_file",
  "params": { "url": "https://example.com/file.txt", "path": "C:/Temp/file.txt" }
}
```

### check_internet
Checks internet connection.

Params: none

Example:
```json
{
  "command": "check_internet",
  "params": {}
}
```

### get_ip
Gets IP address.

Params: none

Example:
```json
{
  "command": "get_ip",
  "params": {}
}
```

## System (Extended)

### get_ram_usage
Gets RAM usage information.

Params: none

Example:
```json
{
  "command": "get_ram_usage",
  "params": {}
}
```

### get_cpu_usage
Gets CPU usage information.

Params: none

Example:
```json
{
  "command": "get_cpu_usage",
  "params": {}
}
```

### get_disk_space
Gets disk space information.

Params:
- drive: string (optional)

Example:
```json
{
  "command": "get_disk_space",
  "params": { "drive": "C:" }
}
```

### list_drives
Lists available drives.

Params: none

Example:
```json
{
  "command": "list_drives",
  "params": {}
}
```

### set_volume
Sets volume level.

Params:
- level: number (0-100)

Example:
```json
{
  "command": "set_volume",
  "params": { "level": 50 }
}
```

### mute
Mutes the sound.

Params: none

Example:
```json
{
  "command": "mute",
  "params": {}
}
```

### unmute
Unmutes the sound.

Params: none

Example:
```json
{
  "command": "unmute",
  "params": {}
}
```

### sleep_pc
Puts the computer to sleep.

Params: none

Example:
```json
{
  "command": "sleep_pc",
  "params": {}
}
```

### shutdown_pc
Shuts down the computer (with confirmation).

Params:
- confirm: bool (must be true)

Example:
```json
{
  "command": "shutdown_pc",
  "params": { "confirm": true }
}
```

### restart_pc
Restarts the computer (with confirmation).

Params:
- confirm: bool (must be true)

Example:
```json
{
  "command": "restart_pc",
  "params": { "confirm": true }
}
```

### lock_screen
Locks the screen.

Params: none

Example:
```json
{
  "command": "lock_screen",
  "params": {}
}
```

## Clipboard

### clipboard_copy
Copies text to clipboard.

Params:
- text: string

Example:
```json
{
  "command": "clipboard_copy",
  "params": { "text": "Hello, World!" }
}
```

### clipboard_paste
Pastes text from clipboard.

Params: none

Example:
```json
{
  "command": "clipboard_paste",
  "params": {}
}
```

### clipboard_get
Gets clipboard content.

Params: none

Example:
```json
{
  "command": "clipboard_get",
  "params": {}
}
```

### clipboard_clear
Clears the clipboard.

Params: none

Example:
```json
{
  "command": "clipboard_clear",
  "params": {}
}
```

## Text and Documents

### read_file
Reads a text file.

Params:
- path: string

Example:
```json
{
  "command": "read_file",
  "params": { "path": "C:/Temp/test.txt" }
}
```

### write_file
Writes to a file.

Params:
- path: string
- content: string

Example:
```json
{
  "command": "write_file",
  "params": { "path": "C:/Temp/test.txt", "content": "Hello, World!" }
}
```

### append_file
Appends to a file.

Params:
- path: string
- content: string

Example:
```json
{
  "command": "append_file",
  "params": { "path": "C:/Temp/test.txt", "content": "Hello, World!" }
}
```

### replace_in_file
Replaces text in a file.

Params:
- path: string
- old_text: string
- new_text: string

Example:
```json
{
  "command": "replace_in_file",
  "params": { "path": "C:/Temp/test.txt", "old_text": "Hello", "new_text": "Hi" }
}
```

### count_lines
Counts lines in a file.

Params:
- path: string

Example:
```json
{
  "command": "count_lines",
  "params": { "path": "C:/Temp/test.txt" }
}
```

## Multimedia

### play_sound
Plays a sound.

Params:
- path: string

Example:
```json
{
  "command": "play_sound",
  "params": { "path": "C:/Temp/sound.wav" }
}
```

### stop_sound
Stops sound playback.

Params: none

Example:
```json
{
  "command": "stop_sound",
  "params": {}
}
```

### open_url
Opens a URL in the browser.

Params:
- url: string

Example:
```json
{
  "command": "open_url",
  "params": { "url": "https://example.com" }
}
```

### take_photo
Takes a photo from the webcam (if available).

Params:
- path: string

Example:
```json
{
  "command": "take_photo",
  "params": { "path": "C:/Temp/photo.jpg" }
}
```

## Security

### hash_file
Calculates file hash (MD5, SHA256).

Params:
- path: string
- algorithm: string (optional, default: sha256)

Example:
```json
{
  "command": "hash_file",
  "params": { "path": "C:/Temp/test.txt", "algorithm": "sha256" }
}
```

### encrypt_file
Encrypts a file.

Params:
- path: string
- output: string

Example:
```json
{
  "command": "encrypt_file",
  "params": { "path": "C:/Temp/test.txt", "output": "C:/Temp/test.enc" }
}
```

### decrypt_file
Decrypts a file.

Params:
- path: string
- output: string

Example:
```json
{
  "command": "decrypt_file",
  "params": { "path": "C:/Temp/test.enc", "output": "C:/Temp/test.txt" }
}
```

### check_hash
Checks file integrity by hash.

Params:
- path: string
- hash: string

Example:
```json
{
  "command": "check_hash",
  "params": { "path": "C:/Temp/test.txt", "hash": "a1b2c3..." }
}
```

## Scheduling

### schedule_command
Schedules a command for a specific time.

Params:
- command: string
- params: object
- time: string (ISO format)

Example:
```json
{
  "command": "schedule_command",
  "params": { "command": "message", "params": { "text": "Hello" }, "time": "2026-01-21T20:00:00" }
}
```

### cancel_scheduled
Cancels a scheduled command.

Params:
- id: string

Example:
```json
{
  "command": "cancel_scheduled",
  "params": { "id": "abc123" }
}
```

### list_scheduled
Lists scheduled commands.

Params: none

Example:
```json
{
  "command": "list_scheduled",
  "params": {}
}
```

## Git and Development

### git_status
Runs git status.

Params:
- path: string (optional)

Example:
```json
{
  "command": "git_status",
  "params": { "path": "C:/Projects/MyProject" }
}
```

### git_pull
Runs git pull.

Params:
- path: string (optional)

Example:
```json
{
  "command": "git_pull",
  "params": { "path": "C:/Projects/MyProject" }
}
```

### git_commit
Runs git commit.

Params:
- path: string (optional)
- message: string

Example:
```json
{
  "command": "git_commit",
  "params": { "path": "C:/Projects/MyProject", "message": "Update README" }
}
```

### git_push
Runs git push.

Params:
- path: string (optional)

Example:
```json
{
  "command": "git_push",
  "params": { "path": "C:/Projects/MyProject" }
}
```

### run_script
Runs a script (.bat, .ps1).

Params:
- path: string

Example:
```json
{
  "command": "run_script",
  "params": { "path": "C:/Temp/script.bat" }
}
```

## Local Databases

### sqlite_query
Runs a SQL query on SQLite.

Params:
- path: string
- query: string

Example:
```json
{
  "command": "sqlite_query",
  "params": { "path": "C:/Temp/database.db", "query": "SELECT * FROM users" }
}
```

### sqlite_insert
Inserts data into SQLite.

Params:
- path: string
- table: string
- data: object

Example:
```json
{
  "command": "sqlite_insert",
  "params": { "path": "C:/Temp/database.db", "table": "users", "data": { "name": "John", "age": 30 } }
}
```

### json_read
Reads a JSON file.

Params:
- path: string

Example:
```json
{
  "command": "json_read",
  "params": { "path": "C:/Temp/data.json" }
}
```

### json_write
Writes to a JSON file.

Params:
- path: string
- data: object

Example:
```json
{
  "command": "json_write",
  "params": { "path": "C:/Temp/data.json", "data": { "name": "John", "age": 30 } }
}
```

## Macros

### macro
Executes a macro (sequence of commands).

Params:
- name: string

Example:
```json
{
  "command": "macro",
  "params": { "name": "backup_project" }
}
```
