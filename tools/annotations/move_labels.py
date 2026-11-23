"""Move YOLO label files from a staging folder into the canonical labels folder.

    python tools/annotations/move_labels.py

Existing files in the destination are never overwritten; collisions are skipped
and reported. Edit the configuration block before running.
"""

from __future__ import annotations

import shutil
from pathlib import Path

# --- Configuration ---------------------------------------------------------
SOURCE_DIR = Path("dataset/labels/staging")
DEST_DIR = Path("dataset/labels/valid")
# ---------------------------------------------------------------------------


def main() -> None:
    if not SOURCE_DIR.is_dir():
        raise SystemExit(f"Source directory not found: {SOURCE_DIR}")

    DEST_DIR.mkdir(parents=True, exist_ok=True)

    moved = 0
    skipped = 0

    for label_path in sorted(SOURCE_DIR.glob("*.txt")):
        destination = DEST_DIR / label_path.name
        if destination.exists():
            print(f"! {destination.name} already exists, skipping")
            skipped += 1
            continue

        shutil.move(str(label_path), str(destination))
        moved += 1

    print(f"Done. {moved} labels moved to {DEST_DIR}, {skipped} skipped.")


if __name__ == "__main__":
    main()
