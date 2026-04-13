# Install from GitHub

Repository:

- `https://github.com/Ivanbeethoven/claude-ssh-remote`

## Claude Code

### Fastest install

```bash
git clone https://github.com/Ivanbeethoven/claude-ssh-remote.git
cd claude-ssh-remote
cc --plugin-dir .
```

### After Claude starts

Connect to the remote host:

```text
/ssh-remote azure
```

Enable Bash enforcement:

```text
/ssh-remote-hook-on azure
```

Disable Bash enforcement:

```text
/ssh-remote-hook-off
```

### What the commands expect

The `ssh-host` argument is only your SSH config host alias.

Example SSH config:

```sshconfig
Host azure
  HostName 20.1.2.3
  User hxy
  Port 22
  IdentityFile ~/.ssh/id_rsa
```

### Hook mode setup

When you run `/ssh-remote-hook-on azure`, Claude writes:

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

---

## OpenAI Codex CLI

### Install skills

Copy the skill directories into your Codex skills path, or add them to
`~/.codex/config.toml`:

```toml
[[skills.config]]
path = "/path/to/claude-ssh-remote/codex/skills/ssh-remote/SKILL.md"
enabled = true

[[skills.config]]
path = "/path/to/claude-ssh-remote/codex/skills/ssh-remote-hook-on/SKILL.md"
enabled = true

[[skills.config]]
path = "/path/to/claude-ssh-remote/codex/skills/ssh-remote-hook-off/SKILL.md"
enabled = true
```

See `codex/config-snippet.toml` for a complete example.

### Enable hooks

Hooks must be enabled in your Codex config:

```toml
[features]
codex_hooks = true
```

Then copy or link `codex/hooks.json` into your Codex hooks directory.

### After Codex starts

Connect to the remote host:

```text
$ssh-remote azure
```

Enable Bash enforcement:

```text
$ssh-remote-hook-on azure
```

This writes `.codex/ssh-remote.local.toml`:

```toml
enabled = true
ssh_host = "azure"
mode = "rewrite_or_block"
```

Disable Bash enforcement:

```text
$ssh-remote-hook-off
```

### AGENTS.md

The `codex/AGENTS.md` file provides agent-level instructions for SSH remote
development. Copy it to your project root if you want Codex to always follow
SSH remote rules.

---

## GitHub Copilot Coding Agent

### Install instructions

Copy the instruction files into your project:

```bash
# Repository-wide instructions
cp github/copilot-instructions.md .github/copilot-instructions.md

# Path-specific instructions (reinforces rules for script files)
cp -r github/instructions/ .github/instructions/

# Shared agent instructions
cp AGENTS.md AGENTS.md
```

### How it works

Copilot has no hook mechanism. Enforcement relies on instruction files:

- `.github/copilot-instructions.md` — primary rules (MUST/NEVER language)
- `.github/instructions/ssh-remote.instructions.md` — reinforces for script files
- `AGENTS.md` — shared agent instructions

The agent reads these instructions and follows them when executing Bash
commands. This is inherently less strict than programmatic hooks.

### Configuration

Copilot reads the same config file as Claude:

```text
.claude/claude-ssh-remote.local.md
```

Create it manually:

```markdown
---
enabled: true
ssh_host: azure
mode: rewrite_or_block
---
```

To disable, set `enabled: false` or delete the file.

---

## All platforms — SSH config

Regardless of platform, make sure this works first:

```bash
ssh azure
```

Example `~/.ssh/config`:

```sshconfig
Host azure
  HostName 20.1.2.3
  User hxy
  Port 22
  IdentityFile ~/.ssh/id_rsa
```

## Important notes

- first make sure `ssh azure` already works in your terminal
- the plugin expects the first argument to be an SSH config host alias
- it is optimized for the simple case `ssh azure`
- keep host, user, port, and identity settings in `~/.ssh/config`
- do not pass `user@host` unless you intentionally change the skill later
- the hook currently enforces the Bash tool only; it does not rewrite every possible tool
- Copilot enforcement is instruction-based and cannot guarantee compliance

## Files in this repo

```text
claude-ssh-remote/
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── ssh_enforce.py
├── .claude-plugin/
│   └── plugin.json
├── hooks/
│   ├── hooks.json
│   ├── claude_hook_adapter.py
│   └── ssh_enforce_hook.py
├── skills/
│   ├── ssh-remote/SKILL.md
│   ├── ssh-remote-hook-on/SKILL.md
│   └── ssh-remote-hook-off/SKILL.md
├── codex/
│   ├── AGENTS.md
│   ├── skills/
│   │   ├── ssh-remote/SKILL.md
│   │   ├── ssh-remote-hook-on/SKILL.md
│   │   └── ssh-remote-hook-off/SKILL.md
│   ├── codex_hook_adapter.py
│   ├── hooks.json
│   └── config-snippet.toml
├── github/
│   ├── copilot-instructions.md
│   └── instructions/
│       └── ssh-remote.instructions.md
├── AGENTS.md
├── INSTALL.md
├── README.md
└── 使用手册.md
```
