# SSH Remote Development Rules

## CRITICAL: Remote-Only Execution

When SSH remote enforcement is enabled for this project, you MUST follow these
rules without exception:

1. **NEVER execute Bash commands locally.** All Bash/shell commands must be run
   remotely via `ssh <configured-host> '<command>'`.

2. **Configuration check:** Before executing any Bash command, check if the file
   `.claude/claude-ssh-remote.local.md` exists and has `enabled: true`. If it
   does, read the `ssh_host` and `mode` fields.

3. **Safe commands (non-interactive, no pipes/chains):** Rewrite to
   `ssh <host> '<original-command>'` and execute that instead.
   Examples:
   - `pwd` becomes `ssh azure 'pwd'`
   - `ls -la` becomes `ssh azure 'ls -la'`
   - `python --version` becomes `ssh azure 'python --version'`
   - `cat /etc/os-release` becomes `ssh azure 'cat /etc/os-release'`
   - `git status` becomes `ssh azure 'git status'`

4. **Interactive/unsafe commands (BLOCKED):** Do NOT execute these commands,
   neither locally nor remotely. Instead, tell the user to run them manually
   in their SSH session:
   - vim, vi, nano, top, htop, tmux, screen, less, more, man, watch
   - tail -f, tailf
   - Commands with pipes (|), chains (&&, ||)
   - ssh, scp, sftp (these are already remote, allow through unchanged)

5. **Connecting to remote:** When the user asks to connect to a remote server,
   run: `ssh <host>` (or with directory/session as requested).

6. **Mode `rewrite_or_block`:** Auto-rewrite safe commands, block unsafe ones.
7. **Mode `block_only`:** Never auto-rewrite. Always block and show the SSH
   form for the user to run manually.

## What NOT to do

- Do NOT run commands locally when enforcement is enabled.
- Do NOT try to transparently proxy interactive commands through SSH.
- Do NOT ignore the configuration file if it exists and is enabled.

## Enabling enforcement

Create or update `.claude/claude-ssh-remote.local.md`:

```markdown
---
enabled: true
ssh_host: azure
mode: rewrite_or_block
---
```

## Disabling enforcement

Update `.claude/claude-ssh-remote.local.md` to set `enabled: false`, or delete
the file entirely.