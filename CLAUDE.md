# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

The `orchid` Python package is the Python API for Orchid (a mark of KAPPA), a fracture diagnostics application. It exposes Orchid's .NET assemblies to Python via `pythonnet`/`clr`. The package is published to PyPI as `orchid-python-api`.

## Development Environment

Uses `poetry` for dependency management. Python 3.10–3.12 required.

```powershell
poetry install          # create/update virtualenv with all deps
poetry shell            # activate the virtualenv
```

## Common Commands

```powershell
# Tests
pytest -m "not slow"    # unit tests only
pytest -m "slow"        # benchmark tests only
pytest                  # all tests

# Run a single test file
pytest tests/test_configuration.py

# Acceptance/feature tests (behave)
behave features/

# Package a distribution
invoke poetry.package

# List all invoke tasks
invoke --list
```

## Architecture

The package has a layered structure:

1. **Public API layer** (`orchid/__init__.py`, `orchid/core.py`): Exports `load_project`, `save_project`, and helper constants/functions. Entry point for all users.

2. **Domain object adapters** (`native_*_adapter.py`): Each adapter wraps a .NET domain object (well, stage, monitor, trajectory, treatment curve, etc.) and exposes it as a Python class. For example, `NativeWellAdapter` wraps the .NET `IWell` interface.

3. **Searchable collections** (`searchable_*.py`): Provide `find_by_name`, `find_by_display_name`, `find_by_object_id`, `find()`, and iteration over domain objects. Used by `Project` to expose wells, stages, data frames, etc.

4. **.NET interop layer** (`dot_net.py`, `dot_net_dom_access.py`, `net_*.py`): Handles `pythonnet`/`clr` loading, .NET type conversions (dates, quantities, enumerables). `IdentifiedDotNetAdapter` is the base class for all adapters.

5. **Configuration** (`configuration.py`): Resolves Orchid installation path via fallback → file (`~/.orchid/python_api.yaml`) → environment variable (`ORCHID_ROOT`). Same layering for training data (`ORCHID_TRAINING_DATA`).

6. **GDAL bootstrapping** (`orchid/_native/`): Registers native GDAL DLLs before `pythonnet` loads. The `tasks.py` `fetch_gdal` task downloads the NuGet package.

### Key Files

- `orchid/core.py` — `load_project()` / `save_project()` implementations
- `orchid/project.py` — `Project` class; top-level domain object
- `orchid/project_store.py` — loads/saves `.ifrac` files via .NET
- `orchid/configuration.py` — config resolution with debug logging
- `tasks.py` — `invoke` tasks for packaging, virtualenv management, GDAL fetch
- `features/` — BDD acceptance tests using `behave`
- `tests/` — unit tests using `pytest` + `pyhamcrest`
- `benchmark_tests/` — slow benchmark tests (marked `@pytest.mark.slow`)

## Runtime Requirements

The package requires a licensed Orchid installation on the workstation. It will not import without it. Configure via:

- **Environment variable**: `ORCHID_ROOT` → path to `PythonApiLibs` directory
- **Config file**: `~/.orchid/python_api.yaml` with `orchid.root` key
- **Fallback**: `%ProgramFiles%\Reveal Energy Services\Orchid\Orchid-<version>`

Debug configuration by running in Python REPL:
```python
import logging; logging.basicConfig(level=logging.DEBUG)
import orchid
```

## Two-Repository Setup

Source lives in both Azure DevOps (`reveal-energy` remote) and GitHub (`origin` remote). The `develop` and `master` branches must be kept in sync between both remotes after completing PRs and releases. See `README-dev.md` for the sync procedure.

## Version Management

When bumping the version, update all three locations:
1. `orchid/VERSION`
2. `pyproject.toml` (`version` key)
3. `ReleaseNotes.md`
4. `docs/conf.py` (`release` value)
