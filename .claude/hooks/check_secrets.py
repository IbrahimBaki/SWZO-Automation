#!/usr/bin/env python3
"""Scan files staged for commit (git diff --cached) for likely secrets:
passwords, API keys/tokens, session cookies, private keys. Heuristic,
local-only — not a replacement for a real secret scanner, just a cheap
backstop so a ServiceNow session cookie or token doesn't land in Git.

Exit 0 = clean. Exit 1 = suspicious content found (printed to stderr).
"""
import re
import subprocess
import sys

PATTERNS = [
    (r"(?i)password\s*[:=]\s*['\"]?[^\s'\"]{3,}", "possible password literal"),
    (r"(?i)api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{10,}", "possible API key"),
    (r"(?i)secret[_-]?(key|token)?\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{10,}", "possible secret/token"),
    (r"(?i)bearer\s+[A-Za-z0-9_\-\.]{10,}", "possible bearer token"),
    (r"(?i)\bJSESSIONID\s*=\s*[A-Za-z0-9!]{10,}", "possible ServiceNow session cookie"),
    (r"(?i)glide_user_session\s*=\s*[A-Za-z0-9]{10,}", "possible ServiceNow session value"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key material"),
    (r"(?i)x-usertoken\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{10,}", "possible ServiceNow user token header"),
]

ALLOWED_PLACEHOLDER = re.compile(r"<[^>]+>|xxx+|\bexample\b|\bTODO\b", re.IGNORECASE)

EXCLUDE_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".pdf")


def staged_files():
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True, check=False,
    )
    return [f for f in out.stdout.splitlines() if f and not f.endswith(EXCLUDE_SUFFIXES)]


def scan_file(path):
    findings = []
    try:
        with open(path, "r", errors="ignore") as fh:
            for lineno, line in enumerate(fh, start=1):
                for pattern, label in PATTERNS:
                    m = re.search(pattern, line)
                    if m and not ALLOWED_PLACEHOLDER.search(m.group(0)):
                        findings.append((lineno, label, m.group(0)[:80]))
    except (FileNotFoundError, IsADirectoryError):
        pass
    return findings


def main():
    files = staged_files()
    problems = []
    for f in files:
        for lineno, label, snippet in scan_file(f):
            problems.append(f"{f}:{lineno}: {label} -> {snippet!r}")

    if problems:
        print("Secret scan found possible credentials in staged files:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print(
            "If this is a false positive, rephrase/redact it; never commit real "
            "credentials, tokens, or session values (see CLAUDE.md §5.10).",
            file=sys.stderr,
        )
        return 1

    print("Secret scan passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
