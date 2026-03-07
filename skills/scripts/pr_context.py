#!/usr/bin/env -S uv run
"""
Extract git context for PR writing.

Usage:
    python pr_context.py                    # Full context
    python pr_context.py --diff             # Just the diff
    python pr_context.py --commits          # Recent commits
    python pr_context.py --files            # Changed files summary
    python pr_context.py --base main        # Compare against specific branch
"""

import subprocess
import sys
import json
from pathlib import Path


def run_git(args: list[str]) -> str:
    """Run a git command and return output."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=Path.cwd()
    )
    return result.stdout.strip()


def get_current_branch() -> str:
    """Get the current branch name."""
    return run_git(["branch", "--show-current"])


def get_base_branch(default: str = "main") -> str:
    """Try to detect the base branch (main or master)."""
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            capture_output=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            return branch
    return default


def get_commits(base: str, limit: int = 10) -> list[dict]:
    """Get commits since base branch."""
    format_str = "%H%n%s%n%b%n---COMMIT---"
    output = run_git([
        "log", f"{base}..HEAD",
        f"--format={format_str}",
        f"-{limit}"
    ])

    commits = []
    for block in output.split("---COMMIT---"):
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n", 2)
        if len(lines) >= 2:
            commits.append({
                "hash": lines[0][:7],
                "subject": lines[1],
                "body": lines[2] if len(lines) > 2 else ""
            })
    return commits


def get_changed_files(base: str) -> dict:
    """Get summary of changed files."""
    output = run_git(["diff", "--stat", f"{base}...HEAD"])

    files = []
    total_additions = 0
    total_deletions = 0

    for line in output.split("\n"):
        if not line.strip():
            continue
        # Parse lines like: "src/file.py | 10 +++++-----"
        if "|" in line:
            parts = line.split("|")
            filename = parts[0].strip()
            if len(parts) > 1:
                stats = parts[1].strip()
                # Count + and - characters
                additions = stats.count("+")
                deletions = stats.count("-")
                total_additions += additions
                total_deletions += deletions
                files.append({
                    "file": filename,
                    "additions": additions,
                    "deletions": deletions
                })

    return {
        "files": files,
        "total_additions": total_additions,
        "total_deletions": total_deletions,
        "file_count": len(files)
    }


def get_diff(base: str, context_lines: int = 3) -> str:
    """Get the actual diff."""
    return run_git(["diff", f"-U{context_lines}", f"{base}...HEAD"])


def main():
    base = "main"

    # Parse arguments
    args = sys.argv[1:]
    show_diff = "--diff" in args
    show_commits = "--commits" in args
    show_files = "--files" in args

    if "--base" in args:
        idx = args.index("--base")
        if idx + 1 < len(args):
            base = args[idx + 1]

    # If no specific flag, show everything
    show_all = not (show_diff or show_commits or show_files)

    base = get_base_branch(base)
    current = get_current_branch()

    output = {}

    if show_all or show_files:
        output["branch"] = current
        output["base"] = base
        output["changed_files"] = get_changed_files(base)

    if show_all or show_commits:
        output["commits"] = get_commits(base)

    if show_diff:
        output["diff"] = get_diff(base)

    # Output as JSON for easy parsing
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
