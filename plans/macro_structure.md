# Структура макрокоманд

## 1. Введение
Макрокоманды позволяют объединять несколько команд в один сценарий для автоматизации сложных задач.

## 2. Формат макрокоманды

### 2.1. Пример макрокоманды
```json
{
  "command": "macro",
  "name": "backup_project",
  "steps": [
    {
      "command": "create_folder",
      "params": {
        "path": "D:\Backups\ProjectX"
      }
    },
    {
      "command": "copy_file",
      "params": {
        "from": "D:\Projects\ProjectX",
        "to": "D:\Backups\ProjectX"
      }
    },
    {
      "command": "zip_files",
      "params": {
        "path": "D:\Backups\ProjectX",
        "output": "project_backup.zip"
      }
    },
    {
      "command": "message",
      "params": {
        "text": "✅ Backup completed!"
      }
    }
  ]
}
```

### 2.2. Описание полей
- `command`: Всегда `macro` для макрокоманд.
- `name`: Имя макрокоманды (опционально, для логирования).
- `steps`: Список команд, которые будут выполнены последовательно.

## 3. Хранение макрокоманд

### 3.1. Файл макрокоманд
Макрокоманды будут храниться в файле `macros.json` в корне проекта.

### 3.2. Пример файла `macros.json`
```json
{
  "macros": [
    {
      "name": "backup_project",
      "steps": [
        {
          "command": "create_folder",
          "params": {
            "path": "D:\Backups\ProjectX"
          }
        },
        {
          "command": "copy_file",
          "params": {
            "from": "D:\Projects\ProjectX",
            "to": "D:\Backups\ProjectX"
          }
        },
        {
          "command": "zip_files",
          "params": {
            "path": "D:\Backups\ProjectX",
            "output": "project_backup.zip"
          }
        },
        {
          "command": "message",
          "params": {
            "text": "✅ Backup completed!"
          }
        }
      ]
    },
    {
      "name": "system_diagnostics",
      "steps": [
        {
          "command": "system_check",
          "params": {}
        },
        {
          "command": "get_ram_usage",
          "params": {}
        },
        {
          "command": "get_cpu_usage",
          "params": {}
        }
      ]
    }
  ]
}
```

## 4. Обработка макрокоманд

### 4.1. Логика выполнения
1. При получении команды `macro`, агент загружает файл `macros.json`.
2. Находит макрокоманду по имени (если указано).
3. Последовательно выполняет все шаги из списка `steps`.
4. Если макрокоманда не найдена, выводится сообщение об ошибке.

### 4.2. Обработка ошибок
- Если одна из команд в макрокоманде завершается с ошибкой, выполнение макрокоманды прекращается.
- Логируются все ошибки для отладки.

## 5. Примеры использования

### 5.1. Запуск макрокоманды через CLI
```powershell
python agent.py send macro --param name=backup_project
```

### 5.2. Запуск макрокоманды через файл
```json
{
  "command": "macro",
  "params": {
    "name": "backup_project"
  }
}
```

## 6. Заключение
Макрокоманды предоставляют мощный инструмент для автоматизации сложных задач, объединяя несколько команд в один сценарий.