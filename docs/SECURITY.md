# Security

## Threat model
- Accidental or malicious JSON could trigger commands.
- Running as admin increases impact.
- Adding a generic shell command would be dangerous.

## Mitigations
- Whitelist only known commands.
- No network listener and no remote API.
- delete_file requires confirm=true.
- Command file is cleared before execution.

## Safe usage guidelines
- Keep COMMANDS small.
- Do not add a general shell or eval command.
- Run as a standard user.
- Review JSON before writing it.
