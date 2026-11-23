"""Offline augmentation for YOLO-format datasets.

Creates contrast-scaled and flipped copies of every image in a folder and
rewrites the bounding boxes so they stay aligned with the transformed image.

Usage
-----
    python tools/augmentation/augment_dataset.py \
        --images dataset/images/train \
        --labels dataset/labels/train \
        --output dataset/images/train_augmented

The output folder receives paired ``.jpg`` images and ``.txt`` labels. Copy or
move them into your dataset split when you are happy with the result.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def read_labels(path: Path) -> list[list[float]]:
    """Read a YOLO label file, skipping malformed lines."""
    labels: list[list[float]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) != 5:
            if line.strip():
                print(f"  ! skipping malformed line in {path.name}: {line!r}")
            continue
        class_id, x, y, w, h = parts
        labels.append([float(class_id), float(x), float(y), float(w), float(h)])
    return labels


def write_labels(path: Path, labels: list[list[float]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for class_id, x, y, w, h in labels:
            handle.write(f"{int(class_id)} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")


def adjust_contrast(image: np.ndarray, alpha: float) -> np.ndarray:
    """Scale pixel values around zero (alpha < 1 softens, alpha > 1 hardens)."""
    return cv2.convertScaleAbs(image, alpha=alpha, beta=0)


def transform_labels(
    labels: list[list[float]], flip: str
) -> list[list[float]]:
    """Mirror boxes for horizontal or vertical flips and clamp to [0, 1]."""
    transformed = []
    for class_id, x, y, w, h in labels:
        if flip == "h":
            x = 1.0 - x
        elif flip == "v":
            y = 1.0 - y
        x = min(max(x, 0.0), 1.0)
        y = min(max(y, 0.0), 1.0)
        w = min(max(w, 0.0), 1.0)
        h = min(max(h, 0.0), 1.0)
        transformed.append([class_id, x, y, w, h])
    return transformed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images", required=True, type=Path, help="Folder with source images")
    parser.add_argument("--labels", required=True, type=Path, help="Folder with YOLO .txt labels")
    parser.add_argument("--output", required=True, type=Path, help="Destination folder")
    parser.add_argument(
        "--contrast",
        nargs="+",
        type=float,
        default=[0.5, 1.0, 1.7],
        help="Contrast factors to generate (default: 0.5 1.0 1.7)",
    )
    parser.add_argument(
        "--flip",
        choices=["h", "v", "hv", "none"],
        default="h",
        help="Flip variants: h, v, hv or none (default: h)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    flips = {"none": ["none"], "h": ["h"], "v": ["v"], "hv": ["h", "v"]}[args.flip]
    images = sorted(p for p in args.images.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)

    if not images:
        raise SystemExit(f"No images found in {args.images}")

    generated = 0
    skipped = 0

    for image_path in images:
        image = cv2.imread(str(image_path))
        if image is None:
            print(f"  ! cannot read {image_path.name}, skipping")
            skipped += 1
            continue

        label_path = args.labels / f"{image_path.stem}.txt"
        if not label_path.exists():
            print(f"  ! no label for {image_path.name}, skipping")
            skipped += 1
            continue

        labels = read_labels(label_path)

        for alpha in args.contrast:
            adjusted = image if alpha == 1.0 else adjust_contrast(image, alpha)

            for flip in flips:
                if alpha == 1.0 and flip == "none":
                    continue  # Do not duplicate the original image.

                output_image = adjusted
                if flip == "h":
                    output_image = cv2.flip(adjusted, 1)
                elif flip == "v":
                    output_image = cv2.flip(adjusted, 0)

                suffix = f"_c{alpha:g}_flip{flip}" if flip != "none" else f"_c{alpha:g}"
                stem = f"{image_path.stem}{suffix}"

                cv2.imwrite(
                    str(args.output / f"{stem}.jpg"),
                    output_image,
                    [cv2.IMWRITE_JPEG_QUALITY, 95],
                )
                write_labels(args.output / f"{stem}.txt", transform_labels(labels, flip))
                generated += 1

    print(f"Done. Generated {generated} image/label pairs in {args.output} ({skipped} skipped).")


if __name__ == "__main__":
    main()
