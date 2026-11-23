"""Create a reproducible train/validation split from a flat YOLO dataset.

The source dataset is expected to look like:

    dataset/
    ├── images/   *.jpg
    └── labels/   *.txt

The script **copies** (does not move) the selected pairs into
``images/valid`` and ``labels/valid``, leaving the training data untouched.

    python tools/annotations/split_train_val.py

Edit the configuration block before running.
"""

from __future__ import annotations

import random
import shutil
from pathlib import Path

# --- Configuration ---------------------------------------------------------
BASE_DIR = Path("dataset")
VALID_RATIO = 0.20
SEED = 42
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
# ---------------------------------------------------------------------------


def main() -> None:
    images_dir = BASE_DIR / "images"
    labels_dir = BASE_DIR / "labels"
    valid_images_dir = images_dir / "valid"
    valid_labels_dir = labels_dir / "valid"

    if not images_dir.is_dir() or not labels_dir.is_dir():
        raise SystemExit(f"Expected {images_dir} and {labels_dir} to exist.")

    valid_images_dir.mkdir(parents=True, exist_ok=True)
    valid_labels_dir.mkdir(parents=True, exist_ok=True)

    images = sorted(
        path for path in images_dir.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS
    )
    labels = {path.stem for path in labels_dir.glob("*.txt")}

    paired = [image for image in images if image.stem in labels]
    unpaired = len(images) - len(paired)

    if not paired:
        raise SystemExit("No image/label pairs found. Check the folder structure.")

    random.seed(SEED)
    random.shuffle(paired)

    valid_count = max(1, int(len(paired) * VALID_RATIO))
    valid_samples = paired[:valid_count]

    for image_path in valid_samples:
        label_path = labels_dir / f"{image_path.stem}.txt"
        shutil.copy2(image_path, valid_images_dir / image_path.name)
        shutil.copy2(label_path, valid_labels_dir / label_path.name)

    print(f"Seed: {SEED}")
    print(f"Copied {valid_count} pairs to {valid_images_dir} and {valid_labels_dir}.")
    print(f"Training pairs remaining: {len(paired) - valid_count}.")
    if unpaired:
        print(f"Warning: {unpaired} images have no matching label and were ignored.")


if __name__ == "__main__":
    main()
