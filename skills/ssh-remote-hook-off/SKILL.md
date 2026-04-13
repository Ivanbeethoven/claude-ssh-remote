---
name: ssh-remote-hook-off
description: Disable SSH Bash enforcement for the current project
allowed-tools:
  - Read
  - Edit
---

Disable the SSH enforcement hook for the current project.

## Instructions

1. Look for `.claude/claude-ssh-remote.local.md` in the current project.
2. If the file does not exist, tell the user the hook is already off.
3. If it exists, change `enabled: true` to `enabled: false`.
4. Confirm that Bash enforcement is disabled for this project.
5. Keep the response short.
