#!/usr/bin/env python3
"""Cheap deterministic repository checks for Nastya Story.

The script intentionally avoids semantic validation. It catches structural mistakes that
should not consume AI/Codex context: missing entry points, duplicate TASK ids, and TASK
lifecycle/frontmatter mismatches.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = ROOT / "docs" / "tasks"
LIFECYCLE = ("backlog", "ready", "in_progress", "review", "done")

REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "docs/MASTER_SPEC.md",
    "docs/REPOSITORY_MAP.md",
    "docs/IMPLEMENTATION_ROADMAP.md",
    "docs/DEVELOPMENT_BOARD.md",
    "docs/DEVELOPMENT_WORKFLOW.md",
    "docs/tasks/README.md",
    "docs/templates/TASK_TEMPLATE.md",
    "docs/templates/CONTEXT_MANIFEST_TEMPLATE.md",
)


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}

    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$", line)
        if match:
            result[match.group(1)] = match.group(2).strip('"\'')
    return result


def check_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"Missing required file: {relative}")


def check_task_lifecycle(errors: list[str], warnings: list[str]) -> None:
    seen: dict[str, Path] = {}

    for status in LIFECYCLE:
        folder = TASKS_ROOT / status
        if not folder.is_dir():
            errors.append(f"Missing TASK lifecycle directory: docs/tasks/{status}")
            continue

        for path in sorted(folder.glob("TASK-*.md")):
            if path.name.endswith("_IMPLEMENTATION_REPORT.md"):
                continue

            meta = read_frontmatter(path)
            task_id = meta.get("id")
            declared_status = meta.get("status")
            relative = path.relative_to(ROOT)

            if not task_id:
                errors.append(f"{relative}: missing frontmatter id")
                continue

            if task_id in seen:
                errors.append(
                    f"Duplicate active TASK id {task_id}: "
                    f"{seen[task_id].relative_to(ROOT)} and {relative}"
                )
            else:
                seen[task_id] = path

            if not declared_status:
                warnings.append(f"{relative}: no frontmatter status")
            elif declared_status != status:
                errors.append(
                    f"{relative}: frontmatter status '{declared_status}' "
                    f"does not match directory '{status}'"
                )


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    check_required_files(errors)
    check_task_lifecycle(errors, warnings)
    try:
        from sync_items import OUTPUT as ITEMS_OUTPUT, render as render_items
        if ITEMS_OUTPUT.read_text(encoding="utf-8") != render_items():
            errors.append("Item runtime data is stale: run tools/sync_items.py")
    except (KeyError, IndexError, OSError, ValueError) as exc:
        errors.append(f"Item card validation failed: {exc}")
    try:
        from sync_world_map import OUTPUT, VISUAL_TESTS, render, render_visual_tests
        if OUTPUT.read_text(encoding="utf-8") != render() or VISUAL_TESTS.read_text(encoding="utf-8") != render_visual_tests():
            errors.append("World map runtime data is stale: run tools/sync_world_map.py")
    except (KeyError, AssertionError, OSError, ValueError) as exc:
        errors.append(f"World map/card validation failed: {exc}")

    print("Nastya Story project health check")
    print(f"Repository: {ROOT}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"\nOK: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
