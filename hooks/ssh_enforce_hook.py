#!/usr/bin/env python3
import json
import shlex
import subprocess
import sys
from pathlib import Path

SETTINGS_FILE = ".claude/claude-ssh-remote.local.md"
INTERACTIVE_HINTS = [
    "vim ",
    "vi ",
    "nano ",
    "top",
    "htop",
    "less ",
    "more ",
    "man ",
    "watch ",
    "tmux",
    "screen",
    "ssh ",
    "sftp ",
    "scp ",
    "tail -f",
    "tailf",
]


def parse_frontmatter(path: Path):
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    frontmatter = parts[1]
    result = {}
    for raw_line in frontmatter.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")
        result[key.strip()] = value
    return result


def build_remote_command(host: str, original: str) -> str:
    return f"ssh {shlex.quote(host)} {shlex.quote(original)}"


def deny(message: str):
    print(
        json.dumps(
            {
                "hookSpecificOutput": {"permissionDecision": "deny"},
                "systemMessage": message,
            }
        )
    )
    sys.exit(0)


def is_already_remote(command: str) -> bool:
    prefixes = ("ssh ", "scp ", "sftp ")
    return command.startswith(prefixes)


def is_interactive_or_unsafe(command: str) -> bool:
    lowered = command.strip().lower()
    if lowered == "top" or lowered == "htop" or lowered == "tmux" or lowered == "screen":
        return True
    if "&&" in command or "||" in command or "|" in command:
        return True
    for hint in INTERACTIVE_HINTS:
        if lowered.startswith(hint) or f" {hint}" in lowered:
            return True
    return False


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

    settings = parse_frontmatter(Path(SETTINGS_FILE))
    enabled = settings.get("enabled", "false").lower() == "true"
    target_host = settings.get("ssh_host", "").strip()
    mode = settings.get("mode", "rewrite_or_block").strip() or "rewrite_or_block"

    if not enabled or not target_host:
        sys.exit(0)

    if is_already_remote(original_command):
        sys.exit(0)

    rewritten = build_remote_command(target_host, original_command)

    if is_interactive_or_unsafe(original_command):
        deny(
            f"Blocked local Bash because this command is not safe to transparently proxy through ssh host '{target_host}'.\n"
            f"Original: {original_command}\n"
            f"Run it manually in the remote session or use: {rewritten}"
        )

    if mode == "block_only":
        deny(
            f"This session is locked to remote execution via ssh host '{target_host}'.\n"
            f"Original: {original_command}\n"
            f"Run it remotely instead: {rewritten}"
        )

    try:
        completed = subprocess.run(
            rewritten,
            shell=True,
            text=True,
            capture_output=True,
        )
    except Exception as exc:
        deny(
            f"Failed to execute the rewritten remote command through ssh host '{target_host}': {exc}.\n"
            f"Original: {original_command}\n"
            f"Run it manually instead: {rewritten}"
        )

    output_chunks = []
    if completed.stdout:
        output_chunks.append(completed.stdout.rstrip())
    if completed.stderr:
        output_chunks.append(completed.stderr.rstrip())
    combined_output = "\n".join(chunk for chunk in output_chunks if chunk) or "(no output)"

    if completed.returncode != 0:
        deny(
            f"Blocked local Bash and tried the command remotely via ssh host '{target_host}', but the remote command failed with exit code {completed.returncode}.\n"
            f"Original: {original_command}\n"
            f"Remote: {rewritten}\n\n"
            f"Remote output:\n{combined_output}"
        )

    deny(
        f"Blocked local Bash and executed it remotely via ssh host '{target_host}'.\n"
        f"Original: {original_command}\n"
        f"Remote: {rewritten}\n\n"
        f"Remote output:\n{combined_output}"
    )


if __name__ == "__main__":
    main()
