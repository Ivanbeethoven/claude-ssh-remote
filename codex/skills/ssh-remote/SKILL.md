---
name: ssh-remote
description: Connect to a remote SSH dev environment. Invoke when the user wants to SSH into a remote server for development work, or mentions a remote host by name.
argument-hint: [ssh-host] [remote-dir] [session-name]
---

Connect to a remote server over SSH for ongoing development work.

The user invoked this command with: `$ARGUMENTS`

Interpret arguments as:
1. `ssh-host` (required): SSH Host from `~/.ssh/config`, for example `azure`
2. `remote-dir` (optional): remote project directory to `cd` into
3. `session-name` (optional): persistent session name; prefer `tmux`, fallback to `screen`

## Instructions

1. Parse `$ARGUMENTS` into up to 3 positional arguments.
2. If `ssh-host` is missing, ask the user for it and stop.
3. Treat `ssh-host` strictly as an SSH config host alias, not as a raw `user@host` string.
4. Prefer connecting with plain `ssh <ssh-host>`.
5. If only `ssh-host` is provided, run a Bash command that starts a normal SSH session.
6. If `remote-dir` is provided but no `session-name`, run SSH and execute:
   - `cd <remote-dir>`
   - if that succeeds, start an interactive login shell in that directory
7. If `session-name` is provided, run SSH and on the remote host:
   - `cd <remote-dir>` if provided
   - if `tmux` exists, attach to session if it exists or create it if it does not
   - otherwise, if `screen` exists, attach/create a session with the same name
   - otherwise, fall back to a normal interactive shell in that directory
8. Quote shell arguments safely. Do not interpolate raw user input without quoting.
9. If the SSH command fails, report the actual error briefly.
10. After starting the remote session, tell the user that subsequent coding work should continue inside that remote shell.

## Preferred command shapes

### Host only

```bash
ssh <ssh-host>
```

### Host + directory

```bash
ssh <ssh-host> "cd <remote-dir> && exec \$SHELL -l"
```

### Host + directory + session

```bash
ssh <ssh-host> 'cd <remote-dir> && if command -v tmux >/dev/null 2>&1; then tmux new-session -A -s <session-name>; elif command -v screen >/dev/null 2>&1; then screen -xRR <session-name>; else exec "$SHELL" -l; fi'
```

## Notes

- Assume SSH host aliases are maintained in the user's SSH config.
- Optimize for the common case: `ssh azure`.
- Do not add support for explicit `user@host` / `port` flags unless the user asks.
- Prefer `tmux` over `screen`.
- Keep the response short and action-oriented.