# TopologyX

Topological Data Analysis library — filtrations, persistence descriptors, ToMaTo clustering, and Keras layers built on persistence features. Published to PyPI as `topologyx`.

## Stack

Python is bounded to `>=3.13,<3.15`: 3.13 and 3.14 are supported, and CI runs the full gate on both. Ruff and `ty` target 3.13, the floor, so code using a 3.14-only feature fails the gate. uv for packaging, Gudhi for simplicial complexes and persistence, scikit-learn for neighbours and decomposition, NumPy throughout, Keras on the JAX backend for the channel layers, Matplotlib for the plotting helpers, Marimo for the examples.

`scipy.stats.gaussian_kde` is imported by `clustering/` but SciPy is not a declared dependency — it arrives transitively through scikit-learn. Treat that as a latent break, not a licence to add more undeclared imports.

## Architecture

Three subpackages under `src/topologyx/`, and the unusual part is that **each `__init__.py` holds the implementation**, not re-exports. The sibling modules beside it are helpers.

- `filtrations/` — `Filtration` (alpha complex, or a hand-built simplex tree for 1D/2D/3D input), `Levels` (upper and lower sublevel filtration of a series), `FiltrationType`. `utils.py` builds Betti curves, persistence landscapes and persistence images, and plots them.
- `clustering/` — `TomatoClustering`, `ClusterGenerator`, `ClusterStructure`. `unionfind.py` is the weighted union-find with path compression that ToMaTo merges through; `utils.py` plots.
- `channels/` — `betti_channel` and `silhouette_channel`, 1D convolutional Keras stacks consuming persistence descriptors, plus `SilhouetteLayer` in `silhouette.py`.

Two constraints that shape the code:

- **Gudhi's Python modules are annotated and `ty` reads them, so no `# type: ignore` is needed or allowed.** `AlphaComplex` is imported from `gudhi.delaunay_complex` because `gudhi/__init__.py` exports it conditionally, and it takes points as nested lists (`.tolist()`), not an ndarray. `SimplexTreeProtocol` in `filtrations/__init__.py` types the simplex trees the public methods return; extend it rather than widening a signature to `Any`.
- **Importing `topologyx.channels` pulls Keras and JAX.** `channels/__init__.py` sets `KERAS_BACKEND` to `jax` with `os.environ.setdefault` before importing Keras, so a caller's explicit backend still wins, and a caller who imports `keras` first without setting it gets the TensorFlow default and fails. `tests/conftest.py` sets the same default for that reason. JAX is a declared dependency because TensorFlow, the Keras default, publishes no Python 3.14 wheels. The other two subpackages import neither, so keep Keras imports out of them.

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

- **`make types` passes warnings.** `error-on-warning = false`, and `unresolved-import` and `unresolved-attribute` are set to `warn`, so it exits 0 while reporting diagnostics. The tree is at zero diagnostics across `src/` and `tests/`; read the output and keep it there.
- **Ruff selects only `E`, `F`, `I001`, `W`.** Annotation, naming and docstring rules are enforced by nobody, so what `CONTRIBUTING.md` states about typing and naming is convention a reviewer checks, not a gate. One convention it does not state: no inline comments and no docstrings — names carry the meaning, and a comment is a second source of truth nothing verifies.

## Release

The version lives in `[project] version` of `pyproject.toml`, and that field is the only one the release reads.

Publishing is manual and never happens on merge. Run the `PyPI Release` workflow with a semantic version; it rewrites that field, pushes the bump directly to `main`, cuts the GitHub release, builds, publishes to PyPI, and opens a pull request from `gh/release-<version>`.

## Dependencies

Every direct dependency and the `hatchling` build requirement is pinned to an exact version. Renovate auto-merges minor and patch updates to Python dependencies, the build requirement, pre-commit hook revisions and workflow env versions annotated with a `# renovate:` comment after 7 days, and major updates to `[dependency-groups]` after 14. GitHub Actions `uses:` bumps open PRs that are merged by hand. Python rules in `renovate.json` match on the pep621 dependency types (`project.dependencies`, `dependency-groups`, `build-system.requires`), and Renovate's pre-commit manager is opted in explicitly because it is off by default.
