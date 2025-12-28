# TopologyX

Topological Data Analysis (TDA) library for Python projects.

## Tech Stack

| Layer                | Technology     |
| -------------------- | -------------- |
| Language             | Python 3.13    |
| Package Manager      | uv             |
| Linting & Formatting | Ruff           |
| Type Checking        | ty             |
| Testing              | Pytest         |
| CI/CD                | GitHub Actions |

## Prerequisites

- Python 3.13
- uv (Astral package manager)

## Quick Start

```bash
git clone https://github.com/merylldindin/topologyx
cd topologyx
make setup
```

## Project Structure

```
topologyx/
├── src/topologyx/           # Main package
│   ├── main.py              # CLI entry point
│   ├── channels/            # Signal processing channels
│   │   ├── __init__.py
│   │   └── silhouette.py
│   ├── clustering/          # Clustering algorithms
│   │   ├── __init__.py
│   │   ├── unionfind.py
│   │   └── utils.py
│   └── filtrations/         # TDA filtrations
│       ├── __init__.py
│       └── utils.py
├── examples/                # Marimo notebook examples
│   ├── clustering.py
│   └── filtrations.py
├── pyproject.toml           # uv configuration
├── .pre-commit-config.yaml
├── Makefile
└── renovate.json
```

## Commands

| Command              | Purpose                                 |
| -------------------- | --------------------------------------- |
| `make setup`         | Install dependencies + pre-commit hooks |
| `make setup-hard`    | Clean install from scratch              |
| `make format`        | Check code formatting                   |
| `make format-fix`    | Format code with Ruff                   |
| `make lint`          | Lint code with Ruff                     |
| `make lint-fix`      | Auto-fix linting issues                 |
| `make types`         | Type check with ty                      |
| `make test`          | Run test suite                          |
| `make test-coverage` | Run tests with coverage                 |
| `make uv-lock`       | Lock dependencies                       |
| `make uv-update`     | Update dependencies                     |
| `make marimo`        | Launch Marimo notebook server           |

## Code Conventions

- Line length: 88 characters
- Type hints required on all functions
- Conventional commits enforced via pre-commit
- Branch naming: `{initials}/{descriptive-kebab-case}`
- Naming:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `SCREAMING_SNAKE_CASE` for constants

## CI/CD

- **Continuous Integration**: Runs on PR/merge_group
  - Ruff format check
  - Ruff lint
  - ty type check
- **PyPI Release**: Manual trigger with semantic version

## Dependencies

All dependencies pinned to exact versions. Renovate handles updates automatically:

- Minor/patch updates: Auto-merged after 7 days
- Major updates (dev deps): Auto-merged after 14 days
- Security updates: Immediate

## Key Files

| File                                           | Purpose                                     |
| ---------------------------------------------- | ------------------------------------------- |
| `pyproject.toml`                               | Project config, dependencies, tool settings |
| `.pre-commit-config.yaml`                      | Pre-commit hooks configuration              |
| `Makefile`                                     | Development commands                        |
| `renovate.json`                                | Dependency update automation                |
| `.github/workflows/continuous-integration.yml` | CI workflow                                 |
| `.github/workflows/pypi-release.yml`           | PyPI release workflow                       |
