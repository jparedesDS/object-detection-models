# Model Zoo — Full Catalog

Complete catalog of the 14 object-detection checkpoints published in this repository. Every model is a fine-tuned [Ultralytics](https://github.com/ultralytics/ultralytics) detector and has a public model card on [Hugging Face](https://huggingface.co/jparedesDS).

[← Back to the main README](../README.md)

---

## Metrics at a glance

| Model | Architecture | Domain | Classes | Precision | Recall | mAP@50 | mAP@50-95 | Params | GFLOPs |
|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [Welding Defects Detection](https://huggingface.co/jparedesDS/welding-defects-detection) | YOLO11x | Industrial NDT | 4 | 0.826 | 0.827 | **0.842** | **0.632** | 56.8 M | 194.4 |
| [Fluorescent Penetrant Inspection](https://huggingface.co/jparedesDS/fluorescent-penetrant-inspection) | YOLO11l | Industrial NDT | 1 | 0.794 | 0.771 | **0.793** | **0.379** | 25.3 M | 86.6 |
| [CS2 Players · YOLOv9c](https://huggingface.co/jparedesDS/cs2-yolov9c) | YOLOv9c | Esports | 4 | — | — | — | — | — | — |
| [CS2 Players · YOLOv10s](https://huggingface.co/jparedesDS/cs2-yolov10s) | YOLOv10s | Esports | 4 | 0.958 | 0.940 | **0.979** | **0.772** | 8.0 M | 24.5 |
| [CS2 Players · YOLOv10m](https://huggingface.co/jparedesDS/cs2-yolov10m) | YOLOv10m | Esports | 4 | — | — | — | — | — | — |
| [CS2 Players · YOLOv10b](https://huggingface.co/jparedesDS/cs2-yolov10b) | YOLOv10b | Esports | 4 | 0.908 | 0.757 | **0.850** | **0.635** | 20.4 M | 98.0 |
| [CS2 Players · YOLO12s](https://huggingface.co/jparedesDS/cs2_yolo12s) | YOLO12s | Esports | 4 | 0.873 | 0.556 | **0.717** | **0.453** | 9.2 M | 21.2 |
| [CS2 Weapons · YOLO12m](https://huggingface.co/jparedesDS/cs2-yolo12m-weapon-detection) | YOLO12m | Esports | 19 | 0.963 | 1.000 | **0.993** | **0.871** | 20.1 M | 67.2 |
| [Valorant Players · YOLOv10b](https://huggingface.co/jparedesDS/valorant-yolov10b) | YOLOv10b | Esports | 2 | 0.959 | 0.886 | **0.925** | **0.631** | 20.4 M | 97.9 |
| [Valorant Players · YOLO11m](https://huggingface.co/jparedesDS/valorant-yolo11m) | YOLO11m | Esports | 2 | 0.963 | 0.898 | **0.931** | **0.655** | 20.0 M | 67.7 |
| [Deadlock Players · YOLO11l](https://huggingface.co/jparedesDS/deadlock-yolo11l) | YOLO11l | Esports | 4 | 0.874 | 0.798 | **0.856** | **0.486** | 25.3 M | 86.6 |
| [Overwatch 2 · YOLO11m](https://huggingface.co/jparedesDS/ow2-yolo11m) | YOLO11m | Esports | 1 | 0.742 | 0.563 | **0.660** | **0.317** | 20.0 M | 67.6 |
| [Fortnite · YOLO11m](https://huggingface.co/jparedesDS/fortnite-yolo11m) | YOLO11m | Esports | 2 | 0.933 | 0.739 | **0.828** | **0.668** | 20.0 M | 67.7 |
| [League of Legends · YOLO11m](https://huggingface.co/jparedesDS/lol-map-tracking-object-detection) | YOLO11m | Esports | 167 | 0.978 | 0.991 | **0.993** | **0.970** | 20.2 M | 68.4 |

> A dash means the value was not recorded in the training artifacts available for that checkpoint. Metrics are evaluated on each project's own validation split and are not directly comparable across datasets.

---

## Checkpoints and weight files

| Project | Hugging Face repository | Weight file | Validation split |
|---|---|---|---|
| CS2 players · YOLOv9c | [`cs2-yolov9c`](https://huggingface.co/jparedesDS/cs2-yolov9c) | `yolov9c_cs2.pt` | — |
| CS2 players · YOLOv10s | [`cs2-yolov10s`](https://huggingface.co/jparedesDS/cs2-yolov10s) | `cs2_yolov10s.pt` | 160 images / 372 instances |
| CS2 players · YOLOv10m | [`cs2-yolov10m`](https://huggingface.co/jparedesDS/cs2-yolov10m) | `yolov10m_cs2.pt` | — |
| CS2 players · YOLOv10b | [`cs2-yolov10b`](https://huggingface.co/jparedesDS/cs2-yolov10b) | `yolov10b_cs2.pt` | 90 images / 215 instances |
| CS2 players · YOLO12s | [`cs2_yolo12s`](https://huggingface.co/jparedesDS/cs2_yolo12s) | `cs2_yolo12s.pt` | 90 images / 255 instances |
| CS2 weapons · YOLO12m | [`cs2-yolo12m-weapon-detection`](https://huggingface.co/jparedesDS/cs2-yolo12m-weapon-detection) | `cs2-yolo12m-weapon-detection.pt` | 87 images / 158 instances |
| Valorant · YOLOv10b | [`valorant-yolov10b`](https://huggingface.co/jparedesDS/valorant-yolov10b) | `yolov10b_vlr.pt` | 999 images / 2,016 instances |
| Valorant · YOLO11m | [`valorant-yolo11m`](https://huggingface.co/jparedesDS/valorant-yolo11m) | `vlr-yolo11m.pt` | 999 images / 2,016 instances |
| Deadlock · YOLO11l | [`deadlock-yolo11l`](https://huggingface.co/jparedesDS/deadlock-yolo11l) | `yolo11l_deadlock.pt` | 551 images / 661 instances |
| Overwatch 2 · YOLO11m | [`ow2-yolo11m`](https://huggingface.co/jparedesDS/ow2-yolo11m) | `ow2-yolo11m.pt` | 273 images / 133 instances |
| Fortnite · YOLO11m | [`fortnite-yolo11m`](https://huggingface.co/jparedesDS/fortnite-yolo11m) | `fortnite-yolo11m.pt` | 1,014 images / 2,097 instances |
| League of Legends · YOLO11m | [`lol-map-tracking-object-detection`](https://huggingface.co/jparedesDS/lol-map-tracking-object-detection) | `yolo11m_lol-tracking.pt` | 822 images / 1,058 instances |
| Welding defects · YOLO11x | [`welding-defects-detection`](https://huggingface.co/jparedesDS/welding-defects-detection) | `welding_defects_yolo11x.pt` | 116 images / 773 instances |
| Fluorescent penetrant inspection · YOLO11l | [`fluorescent-penetrant-inspection`](https://huggingface.co/jparedesDS/fluorescent-penetrant-inspection) | `yolo11l_LPI.pt` | 836 images / 752 instances |

Download example:

```bash
hf download jparedesDS/welding-defects-detection welding_defects_yolo11x.pt --local-dir weights
```

---

## Class taxonomy

### Industrial inspection

| Dataset | Classes |
|---|---|
| Welding defects | `Defect`, `Welding Line`, `Workpiece`, `porosity` |
| Fluorescent penetrant inspection | `defecto` |

### Esports

| Dataset | Classes |
|---|---|
| CS2 players | `CT`, `CT_head`, `T`, `T_head` |
| CS2 weapons | `AK47`, `M4A1-S`, `M4A1`, `GALIL`, `FAMAS`, `TEC-9`, `FIVE-SEVEN`, `GLOCK-18`, `USP-S`, `EAGLE`, `BERETTAS`, `P2000`, `MAC10`, `MP5`, `MP9`, `P90`, `P250`, `SSG08`, `AWP` |
| Valorant | `Body`, `Head` |
| Deadlock | `deny`, `enemy`, `hit`, `minions` |
| Fortnite | `head`, `player` |
| Overwatch 2 | `Head` |
| League of Legends | 167 champion classes — see below |

### League of Legends (167 classes)

The checkpoint uses one class per champion icon. A few duplicate spellings are inherited from the annotation pipeline (for example `ChoGath`/`Chogath`, `Jayce`/`Jaycew`, `VelKoz`/`Velkoz`, `RekSai`/`Reksai`); they are preserved so the class IDs stay compatible with the published weights.

<details>
<summary>Show all 167 labels</summary>

```text
Aatrox, Ahri, Akali, Akshan, Alistar, Amumu, Anivia, Annie, Aphelios, Ashe,
AurelionSol, Azir, Bard, Blitzcrank, Brand, Braum, Caitlyn, Camille, Cassiopeia, ChoGath,
Chogath, Corki, Darius, Diana, DrMundo, Draven, Ekko, Elise, Evelynn, Ezreal,
Fiddlesticks, Fiora, Fizz, Galio, Gangplank, Garen, Gnar, Gragas, Graves, Gwen,
Hecarim, Heimerdinger, Illaoi, Irelia, Ivern, Janna, Jarvan, Jax, Jayce, Jaycew,
Jhin, Jinx, Kaisa, Kalista, Kane, Karma, Karthus, Kassadin, Katarina, Kayle,
Kayn, Kennen, KhaZix, Kindred, Kled, KogMaw, LeBlanc, LeeSin, Leona, Lilia,
Lillia, Lissandra, Lucian, Lulu, Lux, Malphite, Malzahar, Maokai, MasterYi, Mindred,
MissFortune, Mordekaiser, Morgana, Nami, Nasus, Nautilus, Neeko, Nidalee, Nilah, Nocturne,
Nunu, Olaf, Orianna, Ornn, Pantheon, Poppy, Pyke, Qiyana, Quinn, Rakan,
Rammus, RekSai, Reksai, Rell, Renata, Renekton, Rengar, Riven, Rumble, Ryze,
Samira, Sejuani, Senna, Seraphine, Sett, Shaco, Shen, Shyvana, Singed, Sion,
Sivir, Skarner, Sona, Soraka, Swain, Sylas, Syndra, TahmKench, Taliyah, Talon,
Taric, Teemo, Thresh, Tristana, Trundle, Tryndamere, TwistedFate, Twitch, Udyr, Urgot,
Varus, Vayne, Veigar, VelKoz, Velkoz, Vex, Vi, Viego, Viktor, Vladimir,
Volibear, Warwick, Wukong, Xayah, Xerath, XinZhao, Yasuo, Yone, Yorick, Yuumi,
Zac, Zed, Zeri, Ziggs, Zilean, Zoe, Zyra
```

</details>

---

## Model families

| Family | Checkpoints | Notes |
|---|---|---|
| YOLOv9 | `cs2-yolov9c` | Programmable Gradient Information backbone; anchor-free detection head. |
| YOLOv10 | `cs2-yolov10s`, `cs2-yolov10m`, `cs2-yolov10b`, `valorant-yolov10b` | NMS-free end-to-end inference and consistent dual assignments. |
| YOLO11 | `valorant-yolo11m`, `deadlock-yolo11l`, `ow2-yolo11m`, `fortnite-yolo11m`, `lol-map-tracking-object-detection`, `welding-defects-detection`, `fluorescent-penetrant-inspection` | C3k2 blocks and attention improvements; strong accuracy/latency trade-off. |
| YOLO12 | `cs2_yolo12s`, `cs2-yolo12m-weapon-detection` | Attention-centric architecture with area attention. |

All checkpoints load directly with the `ultralytics` package:

```python
from ultralytics import YOLO

model = YOLO("weights/<weight-file>.pt")
model.info()
```

---

## Gated models

Some Hugging Face repositories require accepting access conditions before download:

- `cs2-yolov9c`, `cs2-yolov10s`, `cs2-yolov10m`, `cs2-yolov10b`, `cs2_yolo12s`
- `valorant-yolov10b`, `valorant-yolo11m`
- `ow2-yolo11m`, `fortnite-yolo11m`
- `deadlock-yolo11l`, `welding-defects-detection`, `lol-map-tracking-object-detection`, `fluorescent-penetrant-inspection`

Open the model card, accept the conditions, then authenticate locally:

```bash
hf auth login
```

`cs2-yolo12m-weapon-detection` is publicly downloadable without gating.

---

## Reproducibility notes

- Training artifacts (`results.csv`, `results.png`, confusion matrices, curves, batch previews, `args.yaml`) are stored in each Hugging Face repository.
- The original training notebooks are available under `projects/*/notebooks/` when they were preserved.
- Dataset images are **not** redistributed. The labels and class taxonomies are documented above so you can rebuild equivalent datasets.
- Metrics should be reproduced with `model.val(data="your-data.yaml", imgsz=<training size>)` on the same split.

[← Back to the main README](../README.md)
