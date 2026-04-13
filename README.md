# Claude SSH Remote

A standalone Claude Code plugin repo for opening a remote development shell over SSH.

## What it provides

- `/ssh-remote <ssh-host>`
- `/ssh-remote-hook-on <ssh-host>`
- `/ssh-remote-hook-off`
- optional remote working directory
- optional persistent session via `tmux`, with `screen` fallback
- SSH host lookup via your existing `~/.ssh/config`
- optimized for the simple case: `ssh azure`
- optional hook mode to force Bash commands through a configured SSH host

## Fastest start

```bash
git clone https://github.com/Ivanbeethoven/claude-ssh-remote.git
cd claude-ssh-remote
cc --plugin-dir .
```

Then in Claude Code:

```text
/ssh-remote azure
```

## Current layout

```text
claude-ssh-remote/
├── .claude-plugin/
│   └── plugin.json
├── hooks/
│   ├── hooks.json
│   └── ssh_enforce_hook.py
├── skills/
│   ├── ssh-remote/
│   │   └── SKILL.md
│   ├── ssh-remote-hook-on/
│   │   └── SKILL.md
│   └── ssh-remote-hook-off/
│       └── SKILL.md
├── INSTALL.md
├── README.md
└── 使用手册.md
```

## Quick usage

### Connect to remote

```text
/ssh-remote azure
```

This is designed to map directly to:

```bash
ssh azure
```

### Enable Bash enforcement for this project

```text
/ssh-remote-hook-on azure
```

### Disable Bash enforcement for this project

```text
/ssh-remote-hook-off
```

## Hook mode

When enabled, the hook only targets Claude's `Bash` tool.

Behavior:

- safe non-interactive Bash commands are rewritten to run through `ssh <configured-host>`
- the original local Bash execution is blocked
- interactive or unsafe-to-proxy Bash commands are blocked and shown as a remote command suggestion instead of being auto-run
- existing `ssh` / `scp` / `sftp` commands are left alone

Project config file:

```text
.claude/claude-ssh-remote.local.md
```

Example:

```markdown
---
enabled: true
ssh_host: azure
mode: rewrite_or_block
---
```

Supported modes:

- `rewrite_or_block`: try remote execution first, otherwise block
- `block_only`: never auto-run, only block and tell you the SSH form

## Install

See [INSTALL.md](INSTALL.md) for the shortest GitHub-based install flow.

## Chinese guide

See [使用手册.md](使用手册.md) for Chinese instructions, including how to enable and disable the hook mode.

## Notes

- keep host, user, port, and identity settings in your SSH config
- this plugin intentionally keeps arguments minimal and does not add explicit `user@host` or `port` flags
- the command is designed for interactive remote development sessions, not one-off remote execution
- the hook currently targets Claude's Bash tool, not every possible tool type
