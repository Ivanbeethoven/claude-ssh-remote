"""Shared config parsing and constants for SSH remote enforcement."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

SETTINGS_FILE_DEFAULT = ".claude/claude-ssh-remote.local.md"
CODEX_SETTINGS_FILE = ".codex/ssh-remote.local.toml"

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


@dataclass
class SSHRemoteConfig:
    enabled: bool = False
    ssh_host: str = ""
    mode: str = "rewrite_or_block"


def parse_frontmatter(path: Path) -> SSHRemoteConfig:
    """Parse YAML frontmatter from a Markdown file into SSHRemoteConfig."""
    if not path.exists():
        return SSHRemoteConfig()
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return SSHRemoteConfig()
    parts = text.split("---", 2)
    if len(parts) < 3:
        return SSHRemoteConfig()
    frontmatter = parts[1]
    raw: dict[str, str] = {}
    for raw_line in frontmatter.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")
        raw[key.strip()] = value
    return SSHRemoteConfig(
        enabled=raw.get("enabled", "false").lower() == "true",
        ssh_host=raw.get("ssh_host", "").strip(),
        mode=raw.get("mode", "rewrite_or_block").strip() or "rewrite_or_block",
    )


def parse_toml_config(path: Path) -> SSHRemoteConfig:
    """Parse a minimal TOML config file into SSHRemoteConfig.

    Expected format::

        enabled = true
        ssh_host = "azure"
        mode = "rewrite_or_block"
    """
    if not path.exists():
        return SSHRemoteConfig()
    raw: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("["):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        raw[key.strip()] = value
    return SSHRemoteConfig(
        enabled=raw.get("enabled", "false").lower() == "true",
        ssh_host=raw.get("ssh_host", "").strip(),
        mode=raw.get("mode", "rewrite_or_block").strip() or "rewrite_or_block",
    )


def load_config(preferred_path: Optional[Path] = None) -> SSHRemoteConfig:
    """Load config from the preferred path, falling back to defaults.

    Tries the preferred path first (if given), then the Claude frontmatter
    file, then the Codex TOML file. Returns the first valid enabled config,
    or a default disabled config.
    """
    candidates: list[Path] = []
    if preferred_path is not None:
        candidates.append(preferred_path)
    candidates.append(Path(SETTINGS_FILE_DEFAULT))
    candidates.append(Path(CODEX_SETTINGS_FILE))

    for p in candidates:
        if p.suffix == ".toml":
            cfg = parse_toml_config(p)
        else:
            cfg = parse_frontmatter(p)
        if cfg.enabled and cfg.ssh_host:
            return cfg
    return SSHRemoteConfig()
