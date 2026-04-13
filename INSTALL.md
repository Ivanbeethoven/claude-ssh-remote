# Install from GitHub

This plugin should be installed with the fewest possible steps.

Repository:

- `https://github.com/Ivanbeethoven/claude-ssh-remote`

## Fastest install

### Option A: run Claude directly with this plugin directory

```bash
git clone https://github.com/Ivanbeethoven/claude-ssh-remote.git
cd claude-ssh-remote
cc --plugin-dir .
```

This is the most direct development-friendly flow.

## After Claude starts

### Connect to the remote host

```text
/ssh-remote azure
```

### Enable Bash enforcement for this project

```text
/ssh-remote-hook-on azure
```

### Disable Bash enforcement for this project

```text
/ssh-remote-hook-off
```

The first command is designed to map directly to:

```bash
ssh azure
```

## What the commands expect

The `ssh-host` argument is only your SSH config host alias.

Example SSH config:

```sshconfig
Host azure
  HostName 20.1.2.3
  User hxy
  Port 22
  IdentityFile ~/.ssh/id_rsa
```

## Hook mode setup

When you run:

```text
/ssh-remote-hook-on azure
```

Claude writes this project config file:

```text
.claude/claude-ssh-remote.local.md
```

Example content:

```markdown
---
enabled: true
ssh_host: azure
mode: rewrite_or_block
---
```

Modes:

- `rewrite_or_block`: auto-run safe non-interactive Bash through `ssh azure`, then block the original local Bash
- `block_only`: do not auto-run, only block and tell you which `ssh azure '...'` command to use

## Hook behavior

The hook only targets Claude's `Bash` tool.

- safe non-interactive Bash commands can be auto-executed remotely
- interactive or unsafe-to-proxy Bash commands are blocked and shown as suggestions instead
- existing `ssh`, `scp`, and `sftp` commands are allowed through unchanged

## If you want to open the repo first

```bash
git clone https://github.com/Ivanbeethoven/claude-ssh-remote.git
code claude-ssh-remote
cd claude-ssh-remote
cc --plugin-dir .
```

## Important notes

- first make sure `ssh azure` already works in your terminal
- the plugin expects the first argument to be an SSH config host alias
- it is optimized for the simple case `ssh azure`
- keep host, user, port, and identity settings in `~/.ssh/config`
- do not pass `user@host` unless you intentionally change the skill later
- the hook mode currently enforces Claude's Bash tool; it does not rewrite every possible tool automatically

## Files in this repo

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
