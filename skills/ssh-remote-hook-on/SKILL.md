---
name: ssh-remote-hook-on
description: Enable SSH Bash enforcement for the current project
argument-hint: [ssh-host]
allowed-tools:
  - Bash(ls:*)
  - Bash(mkdir:*)
  - Write
---

Enable the SSH enforcement hook for the current project.

## Arguments

The user invoked this command with: `$ARGUMENTS`

Interpret arguments as:
1. `ssh-host` (required): SSH Host from `~/.ssh/config`, for example `azure`

## Instructions

1. Parse `$ARGUMENTS` and extract `ssh-host`.
2. If `ssh-host` is missing, ask the user for it and stop.
3. Ensure the current project's `.claude/` directory exists.
4. Write `.claude/claude-ssh-remote.local.md` with:

```markdown
---
enabled: true
ssh_host: <ssh-host>
mode: rewrite_or_block
---
```

5. Confirm that Bash enforcement is now enabled for this project.
6. Tell the user that:
   - normal Bash commands will now be forced through `ssh <ssh-host>` when safe
   - clearly interactive or unsafe-to-proxy Bash commands will be blocked with guidance instead of auto-run
   - `/ssh-remote-hook-off` disables the hook

Keep the response short.
