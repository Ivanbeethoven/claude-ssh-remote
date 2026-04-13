---
applyTo: "**/*.sh,**/*.py,**/*.toml,**/*.yaml,**/*.yml"
excludeAgent: "code-review"
---

When editing or running scripts in this project, check if SSH remote enforcement
is enabled (`.claude/claude-ssh-remote.local.md`). If enabled, all Bash commands
must be executed through `ssh <host> '<command>'` instead of locally.

Safe non-interactive commands should be rewritten to `ssh <host> '<cmd>'` and
executed. Interactive or unsafe commands (vim, top, tmux, pipes, chains) must be
blocked with a suggestion to run them in the remote SSH session instead.