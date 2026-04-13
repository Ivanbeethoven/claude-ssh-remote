# Claude SSH Remote

A multi-platform plugin for opening a remote development shell over SSH.
Works with **Claude Code**, **OpenAI Codex CLI**, and **GitHub Copilot coding agent**.

## What it provides

- `/ssh-remote <ssh-host>` — connect to a remote server
- `/ssh-remote-hook-on <ssh-host>` — enforce Bash commands through SSH
- `/ssh-remote-hook-off` — disable enforcement
- optional remote working directory
- optional persistent session via `tmux`, with `screen` fallback
- SSH host lookup via your existing `~/.ssh/config`
- optimized for the simple case: `ssh azure`

## Quick start

### Claude Code

```bash
git clone https://github.com/Ivanbeethoven/claude-ssh-remote.git
cd claude-ssh-remote
cc --plugin-dir .
```

```text
/ssh-remote azure
```

### OpenAI Codex CLI

```bash
git clone https://github.com/Ivanbeethoven/claude-ssh-remote.git
# Copy skills and hooks into your Codex config
# See codex/config-snippet.toml for details
codex
```

### GitHub Copilot

Copy `github/copilot-instructions.md` to `.github/copilot-instructions.md` in your
project. Copy `AGENTS.md` to your repo root.

## Current layout

```text
claude-ssh-remote/
├── core/                           # shared enforcement logic
│   ├── config.py
│   └── ssh_enforce.py
├── .claude-plugin/
│   └── plugin.json
├── hooks/                          # Claude Code hooks
│   ├── hooks.json
│   ├── claude_hook_adapter.py
│   └── ssh_enforce_hook.py         # deprecated, delegates to adapter
├── skills/                         # Claude Code skills
│   ├── ssh-remote/SKILL.md
│   ├── ssh-remote-hook-on/SKILL.md
│   └── ssh-remote-hook-off/SKILL.md
├── codex/                          # Codex CLI integration
│   ├── AGENTS.md
│   ├── skills/
│   │   ├── ssh-remote/SKILL.md
│   │   ├── ssh-remote-hook-on/SKILL.md
│   │   └── ssh-remote-hook-off/SKILL.md
│   ├── codex_hook_adapter.py
│   ├── hooks.json
│   └── config-snippet.toml
├── github/                         # GitHub Copilot integration
│   ├── copilot-instructions.md
│   └── instructions/
│       └── ssh-remote.instructions.md
├── AGENTS.md                       # shared agent instructions
├── INSTALL.md
├── README.md
└── 使用手册.md
```

## Quick usage

### Connect to remote

| Platform | Command |
|----------|---------|
| Claude Code | `/ssh-remote azure` |
| Codex CLI | `$ssh-remote azure` |
| Copilot | `ssh azure` |

### Enable Bash enforcement

| Platform | Command | Config file |
|----------|---------|-------------|
| Claude Code | `/ssh-remote-hook-on azure` | `.claude/claude-ssh-remote.local.md` |
| Codex CLI | `$ssh-remote-hook-on azure` | `.codex/ssh-remote.local.toml` |
| Copilot | edit config manually | `.claude/claude-ssh-remote.local.md` |

### Disable Bash enforcement

| Platform | Command |
|----------|---------|
| Claude Code | `/ssh-remote-hook-off` |
| Codex CLI | `$ssh-remote-hook-off` |
| Copilot | edit config manually |

## Hook mode

When enabled, the hook targets the `Bash` tool.

Behavior:

- safe non-interactive Bash commands are rewritten to run through `ssh <configured-host>`
- the original local Bash execution is blocked
- interactive or unsafe-to-proxy Bash commands are blocked and shown as a remote command suggestion instead of being auto-run
- existing `ssh` / `scp` / `sftp` commands are left alone

**Note:** Copilot has no hook mechanism. Enforcement is instruction-based — the
agent follows rules in `copilot-instructions.md` and `AGENTS.md`. This is less
guaranteed than programmatic hooks.

### Config file formats

Claude / Copilot (YAML frontmatter):

```markdown
---
enabled: true
ssh_host: azure
mode: rewrite_or_block
---
```

Codex (TOML):

```toml
enabled = true
ssh_host = "azure"
mode = "rewrite_or_block"
```

Supported modes:

- `rewrite_or_block`: try remote execution first, otherwise block
- `block_only`: never auto-run, only block and tell you the SSH form

## Install

See [INSTALL.md](INSTALL.md) for platform-specific install flows.

## Chinese guide

See [使用手册.md](使用手册.md) for Chinese instructions for all three platforms.

## Notes

- keep host, user, port, and identity settings in your SSH config
- this plugin intentionally keeps arguments minimal and does not add explicit `user@host` or `port` flags
- the command is designed for interactive remote development sessions, not one-off remote execution
- the hook currently targets the Bash tool, not every possible tool type
- Copilot enforcement is instruction-only — less strict than Claude/Codex hooks
