<div align="center">

<img src="assets/banner.svg" alt="CS2 Player Detection — YOLO detectors for Counter-Strike 2" width="100%">

# CS2 Player Detection

**YOLOv9, YOLOv10 and YOLO12 detectors for Counter-Strike 2 player and head localization.**

[![Architecture](https://img.shields.io/badge/Architecture-YOLOv9_%7C_v10_%7C_v12-0B1526)](https://github.com/ultralytics/ultralytics)
[![mAP@50](https://img.shields.io/badge/mAP%4050-0.979-22C55E)](#results)
[![Classes](https://img.shields.io/badge/Classes-4-22D3EE)](#class-labels)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97_Models-5-FFD21E)](https://huggingface.co/jparedesDS)

[← Model zoo](../../README.md) · [Full catalog](../../docs/model-zoo.md) · [Training guide](../../docs/training-guide.md)

</div>

---

## At a glance

| Property | Value |
|---|---|
| **Task** | Player body and head localization in Counter-Strike 2 |
| **Architectures** | YOLOv9c, YOLOv10s/m/b, YOLO12s |
| **Checkpoints** | 5 |
| **Classes** | `CT`, `CT_head`, `T`, `T_head` |
| **Best mAP@50** | **0.979** (YOLOv10s) |
| **Best mAP@50-95** | **0.772** (YOLOv10s) |
| **Weights** | [`cs2_yolov10s.pt`](https://huggingface.co/jparedesDS/cs2-yolov10s) and 4 more on Hugging Face |
| **Training notebook** | [`notebooks/yolov10s_training.ipynb`](notebooks/yolov10s_training.ipynb) |

## Overview

Five checkpoints trained to detect player bodies and heads in Counter-Strike 2 footage. The models are intended for computer-vision research, broadcast analysis and game-state extraction — not for interfering with live matches.

The dataset uses four classes that separate team identity from body part, so downstream code can reason about *who* is visible and *where* the head is without retraining. Across the series, the same dataset was used to compare how YOLOv9, YOLOv10 and YOLO12 behave on a small-object, high-occlusion problem.

## Models

| Model | Architecture | Weights | Params | GFLOPs | mAP@50 | mAP@50-95 | Hugging Face |
|---|---|---|:---:|:---:|:---:|:---:|---|
| CS2 · YOLOv9c | YOLOv9c | `yolov9c_cs2.pt` | — | — | — | — | [`cs2-yolov9c`](https://huggingface.co/jparedesDS/cs2-yolov9c) |
| CS2 · YOLOv10s | YOLOv10s | `cs2_yolov10s.pt` | 8.0 M | 24.5 | **0.979** | **0.772** | [`cs2-yolov10s`](https://huggingface.co/jparedesDS/cs2-yolov10s) |
| CS2 · YOLOv10m | YOLOv10m | `yolov10m_cs2.pt` | — | — | — | — | [`cs2-yolov10m`](https://huggingface.co/jparedesDS/cs2-yolov10m) |
| CS2 · YOLOv10b | YOLOv10b | `yolov10b_cs2.pt` | 20.4 M | 98.0 | **0.850** | **0.635** | [`cs2-yolov10b`](https://huggingface.co/jparedesDS/cs2-yolov10b) |
| CS2 · YOLO12s | YOLO12s | `cs2_yolo12s.pt` | 9.2 M | 21.2 | **0.717** | **0.453** | [`cs2_yolo12s`](https://huggingface.co/jparedesDS/cs2_yolo12s) |

> All five repositories are gated on Hugging Face: accept the conditions on the model card and run `hf auth login` before downloading.
>
> A dash means the metric was not published for that checkpoint. YOLOv9c and YOLOv10m expose only training-curve images on their model cards, without a numeric validation summary.

## Class labels

| ID | Label | Meaning |
|:---:|---|---|
| 0 | `CT` | Counter-Terrorist body |
| 1 | `CT_head` | Counter-Terrorist head |
| 2 | `T` | Terrorist body |
| 3 | `T_head` | Terrorist head |

The head/body split is deliberate: heads are small and heavily occluded, so mixing them with bodies would hide the hardest failure mode behind a strong body score.

## Results

Metrics for the YOLOv10s checkpoint on its validation split (160 images, 372 instances):

| Class | Precision | Recall | mAP@50 | mAP@50-95 |
|---|---:|---:|---:|---:|
| **all** | **0.958** | **0.940** | **0.979** | **0.772** |
| `ct_body` | 0.964 | 0.964 | 0.988 | 0.861 |
| `ct_head` | 0.946 | 0.847 | 0.953 | 0.634 |
| `t_body` | 0.986 | 0.976 | 0.990 | 0.866 |
| `t_head` | 0.938 | 0.973 | 0.984 | 0.728 |

Head localization is the hardest class, which is expected: heads are small, partially occluded and often overlap with the body box.

<details>
<summary><strong>YOLOv10b per-class metrics</strong> (90 images / 215 instances)</summary>

| Class | Precision | Recall | mAP@50 | mAP@50-95 |
|---|---:|---:|---:|---:|
| **all** | **0.908** | **0.757** | **0.850** | **0.635** |
| `ct_body` | 0.914 | 0.911 | 0.953 | 0.819 |
| `ct_head` | 0.909 | 0.639 | 0.735 | 0.465 |
| `t_body` | 0.932 | 0.921 | 0.964 | 0.781 |
| `t_head` | 0.877 | 0.556 | 0.748 | 0.476 |

</details>

<details>
<summary><strong>YOLO12s per-class metrics</strong> (90 images / 255 instances)</summary>

| Class | Precision | Recall | mAP@50 | mAP@50-95 |
|---|---:|---:|---:|---:|
| **all** | **0.873** | **0.556** | **0.717** | **0.453** |
| `CT_Body` | 0.915 | 0.595 | 0.786 | 0.574 |
| `CT_Head` | 0.848 | 0.485 | 0.685 | 0.361 |
| `T_Body` | 0.822 | 0.655 | 0.747 | 0.547 |
| `T_Head` | 0.905 | 0.491 | 0.648 | 0.329 |

</details>

> The YOLOv10b and YOLO12s checkpoints were evaluated on a smaller validation split (90 images) than YOLOv10s (160 images), so their scores are not directly comparable. YOLOv10s remains the recommended checkpoint for this project.

### Training results and label distribution

<p align="center">
  <img src="assets/results.png" alt="Training results" width="64%">
  <img src="assets/labels.jpg" alt="Label distribution" width="32%">
</p>

### Batch preview

<p align="center">
  <img src="assets/train_batch0.jpg" alt="Training batch with labels" width="80%">
</p>

## Quick start

```bash
hf download jparedesDS/cs2-yolov10s cs2_yolov10s.pt --local-dir weights
```

```python
from ultralytics import YOLO

model = YOLO("weights/cs2_yolov10s.pt")
results = model.predict("frame.jpg", conf=0.25, save=True, device=0)

for box in results[0].boxes:
    print(model.names[int(box.cls)], float(box.conf))
```

The same API works with every checkpoint: change the weight file and keep the class IDs.

## Dataset

- **Source:** Counter-Strike 2 gameplay frames captured at 16:9.
- **Format:** YOLO boxes, one `.txt` per image.
- **Classes:** 4, separating team (`CT`/`T`) from body part (`body`/`head`).
- **Variation:** multiple maps, lighting conditions and weapon viewpoints.
- **Distribution:** the dataset is **not** distributed. Class definitions and validation metrics are documented so equivalent datasets can be rebuilt.
- **Quality control:** annotations were audited with [`check_labels.py`](../../tools/annotations/check_labels.py); low-confidence images were pseudo-labeled with [`auto_label.py`](../../tools/annotations/auto_label.py) and corrected manually.

## Training

[`notebooks/yolov10s_training.ipynb`](notebooks/yolov10s_training.ipynb) contains the YOLOv10s training workflow, including dataset preparation and evaluation.

General instructions: [docs/training-guide.md](../../docs/training-guide.md).

## Related projects

- [CS2 Weapon Detection](../cs2-weapon-detection/) — 19-class weapon detector built on the same capture pipeline.
- [Valorant Player Detection](../valorant-players-detection/) — the same body/head formulation in a different tactical shooter.
- [Full model zoo](../../docs/model-zoo.md) — every checkpoint, parameter count and class list.

## License

MIT. See the [repository license](../../LICENSE).
