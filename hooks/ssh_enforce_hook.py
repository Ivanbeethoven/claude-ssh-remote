#!/usr/bin/env python3
"""DEPRECATED: Use claude_hook_adapter.py instead.

This file is kept for backward compatibility with existing hook registrations.
It delegates entirely to the new adapter which uses the shared core modules.
"""

from hooks.claude_hook_adapter import main

if __name__ == "__main__":
    main()
