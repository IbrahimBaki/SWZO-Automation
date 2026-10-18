#!/usr/bin/env python3
"""PreToolUse hook: when Claude Code is about to run a Bash command that
looks like `git commit`, run the local secret scan and change-package
validator first. Blocks the commit (exit 2) if either fails.

Any other Bash command passes straight through (exit 0). Never touches
ServiceNow, the network, or a browser — local file checks only.
"""
import json
import re
import subprocess
import sys
import pathlib

HOOKS_DIR = pathlib.Path(__file__).resolve().parent

COMMIT_RE = re.compile(r"(^|[;&|]\s*)git\s+commit\b")


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        return 0  # can't read input — don't block on a hook malfunction

    if payload.get("tool_name") != "Bash":
        return 0

    command = (payload.get("tool_input") or {}).get("command", "")
    if not COMMIT_RE.search(command):
        return 0

    failures = []
    for script in ("check_secrets.py", "validate_change_packages.py"):
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / script)],
            capture_output=True, text=True, check=False,
        )
        if result.returncode != 0:
            failures.append(result.stderr.strip() or result.stdout.strip())

    if failures:
        print("\n\n".join(failures), file=sys.stderr)
        return 2  # blocks the tool call in Claude Code

    return 0


if __name__ == "__main__":
    sys.exit(main())
