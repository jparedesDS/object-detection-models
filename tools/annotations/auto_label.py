"""Generate YOLO pseudo-labels for unlabeled images with a trained checkpoint.

Edit the paths in the configuration block, then run:

    python tools/annotations/auto_label.py

Images where the model finds nothing above ``CONFIDENCE`` are moved to
``NO_LABELS_DIR`` and receive an empty label file so they can be reviewed and
annotated manually.

Review every generated label before training on it: pseudo-label errors are
amplified by the next model.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import cv2
from ultralytics import YOLO

# --- Configuration ---------------------------------------------------------
MODEL_PATH = Path("weights/cs2_yolov10s.pt")
IMAGES_DIR = Path("dataset/images/train")
LABELS_DIR = Path("dataset/labels/train")
NO_LABELS_DIR = Path("dataset/images/train_no_labels")
NO_LABELS_LABELS_DIR = Path("dataset/labels/train_no_labels")
CONFIDENCE = 0.52
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
# ---------------------------------------------------------------------------

model = YOLO(str(MODEL_PATH))


def detections_to_yolo(result, width: int, height: int) -> list[str]:
    """Convert Ultralytics boxes to normalized YOLO label lines."""
    lines: list[str] = []
    for box in result.boxes:
        confidence = float(box.conf[0])
        if confidence < CONFIDENCE:
            continue

        x1, y1, x2, y2 = box.xyxy[0].tolist()
        x_center = ((x1 + x2) / 2.0) / width
        y_center = ((y1 + y2) / 2.0) / height
        box_width = (x2 - x1) / width
        box_height = (y2 - y1) / height

        # Clamp to the image bounds.
        x_center = min(max(x_center, 0.0), 1.0)
        y_center = min(max(y_center, 0.0), 1.0)
        box_width = min(max(box_width, 0.0), 1.0)
        box_height = min(max(box_height, 0.0), 1.0)

        class_id = int(box.cls[0])
        lines.append(
            f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"
        )
    return lines


def main() -> None:
    for folder in (LABELS_DIR, NO_LABELS_DIR, NO_LABELS_LABELS_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    images = sorted(
        path for path in IMAGES_DIR.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS
    )
    if not images:
        raise SystemExit(f"No images found in {IMAGES_DIR}")

    labeled = 0
    moved = 0

    for image_path in images:
        image = cv2.imread(str(image_path))
        if image is None:
            print(f"! cannot read {image_path.name}, skipping")
            continue

        height, width = image.shape[:2]
        result = model(image, verbose=False)[0]
        lines = detections_to_yolo(result, width, height)

        if lines:
            (LABELS_DIR / f"{image_path.stem}.txt").write_text(
                "\n".join(lines) + "\n", encoding="utf-8"
            )
            labeled += 1
        else:
            shutil.move(str(image_path), str(NO_LABELS_DIR / image_path.name))
            (NO_LABELS_LABELS_DIR / f"{image_path.stem}.txt").write_text(
                "", encoding="utf-8"
            )
            moved += 1

    print(
        f"Done. {labeled} images labeled, {moved} moved to {NO_LABELS_DIR}. "
        f"Labels saved in {LABELS_DIR}."
    )


if __name__ == "__main__":
    main()
