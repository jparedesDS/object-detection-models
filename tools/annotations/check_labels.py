"""Audit a YOLO-format dataset split.

Counts instances per class and reports images that are missing a label file or
have an empty one (backgrounds). It does not modify anything.

    python tools/annotations/check_labels.py

Edit the two paths below before running.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

# --- Configuration ---------------------------------------------------------
IMAGES_DIR = Path("dataset/images/val")
LABELS_DIR = Path("dataset/labels/val")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
# ---------------------------------------------------------------------------


def main() -> None:
    if not IMAGES_DIR.is_dir():
        raise SystemExit(f"Images directory not found: {IMAGES_DIR}")
    if not LABELS_DIR.is_dir():
        raise SystemExit(f"Labels directory not found: {LABELS_DIR}")

    class_count: Counter[int] = Counter()
    backgrounds = 0
    missing_labels = 0
    malformed = 0
    total_images = 0

    for image_path in sorted(IMAGES_DIR.iterdir()):
        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        total_images += 1

        label_path = LABELS_DIR / f"{image_path.stem}.txt"
        if not label_path.exists():
            missing_labels += 1
            continue

        lines = [line for line in label_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            backgrounds += 1
            continue

        for line in lines:
            parts = line.split()
            if len(parts) != 5:
                malformed += 1
                continue
            try:
                class_count[int(parts[0])] += 1
            except ValueError:
                malformed += 1

    print(f"Images scanned:      {total_images}")
    print(f"Background images:   {backgrounds}")
    print(f"Missing label files: {missing_labels}")
    print(f"Malformed lines:     {malformed}")
    print("\nInstances per class:")
    if not class_count:
        print("  (none)")
    for class_id, count in sorted(class_count.items()):
        print(f"  class {class_id:>3}: {count}")


if __name__ == "__main__":
    main()
