#!/usr/bin/env python3
"""Add a back-link to the object-detection-models zoo in each Hugging Face model card.

The consolidated GitHub repository is the canonical documentation hub. Every model
card should point back to it and to the concrete project page, so readers landing on
Hugging Face can find the dataset notes, training notebooks and related checkpoints.

Requirements
------------
* ``pip install huggingface_hub``
* A Hugging Face token with **write** access to the repositories, and access to any
  gated repository you want to update::

      hf auth login                 # interactive, stores the token
      # or:  set HF_TOKEN=hf_...    # environment variable

Usage
-----
::

    python tools/update_hf_cards.py --dry-run     # show what would change
    python tools/update_hf_cards.py               # commit the changes
    python tools/update_hf_cards.py --only cs2-yolov10b valorant-yolo11m

The script is idempotent: a hidden marker comment prevents duplicate sections.
"""

from __future__ import annotations

import argparse
import os
import sys
import tempfile

REPO_URL = "https://github.com/jparedesDS/object-detection-models"
MARKER = "<!-- object-detection-models:backlink -->"

# Hugging Face repository id -> (project slug, human-readable project title)
MODELS: dict[str, tuple[str, str]] = {
    "jparedesDS/cs2-yolov9c": ("cs2-players-detection", "CS2 Player Detection"),
    "jparedesDS/cs2-yolov10s": ("cs2-players-detection", "CS2 Player Detection"),
    "jparedesDS/cs2-yolov10m": ("cs2-players-detection", "CS2 Player Detection"),
    "jparedesDS/cs2-yolov10b": ("cs2-players-detection", "CS2 Player Detection"),
    "jparedesDS/cs2_yolo12s": ("cs2-players-detection", "CS2 Player Detection"),
    "jparedesDS/cs2-yolo12m-weapon-detection": ("cs2-weapon-detection", "CS2 Weapon Detection"),
    "jparedesDS/valorant-yolov10b": ("valorant-players-detection", "Valorant Player Detection"),
    "jparedesDS/valorant-yolo11m": ("valorant-players-detection", "Valorant Player Detection"),
    "jparedesDS/deadlock-yolo11l": ("deadlock-players-detection", "Deadlock Player Detection"),
    "jparedesDS/ow2-yolo11m": ("overwatch2-players-detection", "Overwatch 2 Detection"),
    "jparedesDS/fortnite-yolo11m": ("fortnite-players-detection", "Fortnite Player Detection"),
    "jparedesDS/lol-map-tracking-object-detection": ("league-of-legends-tracking", "League of Legends Tracking"),
    "jparedesDS/welding-defects-detection": ("welding-defects-detection", "Welding Defects Detection"),
    "jparedesDS/fluorescent-penetrant-inspection": ("fluorescent-penetrant-inspection", "Fluorescent Penetrant Inspection"),
}


def backlink_block(slug: str, title: str) -> str:
    project_url = f"{REPO_URL}/tree/main/projects/{slug}"
    catalog_url = f"{REPO_URL}/blob/main/docs/model-zoo.md"
    return (
        f"{MARKER}\n"
        "---\n\n"
        "## 🔗 Part of the Object Detection Models zoo\n\n"
        f"This checkpoint is documented in the consolidated **[object-detection-models]({REPO_URL})** repository.\n\n"
        f"- **Project page:** [{title}]({project_url})\n"
        f"- **Full catalog:** [docs/model-zoo.md]({catalog_url})\n"
        f"- **Training guide:** [docs/training-guide.md]({REPO_URL}/blob/main/docs/training-guide.md)\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="Print the planned changes without committing.")
    parser.add_argument("--only", nargs="*", metavar="REPO", help="Restrict to these Hugging Face repository ids (short or full).")
    parser.add_argument("--token", default=os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN"), help="Hugging Face token (defaults to HF_TOKEN / cached login).")
    args = parser.parse_args()

    try:
        from huggingface_hub import HfApi, hf_hub_download
    except ImportError:
        print("huggingface_hub is required: pip install huggingface_hub", file=sys.stderr)
        return 1

    api = HfApi(token=args.token)

    selected = MODELS
    if args.only:
        wanted = {r if "/" in r else f"jparedesDS/{r}" for r in args.only}
        selected = {k: v for k, v in MODELS.items() if k in wanted}
        missing = wanted - set(selected)
        if missing:
            print(f"Unknown repositories: {', '.join(sorted(missing))}", file=sys.stderr)
            return 1

    changed = skipped = failed = 0
    for repo_id, (slug, title) in selected.items():
        try:
            local = hf_hub_download(repo_id=repo_id, filename="README.md", repo_type="model", token=args.token)
            text = open(local, encoding="utf-8").read()
        except Exception as exc:  # gated / missing / network
            print(f"[skip] {repo_id}: cannot read README ({exc})")
            failed += 1
            continue

        if MARKER in text:
            print(f"[ok]   {repo_id}: back-link already present")
            skipped += 1
            continue

        new_text = text.rstrip() + "\n\n" + backlink_block(slug, title)
        if args.dry_run:
            print(f"[dry]  {repo_id}: would append back-link to projects/{slug}")
            changed += 1
            continue

        try:
            api.upload_file(
                path_or_fileobj=new_text.encode("utf-8"),
                path_in_repo="README.md",
                repo_id=repo_id,
                repo_type="model",
                commit_message="docs: link back to the object-detection-models zoo",
            )
            print(f"[done] {repo_id}: back-link committed")
            changed += 1
        except Exception as exc:
            print(f"[fail] {repo_id}: {exc}")
            failed += 1

    print(f"\nSummary: {changed} updated, {skipped} already linked, {failed} failed.")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
