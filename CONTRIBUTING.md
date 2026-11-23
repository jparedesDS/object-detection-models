# Contributing

Thanks for your interest in these models. This repository is primarily a personal model zoo, but issues, corrections and well-scoped pull requests are welcome.

[← Back to the main README](README.md)

---

## Reporting a problem

Open an issue with:

- The model or project involved (for example `cs2-yolov10s`).
- The exact weight filename.
- The command or code snippet you ran, including `ultralytics` and `torch` versions.
- The full error traceback, if any.
- A sample image or a description of the scene when the failure is visual.

Please **do not** upload datasets, personal information or footage that violates a game's terms of service.

## Requesting a model

Model requests are welcome. Include:

- The target domain and why existing checkpoints are insufficient.
- The classes you need.
- Whether you can contribute annotated data or only evaluation data.
- Any latency or deployment constraints (CPU, Jetson, browser, etc.).

## Pull requests

1. Open an issue first for anything larger than a typo or a documentation fix.
2. Keep changes focused: one concern per pull request.
3. Follow the existing structure:
   - Project documentation under `projects/<project>/README.md`.
   - Shared tooling under `tools/`.
   - Guides under `docs/`.
4. Do not commit datasets, model weights, `runs/`, virtual environments or notebook outputs containing sensitive paths.
5. If you add a model, update:
   - `docs/model-zoo.md`
   - The root `README.md` and `README.es.md` tables
   - The corresponding project README
6. Test any script you modify. At minimum, run it on a small synthetic dataset.

## Documentation style

- English is the primary language; `README.es.md` is the Spanish mirror.
- Use relative links inside the repository and absolute links for Hugging Face.
- Report metrics with the evaluation split and command used. Do not present numbers without context.

## Code style

- Python 3.9+.
- Four-space indentation, descriptive names, no hardcoded credentials.
- Keep utility scripts runnable as standalone files; avoid adding a package structure unless it is justified.

## License

By contributing, you agree that your contributions are licensed under the MIT License.
