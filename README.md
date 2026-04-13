# Claude SSH Remote

A standalone Claude Code plugin repo for opening a remote development shell over SSH.

## What it provides

- `/ssh-remote <host-alias>`
- optional remote working directory
- optional persistent session via `tmux`, with `screen` fallback
- host lookup via your existing `~/.ssh/config`

## Current layout

```text
claude-ssh-remote/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── ssh-remote/
│       └── SKILL.md
└── README.md
```

## Usage

### Host only

```text
/ssh-remote my-server
```

### Host + remote directory

```text
/ssh-remote my-server /srv/my-app
```

### Host + remote directory + session name

```text
/ssh-remote my-server /srv/my-app dev-session
```

## Behavior

- connects with `ssh <host-alias>`
- if `remote-dir` is given, enters that directory first
- if `session-name` is given, prefers `tmux`, then `screen`
- if neither `tmux` nor `screen` exists, falls back to a normal remote shell

## Notes

- host aliases should be maintained in your SSH config
- this plugin intentionally keeps arguments minimal and does not add explicit `user@host` or `port` flags
- the command is designed for interactive remote development sessions, not one-off remote execution

## Install / use locally

Open this repo in Claude Code or place it where your Claude plugin workflow loads local plugins.

If you only want the command file, the equivalent user command is the same content in:

```text
~/.claude/commands/ssh-remote.md
```
