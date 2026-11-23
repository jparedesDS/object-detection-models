"""Remap or merge class IDs across every YOLO label file in a directory.

Edit ``LABELS_DIR`` and ``LABEL_MAP`` below, then run:

    python tools/annotations/remap_labels.py

``LABEL_MAP`` maps original IDs to new IDs. Classes that are not present in the
map are removed from the label files. The script overwrites files in place, so
make a copy of the labels folder first.
"""

from __future__ import annotations

from pathlib import Path

# --- Configuration ---------------------------------------------------------
LABELS_DIR = Path("dataset/labels/train")
# Example: merge classes 2 and 3 into 0 and 1, drop the rest.
LABEL_MAP = {0: 0, 1: 1, 2: 0, 3: 1}
# ---------------------------------------------------------------------------


def main() -> None:
    if not LABELS_DIR.is_dir():
        raise SystemExit(f"Labels directory not found: {LABELS_DIR}")

    files_changed = 0
    boxes_kept = 0
    boxes_dropped = 0

    for label_path in sorted(LABELS_DIR.glob("*.txt")):
        new_lines: list[str] = []

        for line in label_path.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) != 5:
                continue

            try:
                original_id = int(parts[0])
            except ValueError:
                continue

            if original_id not in LABEL_MAP:
                boxes_dropped += 1
                continue

            new_lines.append(f"{LABEL_MAP[original_id]} " + " ".join(parts[1:]))
            boxes_kept += 1

        label_path.write_text(
            "\n".join(new_lines) + ("\n" if new_lines else ""), encoding="utf-8"
        )
        files_changed += 1

    print(
        f"Done. {files_changed} files updated, {boxes_kept} boxes kept, "
        f"{boxes_dropped} boxes dropped."
    )


if __name__ == "__main__":
    main()
