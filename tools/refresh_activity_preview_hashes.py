#!/usr/bin/env python3
"""Refresh visual-review preview hashes for all Activity Diagram view YAML files."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIEW_DIR = ROOT / "views" / "activity"
PREVIEW_DIR = ROOT / "build" / "preview"
HASH_LINE = re.compile(r"^(\s*previewHash:\s*)'?[0-9a-f]{64}'?\s*$", re.MULTILINE)


def main() -> None:
    updated = 0
    for view_path in sorted(VIEW_DIR.glob("aafiatak-ad*.yaml")):
        preview = PREVIEW_DIR / f"{view_path.stem}.png"
        if not preview.exists():
            raise FileNotFoundError(preview)
        digest = hashlib.sha256(preview.read_bytes()).hexdigest()
        content = view_path.read_text(encoding="utf-8")
        replacement = lambda match: f"{match.group(1)}'{digest}'"
        refreshed, count = HASH_LINE.subn(replacement, content, count=1)
        if count != 1:
            raise ValueError(f"Expected one previewHash in {view_path}")
        view_path.write_text(refreshed, encoding="utf-8")
        updated += 1
    print(f"Refreshed {updated} Activity Diagram preview hashes.")


if __name__ == "__main__":
    main()
