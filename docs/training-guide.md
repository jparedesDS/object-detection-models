# Training Guide

Reference workflow for training a custom YOLO detector with this repository's tooling. It summarizes the pipeline used for the published models; the original Spanish-language walkthrough is in [`notebooks/yolo-training-guide.ipynb`](../notebooks/yolo-training-guide.ipynb).

[← Back to the main README](../README.md)

---

## 1. Environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -U ultralytics opencv-python numpy huggingface_hub
```

A CUDA-capable GPU is strongly recommended. Verify it with:

```python
import torch
print(torch.cuda.is_available(), torch.cuda.get_device_name(0))
```

---

## 2. Dataset layout

Ultralytics expects images and labels in parallel directories:

```text
dataset/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── data.yaml
```

Each image has a sibling `.txt` file with one detection per line:

```text
<class_id> <x_center> <y_center> <width> <height>
```

All coordinates are normalized to `[0, 1]`. An empty `.txt` file is a valid background image. Class IDs are zero-based and must match the order in `data.yaml`.

### `data.yaml`

```yaml
path: ./dataset
train: images/train
val: images/val
nc: 4
names:
  0: Defect
  1: Welding Line
  2: Workpiece
  3: porosity
```

For a quick sanity check, `nc` must equal `len(names)`.

---

## 3. Build and audit the dataset

| Step | Tool |
|---|---|
| Label images manually | [Label Studio](https://labelstud.io/) or [labelImg](https://github.com/HumanSignal/labelImg) |
| Generate pseudo-labels with an existing model | [`tools/annotations/auto_label.py`](../tools/annotations/auto_label.py) |
| Count instances per class and backgrounds | [`tools/annotations/check_labels.py`](../tools/annotations/check_labels.py) |
| Merge or remap class IDs | [`tools/annotations/remap_labels.py`](../tools/annotations/remap_labels.py) |
| Split into train/val | [`tools/annotations/split_train_val.py`](../tools/annotations/split_train_val.py) |
| Offline augmentation | [`tools/augmentation/augment_dataset.py`](../tools/augmentation/augment_dataset.py) |

Recommended ratio: **80 % train / 20 % validation**, stratified by scene whenever possible. Keep a separate test set if you need an unbiased final number.

Before training, always run the audit:

```bash
python tools/annotations/check_labels.py
```

A healthy dataset has no missing labels, no malformed lines, and enough instances per class. Classes with fewer than ~50 instances are likely to underperform.

---

## 4. Train

```bash
yolo detect train \
  model=yolo11m.pt \
  data=dataset/data.yaml \
  epochs=150 \
  imgsz=640 \
  batch=16 \
  patience=30 \
  project=runs \
  name=my-detector
```

Useful options:

| Option | Effect |
|---|---|
| `model=yolo11n.pt` … `yolo11x.pt` | Model size / accuracy trade-off. |
| `imgsz=640` | Training resolution. Must match inference resolution. |
| `batch=-1` | Automatic batch size (Ultralytics chooses based on VRAM). |
| `cache=ram` | Faster epochs if the dataset fits in memory. |
| `cos_lr=True` | Cosine learning-rate schedule. |
| `close_mosaic=10` | Disables mosaic for the last 10 epochs. |
| `resume=True` | Resume an interrupted run from `last.pt`. |

Training outputs:

```text
runs/detect/my-detector/
├── weights/best.pt
├── weights/last.pt
├── results.csv
├── results.png
├── confusion_matrix.png
├── confusion_matrix_normalized.png
├── F1_curve.png
├── PR_curve.png
└── args.yaml
```

`args.yaml` is important: it records the exact configuration used for the run.

---

## 5. Validate

```bash
yolo detect val model=runs/detect/my-detector/weights/best.pt data=dataset/data.yaml
```

This reports precision, recall, mAP@50 and mAP@50-95, and regenerates the confusion matrix and curves. Evaluate at the same `imgsz` used during training.

For a per-class breakdown:

```python
from ultralytics import YOLO

model = YOLO("runs/detect/my-detector/weights/best.pt")
metrics = model.val(data="dataset/data.yaml", imgsz=640)
print(metrics.box.map50, metrics.box.map)
print(metrics.box.ap_class_index)
```

---

## 6. Predict and export

```bash
yolo detect predict model=best.pt source=image.jpg conf=0.25 save=True
yolo export model=best.pt format=onnx imgsz=640
```

Typical export targets:

| Format | Use case |
|---|---|
| `onnx` | Cross-platform inference, ONNX Runtime |
| `engine` | NVIDIA TensorRT, lowest latency |
| `openvino` | Intel CPU / iGPU deployment |
| `coreml` | Apple devices |

---

## 7. Publish the model

1. Copy `best.pt` with a descriptive filename (for example `welding_defects_yolo11x.pt`).
2. Upload the weights to a Hugging Face model repository with `pipeline_tag: object-detection`.
3. Include `results.csv`, `results.png`, the confusion matrix and the curves.
4. Add the class list and the exact validation command to the model card.
5. Add the new checkpoint to [`docs/model-zoo.md`](model-zoo.md) and to the project README.

---

## Practical notes

- **Resolution matters.** A model trained at 640 px and evaluated at 1280 px will not reproduce its reported metrics.
- **Do not mix label conventions.** Fix class IDs before training, not after.
- **Augment offline only when needed.** Ultralytics already applies mosaic, HSV, flips and scale augmentation online. Offline augmentation is useful for small, imbalanced datasets.
- **Keep background images.** They reduce false positives in scenes with no target objects.
- **Version the dataset.** A hash or a tag per training run makes results reproducible.

[← Back to the main README](../README.md)
