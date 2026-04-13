# SSH Remote Development

This project supports SSH remote execution. When configured, all Bash commands
should run through a remote SSH host instead of locally.

## Configuration

Check `.claude/claude-ssh-remote.local.md` for enforcement settings:

- `enabled: true/false` — whether enforcement is active
- `ssh_host: <alias>` — SSH config host alias (e.g., `azure`)
- `mode: rewrite_or_block | block_only` — enforcement behavior

For Codex CLI, config can also live at `.codex/ssh-remote.local.toml`:

```toml
enabled = true
ssh_host = "azure"
mode = "rewrite_or_block"
```

## Rules when enforcement is enabled

- Safe non-interactive commands: rewrite to `ssh <host> '<cmd>'` and execute
- Interactive/unsafe commands: do not execute; suggest the user run them in an
  SSH session
- Already-remote commands (ssh/scp/sftp): allow through unchanged
- NEVER execute commands locally when enforcement is active

## Connecting

```bash
ssh <host>                                    # plain connection
ssh <host> "cd <dir> && exec $SHELL -l"       # with directory
ssh <host> 'cd <dir> && tmux new-session -A -s <name>'  # with tmux session
```