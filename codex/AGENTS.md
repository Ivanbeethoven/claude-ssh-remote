# SSH Remote Development

## When to use SSH remote

When the user asks to work on a remote server, or when the project is configured
for remote execution, route Bash commands through the configured SSH host.

## Connecting

Use `ssh <host>` to establish an SSH connection.

- Plain SSH connection: `ssh <host>`
- Remote directory: `ssh <host> "cd <dir> && exec $SHELL -l"`
- Persistent session: `ssh <host> 'cd <dir> && tmux new-session -A -s <name>'`

## Enforcement mode

When enforcement is enabled, all Bash commands MUST be routed through the
configured SSH host. The PreToolUse hook will intercept and enforce this
automatically.

### Safe commands (auto-rewrite to SSH)

Commands like `pwd`, `ls`, `uname -a`, `python --version` are safe to
transparently proxy through `ssh <host> '<cmd>'`.

### Interactive/unsafe commands (blocked with hint)

Commands like `vim`, `nano`, `top`, `htop`, `tmux`, `screen`, `tail -f`, and
commands with pipes `|` or chains `&&`/`||` are NOT safe to transparently proxy.
They will be blocked. Use `ssh <host>` and run them in the interactive session
instead.

## Configuration file

`.codex/ssh-remote.local.toml`:

```toml
enabled = true
ssh_host = "azure"
mode = "rewrite_or_block"
```

Modes:

- `rewrite_or_block`: auto-rewrite safe commands, block unsafe ones
- `block_only`: never auto-rewrite, always block and show the SSH form