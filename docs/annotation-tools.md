# Annotation & Dataset Tools

The scripts in [`tools/`](../tools/) were written to build the datasets behind the published models. They are intentionally small and pragmatic: each file declares its paths at the top, processes a folder, and prints a summary. **Back up your dataset before running any script that writes or moves files.**

[← Back to the main README](../README.md) · [Training guide](training-guide.md)

---

## Recommended workflow

```text
raw screenshots / frames
        │
        ▼
 auto_label.py  ──►  pseudo-labels for easy images
        │
        ▼
 manual review in Label Studio / labelImg
        │
        ▼
 check_labels.py  ──►  class balance & background count
        │
        ▼
 remap_labels.py  ──►  fix class IDs before training
        │
        ▼
 augment_dataset.py  ──►  offline augmentation (optional)
        │
        ▼
 split_train_val.py / move_split_files.py  ──►  train / val
        │
        ▼
 yolo detect train ...
```

---

## `tools/annotations/`

### `auto_label.py`

Runs a trained YOLO checkpoint over an unlabeled image folder and writes YOLO-format pseudo-labels.

- **Input:** `directorio_imagenes` (images) and `model` (checkpoint path).
- **Output:** `.txt` labels in `directorio_salida`; images with no detections are moved to `images_SINLABELS` and get an empty label file.
- **Confidence threshold:** `0.52` by default (edit the `if conf > 0.52` line).
- **Use it for:** bootstrapping a dataset, then **review every pseudo-label manually**. Errors propagate into the next model.

### `check_labels.py`

Audits a dataset split.

- Counts instances per class ID.
- Counts images without a label file or with an empty label file (backgrounds).
- Does not modify anything.
- **Use it for:** catching missing pairs, class imbalance and accidental background-heavy splits before training.

### `remap_labels.py`

Remaps class IDs across every `.txt` file in a directory, in place.

- Edit `label_map` to define the mapping, for example `{0: 0, 1: 1, 2: 0, 3: 1}` merges classes 2 and 3 into 0 and 1.
- Classes not present in the map are **dropped** from the label files.
- **Use it for:** merging duplicate classes (for example `CT`/`CT_body`) or reordering IDs to match `data.yaml`.
- **Warning:** the script overwrites files. Copy the labels folder first.

### `split_train_val.py`

Moves a random percentage of a flat image/label dataset into `valid/images` and `valid/labels`.

- **Default ratio:** `valid_ratio = 0.20`.
- Pairs images with labels by filename and skips unpaired images.
- **Use it for:** creating a validation split from a single annotated folder.
- **Warning:** it uses `shutil.move`, not copy.

### `move_split_files.py`

Distributes augmented images and their labels from a staging folder into train/validation directories.

- **Default ratio:** `valid_split = 0.2`.
- **Use it for:** placing the output of `augment_dataset.py` into the final dataset structure.

### `move_labels.py`

Moves every `.txt` file from a staging folder into the canonical `labels/` directory.

- **Use it for:** consolidating labels after augmentation or manual review.
- **Warning:** it moves files and does not check for collisions.

---

## `tools/augmentation/`

### `augment_dataset.py`

Offline augmentation with OpenCV.

- Applies contrast scaling (`0.5`, `1.0`, `1.7`) and horizontal flipping.
- Rewrites bounding boxes for the flip (`x → 1 − x`).
- Writes paired image/label files with descriptive suffixes.
- **Use it for:** small datasets where online augmentation is not enough.
- **Do not use it** as a substitute for collecting diverse data; offline flips and contrast changes do not add new scenes.

The original notebook also experimented with rotation, brightness, scaling and Gaussian blur. Those transformations are easy to add to this script, but remember to transform the bounding boxes consistently.

---

## `examples/`

### `screen_inference.py`

Captures a screen region with `pyautogui`, runs a YOLO checkpoint and draws the detections with OpenCV.

```bash
python examples/screen_inference.py --model weights/ow2-yolo11m.pt --conf 0.4
```

- `--region WxH+X+Y` selects the capture area (default `640x640` centered on a 1920×1080 screen).
- Press `q` to quit.
- **Use it for:** quick qualitative checks of a detector on live gameplay or any application window.

---

## Conventions used by these scripts

- Label format: YOLO (`class x_center y_center width height`, normalized).
- Image/label pairing: same stem, `.txt` extension.
- Class IDs: zero-based, matching `data.yaml`.
- Paths: edit the constants at the top of each script. They are deliberately not CLI-complete — these are dataset-building utilities, not a library.

[← Back to the main README](../README.md)
