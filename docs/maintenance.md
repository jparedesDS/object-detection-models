# Repository maintenance

Three recurring tasks keep the zoo consistent across GitHub and Hugging Face.

[← Back to the main README](../README.md)

---

## 1. Link every Hugging Face model card back to this repo

Readers often land on a Hugging Face model card first. Each card should point back to the
consolidated repository and to the concrete project page, so they can find the dataset
notes, training notebooks and related checkpoints.

**Recommended block** (append to the model card):

```markdown
---

## 🔗 Part of the Object Detection Models zoo

This checkpoint is documented in the consolidated **[object-detection-models](https://github.com/jparedesDS/object-detection-models)** repository.

- **Project page:** [<Project title>](https://github.com/jparedesDS/object-detection-models/tree/main/projects/<slug>)
- **Full catalog:** [docs/model-zoo.md](https://github.com/jparedesDS/object-detection-models/blob/main/docs/model-zoo.md)
- **Training guide:** [docs/training-guide.md](https://github.com/jparedesDS/object-detection-models/blob/main/docs/training-guide.md)
```

**Automated:** [`tools/update_hf_cards.py`](../tools/update_hf_cards.py) inserts this block
into all 14 model cards. It is idempotent (a hidden marker prevents duplicates) and supports
`--dry-run` and `--only`.

```bash
pip install huggingface_hub
hf auth login                              # or set HF_TOKEN=hf_...
python tools/update_hf_cards.py --dry-run  # preview
python tools/update_hf_cards.py            # commit
```

> **Requires a Hugging Face token with write access.** Gated repositories also require that
> the token has been granted access. Without a token the script cannot read or write the
> cards; run it on a machine where you are authenticated.

---

## 2. GitHub social preview

The repository social preview is the image shown when the repo is shared on social media
or in link previews. GitHub does not expose this setting through the API, so it must be set
from the web UI:

1. Open **Settings → General** on
   [`jparedesDS/object-detection-models`](https://github.com/jparedesDS/object-detection-models/settings).
2. Scroll to **Social preview**.
3. Click **Upload an image…** and select [`assets/social-preview.png`](../assets/social-preview.png).

The provided PNG is **1280 × 640**, the size GitHub recommends. Its editable source is
[`assets/social-preview.svg`](../assets/social-preview.svg); regenerate the PNG with any
SVG renderer (or headless Chrome) after editing:

```bash
chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1280,640 --screenshot=assets/social-preview.png \
  file:///absolute/path/to/assets/social-preview.svg
```

---

## 3. Adding a new model

When you publish a new checkpoint, update **three places** so the catalog never drifts:

1. **[`docs/model-zoo.md`](model-zoo.md)**
   - Add a row to *Metrics at a glance* (precision, recall, mAP@50, mAP@50-95, params, GFLOPs).
   - Add a row to *Checkpoints and weight files* (repo, weight filename, validation split).
   - Add the class list to *Class taxonomy* if it introduces new labels.
2. **Root READMEs** — [`README.md`](../README.md) and [`README.es.md`](../README.es.md)
   - Add the model to the appropriate domain table (Industrial NDT / Esports & gaming).
   - Add or update the project row in the *Projects* table.
   - Update the model count in the banner/badges if it changes.
3. **Project README** — `projects/<slug>/README.md`
   - Create the project folder with `assets/` (banner + training images) and an optional notebook.
   - Fill the *At a glance*, *Models*, *Class labels*, *Results*, *Quick start* and *Dataset* sections.
   - Link back to the model zoo and related projects.

**Checklist**

- [ ] Weights published on Hugging Face with a model card.
- [ ] Metrics copied from the training artifacts (`model.val()` output), not estimated.
- [ ] Missing values left as `—`, never invented.
- [ ] Banner generated (`projects/<slug>/assets/banner.svg`).
- [ ] All training images referenced in the project README.
- [ ] `docs/model-zoo.md`, `README.md`, `README.es.md` and the project README updated together.
- [ ] Back-link added to the Hugging Face card (task 1).
- [ ] Link/case checks pass before committing.

> **Metrics provenance.** Prefer the numeric validation summary printed by Ultralytics
> (`Class / Images / Instances / Box(P R mAP50 mAP50-95)`). If a model card only publishes
> training-curve images, leave the numeric cells as `—` rather than reading values off a plot.
