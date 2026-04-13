"""Shared SSH remote enforcement logic, platform-independent."""

import shlex
import subprocess
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from core.config import INTERACTIVE_HINTS, SSHRemoteConfig


class Action(Enum):
    ALLOW = "allow"
    REWRITE_AND_BLOCK = "rewrite_and_block"
    BLOCK_WITH_HINT = "block_with_hint"
    BLOCK_ONLY = "block_only"


@dataclass
class ClassifyResult:
    action: Action
    original_command: str
    rewritten_command: Optional[str] = None
    message: Optional[str] = None
    remote_output: Optional[str] = None


def is_already_remote(command: str) -> bool:
    prefixes = ("ssh ", "scp ", "sftp ")
    return command.startswith(prefixes)


def is_interactive_or_unsafe(command: str) -> bool:
    lowered = command.strip().lower()
    if lowered in ("top", "htop", "tmux", "screen"):
        return True
    if "&&" in command or "||" in command or "|" in command:
        return True
    for hint in INTERACTIVE_HINTS:
        if lowered.startswith(hint) or f" {hint}" in lowered:
            return True
    return False


def build_remote_command(host: str, original: str) -> str:
    return f"ssh {shlex.quote(host)} {shlex.quote(original)}"


def classify_command(config: SSHRemoteConfig, command: str) -> ClassifyResult:
    """Classify a Bash command and decide how to handle it under SSH enforcement.

    Returns a ClassifyResult indicating whether to allow, rewrite, or block.
    For REWRITE_AND_BLOCK, the caller must execute the rewritten command
    separately and populate ``remote_output`` on the result.
    """
    if not config.enabled or not config.ssh_host:
        return ClassifyResult(action=Action.ALLOW, original_command=command)

    if is_already_remote(command):
        return ClassifyResult(action=Action.ALLOW, original_command=command)

    rewritten = build_remote_command(config.ssh_host, command)

    if is_interactive_or_unsafe(command):
        return ClassifyResult(
            action=Action.BLOCK_WITH_HINT,
            original_command=command,
            rewritten_command=rewritten,
            message=(
                f"Blocked local Bash because this command is not safe to "
                f"transparently proxy through ssh host '{config.ssh_host}'.\n"
                f"Original: {command}\n"
                f"Run it manually in the remote session or use: {rewritten}"
            ),
        )

    if config.mode == "block_only":
        return ClassifyResult(
            action=Action.BLOCK_ONLY,
            original_command=command,
            rewritten_command=rewritten,
            message=(
                f"This session is locked to remote execution via ssh host "
                f"'{config.ssh_host}'.\n"
                f"Original: {command}\n"
                f"Run it remotely instead: {rewritten}"
            ),
        )

    # rewrite_or_block: try remote execution
    try:
        completed = subprocess.run(
            rewritten,
            shell=True,
            text=True,
            capture_output=True,
        )
    except Exception as exc:
        return ClassifyResult(
            action=Action.BLOCK_WITH_HINT,
            original_command=command,
            rewritten_command=rewritten,
            message=(
                f"Failed to execute the rewritten remote command through ssh "
                f"host '{config.ssh_host}': {exc}.\n"
                f"Original: {command}\n"
                f"Run it manually instead: {rewritten}"
            ),
        )

    output_chunks = []
    if completed.stdout:
        output_chunks.append(completed.stdout.rstrip())
    if completed.stderr:
        output_chunks.append(completed.stderr.rstrip())
    combined_output = "\n".join(chunk for chunk in output_chunks if chunk) or "(no output)"

    if completed.returncode != 0:
        return ClassifyResult(
            action=Action.BLOCK_WITH_HINT,
            original_command=command,
            rewritten_command=rewritten,
            message=(
                f"Blocked local Bash and tried the command remotely via ssh host "
                f"'{config.ssh_host}', but the remote command failed with exit code "
                f"{completed.returncode}.\n"
                f"Original: {command}\n"
                f"Remote: {rewritten}\n\n"
                f"Remote output:\n{combined_output}"
            ),
        )

    return ClassifyResult(
        action=Action.REWRITE_AND_BLOCK,
        original_command=command,
        rewritten_command=rewritten,
        remote_output=combined_output,
        message=(
            f"Blocked local Bash and executed it remotely via ssh host "
            f"'{config.ssh_host}'.\n"
            f"Original: {command}\n"
            f"Remote: {rewritten}\n\n"
            f"Remote output:\n{combined_output}"
        ),
    )
