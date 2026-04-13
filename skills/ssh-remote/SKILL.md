---
name: ssh-remote
description: Connect to a remote SSH dev environment
argument-hint: [host-alias] [remote-dir] [session-name]
allowed-tools:
  - Bash(ssh:*)
  - Bash(command -v:*)
---

Connect to a remote server over SSH for ongoing development work.

## Arguments

The user invoked this command with: `$ARGUMENTS`

Interpret arguments as:
1. `host-alias` (required): SSH Host from `~/.ssh/config`
2. `remote-dir` (optional): remote project directory to `cd` into
3. `session-name` (optional): persistent session name; prefer `tmux`, fallback to `screen`

## Instructions

1. Parse `$ARGUMENTS` into up to 3 positional arguments.
2. If `host-alias` is missing, ask the user for it and stop.
3. Prefer connecting with plain `ssh <host-alias>`.
4. If only `host-alias` is provided, run a Bash command that starts a normal SSH session.
5. If `remote-dir` is provided but no `session-name`, run SSH and execute:
   - `cd <remote-dir>`
   - if that succeeds, start an interactive login shell in that directory
6. If `session-name` is provided, run SSH and on the remote host:
   - `cd <remote-dir>` if provided
   - if `tmux` exists, attach to session if it exists or create it if it does not
   - otherwise, if `screen` exists, attach/create a session with the same name
   - otherwise, fall back to a normal interactive shell in that directory
7. Quote shell arguments safely. Do not interpolate raw user input without quoting.
8. If the SSH command fails, report the actual error briefly.
9. After starting the remote session, tell the user that subsequent coding work should continue inside that remote shell.

## Preferred command shapes

### Host only
Use:

```bash
ssh <host-alias>
```

### Host + directory
Use a remote shell command equivalent to:

```bash
ssh <host-alias> "cd <remote-dir> && exec \$SHELL -l"
```

### Host + directory + session
Use a remote shell command equivalent to:

```bash
ssh <host-alias> 'cd <remote-dir> && if command -v tmux >/dev/null 2>&1; then tmux new-session -A -s <session-name>; elif command -v screen >/dev/null 2>&1; then screen -xRR <session-name>; else exec "$SHELL" -l; fi'
```

## Notes

- Assume host aliases are maintained in the user's SSH config.
- Do not add support for explicit `user@host` / `port` flags unless the user asks.
- Prefer `tmux` over `screen`.
- Keep the response short and action-oriented.
