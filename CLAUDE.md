# TopologyX

Topological Data Analysis library — filtrations, persistence descriptors, ToMaTo clustering, and Keras layers built on persistence features. Published to PyPI as `topologyx`.

## Stack

Python is bounded to `>=3.13,<3.15`: 3.13 and 3.14 are supported, and CI runs the full gate on both. Ruff and `ty` take their target version from the `requires-python` floor, 3.13, so code using a 3.14-only feature fails the gate. uv for packaging, Gudhi for simplicial complexes and persistence, scikit-learn for neighbours and decomposition, NumPy throughout, Keras on the JAX backend for the channel layers, Matplotlib for the plotting helpers, Marimo for the examples.

`scipy.stats.gaussian_kde` is imported by `clustering/` but SciPy is not a declared dependency — it arrives transitively through scikit-learn. Treat that as a latent break, not a licence to add more undeclared imports.

## Architecture

Three subpackages under `src/topologyx/`, and the unusual part is that **each `__init__.py` holds the implementation**, not re-exports. The sibling modules beside it are helpers.

- `filtrations/` — `Filtration` (alpha complex, or a hand-built simplex tree for 1D/2D/3D input), `Levels` (upper and lower sublevel filtration of a series), `FiltrationType`. `utils.py` builds Betti curves, persistence landscapes and persistence images, and plots them.
- `clustering/` — `TomatoClustering`, `ClusterGenerator`, `ClusterStructure`. `unionfind.py` is the weighted union-find with path compression that ToMaTo merges through; `utils.py` plots.
- `channels/` — `betti_channel` and `silhouette_channel`, 1D convolutional Keras stacks consuming persistence descriptors, plus `SilhouetteLayer` in `silhouette.py`.

Two constraints that shape the code:

- **Gudhi's Python modules are annotated and `ty` reads them, so no `# type: ignore` is needed or allowed.** `AlphaComplex` is imported from `gudhi.delaunay_complex` because `gudhi/__init__.py` exports it conditionally, and it takes points as nested lists (`.tolist()`), not an ndarray. `SimplexTreeProtocol` in `filtrations/__init__.py` types the simplex trees the public methods return; extend it rather than widening a signature to `Any`.
- **Importing `topologyx.channels` pulls Keras and JAX.** Before importing Keras, `channels/__init__.py` calls `select_keras_backend` (`channels/backend.py`). An explicit `KERAS_BACKEND` is always kept. Otherwise it reads the `backend` from `keras.json`, located the way Keras locates it (`$KERAS_HOME`, else `~/.keras`, else `/tmp/.keras`), with `tensorflow` as the default, and sets `KERAS_BACKEND` to `jax` only when that is a known Keras backend whose module is not installed. Keras writes `keras.json` with `tensorflow` on its first import, so a configured backend counts as a choice only when its module is installed; an unknown backend name is left for Keras to reject. A caller who imports `keras` before `topologyx.channels` bypasses this; `tests/conftest.py` sets `KERAS_BACKEND` to `jax` for that reason. JAX is a declared dependency because TensorFlow, the Keras default, publishes no Python 3.14 wheels. `jaxlib` publishes no Intel macOS wheel, so the `jax` requirement carries a marker that skips that platform; an Intel Mac caller of `topologyx.channels` sets `KERAS_BACKEND` to a backend they install. The other two subpackages import neither, so keep Keras imports out of them.

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

CI runs on `pull_request`, `merge_group` and `workflow_dispatch`. It runs the same four make targets, plus `renovate-config-validator` on the 3.13 leg.

Two gates are weaker than they look:

- **`make types` passes warnings.** `error-on-warning = false`, and `unresolved-import` and `unresolved-attribute` are set to `warn`, so it exits 0 while reporting diagnostics. The tree is at zero diagnostics across `src/` and `tests/`; read the output and keep it there.
- **Ruff selects only `E`, `F`, `I001`, `W`.** Annotation, naming and docstring rules are enforced by nobody, so what `CONTRIBUTING.md` states about typing and naming is convention a reviewer checks, not a gate. One convention it does not state: no inline comments and no docstrings — names carry the meaning, and a comment is a second source of truth nothing verifies.

## Release

The version lives in `[project] version` of `pyproject.toml`, and that field is the only one the release reads.

Publishing is manual and never happens on merge. Run the `PyPI Release` workflow with a semantic version; it sets the version with `uv version`, which rewrites that field and `uv.lock` together, commits the bump on `gh/release-<version>`, cuts the GitHub release from that branch so the tag holds the bump, builds, publishes to PyPI, and opens a pull request that brings the bump to `main`.

## Dependencies

Every direct dependency and the `hatchling` build requirement is pinned to an exact version, and the committed `uv.lock` pins the full resolution. Renovate auto-merges minor and patch updates to Python dependencies, the build requirement, pre-commit hook revisions and workflow env versions annotated with a `# renovate:` comment after 7 days, and major updates to `[dependency-groups]` after 14. GitHub Actions `uses:` bumps open PRs that are merged by hand, and so does a new Node major for setup-node's `node-version`, which keeps its major-only value instead of being pinned. Python rules in `renovate.json` match on the pep621 dependency types (`project.dependencies`, `dependency-groups`, `build-system.requires`), and Renovate's pre-commit manager is opted in explicitly because it is off by default. The `ruff` and `commitizen` hooks are local hooks that run the pinned dev dependencies through `uv run --frozen`, so a hook always uses the version CI checks with; the pre-commit manager only tracks `pre-commit-hooks`. Weekly lock file maintenance re-resolves the transitive dependencies in `uv.lock` and auto-merges with no release-age wait. CI installs with `uv sync --locked`, so a `uv.lock` out of step with `pyproject.toml` fails the build.
