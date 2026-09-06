# TopologyX

Topological Data Analysis library — filtrations, persistence descriptors, ToMaTo clustering, and Keras layers built on persistence features. Published to PyPI as `topologyx`.

## Stack

Python is pinned to `==3.13.*` — an exact pin, not a floor, so `uv sync` refuses any other interpreter. uv for packaging, Gudhi for simplicial complexes and persistence, scikit-learn for neighbours and decomposition, NumPy throughout, Keras for the channel layers, Matplotlib for the plotting helpers, Marimo for the examples.

`scipy.stats.gaussian_kde` is imported by `clustering/` but SciPy is not a declared dependency — it arrives transitively through scikit-learn. Treat that as a latent break, not a licence to add more undeclared imports.

## Architecture

Three subpackages under `src/topologyx/`, and the unusual part is that **each `__init__.py` holds the implementation**, not re-exports. The sibling modules beside it are helpers.

- `filtrations/` — `Filtration` (alpha complex, or a hand-built simplex tree for 1D/2D/3D input), `Levels` (upper and lower sublevel filtration of a series), `FiltrationType`. `utils.py` builds Betti curves, persistence landscapes and persistence images, and plots them.
- `clustering/` — `TomatoClustering`, `ClusterGenerator`, `ClusterStructure`. `unionfind.py` is the weighted union-find with path compression that ToMaTo merges through; `utils.py` plots.
- `channels/` — `betti_channel` and `silhouette_channel`, 1D convolutional Keras stacks consuming persistence descriptors, plus `SilhouetteLayer` in `silhouette.py`.

Two constraints that shape the code:

- **Gudhi ships no type stubs.** Every `gudhi.SimplexTree()` and `gudhi.AlphaComplex()` construction carries `# type: ignore`, and `SimplexTreeProtocol` in `filtrations/__init__.py` exists to give the returned object a typed interface. Extend that Protocol rather than widening a signature to `Any`.
- **Importing `topologyx.channels` pulls Keras and a configured backend.** The other two subpackages do not, so keep Keras imports out of them.

`Filtration` built with `use_alpha=False` handles 1D, 2D and 3D input only and raises `ValueError` beyond that; the alpha-complex path has no such ceiling.

## Public API

Semver tracks what the three subpackages export:

```python
from topologyx.filtrations import Filtration, FiltrationType, Levels
from topologyx.clustering import ClusterGenerator, ClusterStructure, TomatoClustering
from topologyx.channels import betti_channel, silhouette_channel
```

Renaming or removing any of those, or changing a keyword argument on their public methods, is a breaking change.

The package is import-only in practice. `pyproject.toml` declares a `topologyx` console script pointing at `topologyx.main:cli`, but `src/topologyx/main.py` is empty, so the installed command fails — do not document or extend a CLI without implementing it first.

## Commands

| Command              | Purpose                                 |
| -------------------- | --------------------------------------- |
| `make setup`         | Install dependencies + pre-commit hooks |
| `make setup-hard`    | Clean install from scratch              |
| `make format`        | Check formatting                        |
| `make format-fix`    | Format with Ruff                        |
| `make lint`          | Lint with Ruff                          |
| `make lint-fix`      | Lint and auto-fix                       |
| `make types`         | Type check with ty                      |
| `make test`          | Run the test suite                      |
| `make test-coverage` | Run tests with a coverage report        |
| `make marimo`        | Open the examples in Marimo             |
| `make uv-lock`       | Lock dependencies                       |
| `make uv-update`     | Upgrade the lockfile                    |

There is no `check` aggregate. `make format lint types test` is the full local gate.

`examples/` holds Marimo notebooks, which are plain `.py` files and are linted and formatted like the rest of the source.

## Gates

`make setup` installs the pre-commit hooks. They run on every commit: trailing whitespace, end-of-file, YAML and TOML syntax, `ruff format`, `ruff check --fix`, and commitizen on the message — so every commit must be a Conventional Commit.

CI runs on `pull_request` and `merge_group`, and runs the same four make targets.

Two gates are weaker than they look:

- **`make types` is advisory.** `error-on-warning = false`, and the noisy `ty` rules are set to `warn`, so it exits 0 while reporting diagnostics. Read its output; a green exit is not a clean type check.
- **Ruff selects only `E`, `F`, `I001`, `W`.** Annotation, naming and docstring rules are enforced by nobody, so what `CONTRIBUTING.md` states about typing and naming is convention a reviewer checks, not a gate. One convention it does not state: no inline comments and no docstrings — names carry the meaning, and a comment is a second source of truth nothing verifies.

## Release

The version lives in `[project] version` of `pyproject.toml`, and that field is the only one the release reads.

Publishing is manual and never happens on merge. Run the `PyPI Release` workflow with a semantic version; it rewrites that field, pushes the bump directly to `main`, cuts the GitHub release, builds, publishes to PyPI, and opens a pull request from `gh/release-<version>`.

## Dependencies

Every dependency is pinned to an exact version. Renovate auto-merges minor and patch updates after 7 days, major updates to dev dependencies after 14, and security updates immediately.
