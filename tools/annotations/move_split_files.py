"""Move augmented images and labels into train/validation splits.

Designed for the output of ``tools/augmentation/augment_dataset.py``. It takes
a flat staging folder with paired ``.jpg``/``.txt`` files and moves a random
fraction to the validation tree.

    python tools/annotations/move_split_files.py

Edit the configuration block before running. Back up the staging folder first:
the script moves files.
"""

from __future__ import annotations

import random
import shutil
from pathlib import Path

# --- Configuration ---------------------------------------------------------
STAGING_DIR = Path("dataset/images/train_augmented")
TRAIN_IMAGES_DIR = Path("dataset/images/train")
TRAIN_LABELS_DIR = Path("dataset/labels/train")
VALID_IMAGES_DIR = Path("dataset/images/valid")
VALID_LABELS_DIR = Path("dataset/labels/valid")
VALID_RATIO = 0.20
SEED = 42
# ---------------------------------------------------------------------------


def move_pair(image_path: Path, label_path: Path, images_dest: Path, labels_dest: Path) -> None:
    images_dest.mkdir(parents=True, exist_ok=True)
    labels_dest.mkdir(parents=True, exist_ok=True)
    shutil.move(str(image_path), str(images_dest / image_path.name))
    shutil.move(str(label_path), str(labels_dest / label_path.name))


def main() -> None:
    if not STAGING_DIR.is_dir():
        raise SystemExit(f"Staging directory not found: {STAGING_DIR}")

    images = sorted(STAGING_DIR.glob("*.jpg"))
    labels = {path.stem for path in STAGING_DIR.glob("*.txt")}
    paired = [image for image in images if image.stem in labels]

    if not paired:
        raise SystemExit("No .jpg/.txt pairs found in the staging directory.")

    random.seed(SEED)
    random.shuffle(paired)

    valid_count = max(1, int(len(paired) * VALID_RATIO))
    valid_samples = paired[:valid_count]
    train_samples = paired[valid_count:]

    for image_path in train_samples:
        move_pair(
            image_path,
            STAGING_DIR / f"{image_path.stem}.txt",
            TRAIN_IMAGES_DIR,
            TRAIN_LABELS_DIR,
        )

    for image_path in valid_samples:
        move_pair(
            image_path,
            STAGING_DIR / f"{image_path.stem}.txt",
            VALID_IMAGES_DIR,
            VALID_LABELS_DIR,
        )

    print(f"Seed: {SEED}")
    print(f"Moved {len(train_samples)} pairs to train and {len(valid_samples)} to valid.")


if __name__ == "__main__":
    main()
