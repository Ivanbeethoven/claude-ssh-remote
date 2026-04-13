#!/usr/bin/env python3
"""Codex CLI hook adapter for SSH remote enforcement.

Reads Codex's PreToolUse JSON payload from stdin, classifies the command
using the shared core, and outputs the hook JSON response.
"""

import json
import sys
from pathlib import Path

try:
    from core.config import load_config, parse_toml_config
    from core.ssh_enforce import Action, classify_command
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from core.config import load_config, parse_toml_config
    from core.ssh_enforce import Action, classify_command


CODEX_CONFIG_PATH = Path(".codex/ssh-remote.local.toml")


def deny(message: str):
    print(json.dumps({
        "hookSpecificOutput": {"permissionDecision": "deny"},
        "systemMessage": message,
    }))
    sys.exit(0)


def main():
    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(0)

    if payload.get("tool_name") != "Bash":
        sys.exit(0)

    tool_input = payload.get("tool_input", {})
    original_command = tool_input.get("command", "").strip()
    if not original_command:
        sys.exit(0)

    # Prefer Codex TOML config, then fall back to shared config
    config = parse_toml_config(CODEX_CONFIG_PATH)
    if not config.enabled or not config.ssh_host:
        config = load_config()
    if not config.enabled or not config.ssh_host:
        sys.exit(0)

    result = classify_command(config, original_command)

    if result.action == Action.ALLOW:
        sys.exit(0)

    deny(result.message)


if __name__ == "__main__":
    main()
