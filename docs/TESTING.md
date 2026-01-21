# Testing

## Manual checklist
1. Start the agent: `python agent.py`.
2. Write a message command and verify console output.
3. Run open_app with notepad.
4. Run system_check and verify JSON output.
5. Create a temp file and run delete_file without confirm; verify it stays.
6. Run delete_file with confirm=true; verify deletion.
7. Write invalid JSON; verify it is ignored.
8. Use an unknown command; verify warning output.
