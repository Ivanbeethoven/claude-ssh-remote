---
name: ssh-remote-hook-off
description: Disable SSH Bash enforcement for the current project. Invoke when the user wants to stop forcing Bash commands through a remote SSH host.
---

Disable the SSH enforcement hook for the current project.

## Instructions

1. Look for `.codex/ssh-remote.local.toml` in the current project.
2. If the file does not exist, tell the user the hook is already off.
3. If it exists, change `enabled = true` to `enabled = false`.
4. Confirm that Bash enforcement is disabled for this project.
5. Keep the response short.