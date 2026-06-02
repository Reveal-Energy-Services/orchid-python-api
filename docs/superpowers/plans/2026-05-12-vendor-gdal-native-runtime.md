# Vendor GDAL Native Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Vendor MaxRev.Gdal.Core 3.3.3.120 native DLLs into the `orchid` package so the API resolves `osr_wrap.dll` (and related GDAL DLLs) without relying on external DLL folders on the Windows search path.

**Architecture:** A new `orchid/_native/` sub-package holds an idempotent bootstrapper (`__init__.py`) that runs as the very first action in `orchid/__init__.py` — before `pythonnet.load()` — registering the DLL directory via `os.add_dll_directory()` and setting `GDAL_DATA`/`PROJ_LIB`. A `gdal/` subdirectory (manually populated from the NuGet package) holds the native files. `orchid/dot_net.py` gains a `configure_gdal()` helper for the managed-side `GdalBase.ConfigureAll()` call.

**Tech Stack:** Python 3.10, pythonnet 3.0.3, Poetry, `os.add_dll_directory` (Win32 Python 3.8+), MaxRev.Gdal.Core 3.3.3.120 NuGet package

---

## File Map

| Action | Path | Purpose |
|--------|------|---------|
| Create | `orchid/_native/__init__.py` | Idempotent GDAL bootstrapper |
| Create | `orchid/_native/gdal/README.md` | Instructions for populating the native DLL directory |
| Create | `orchid/_native/gdal/.gitkeep` | Keeps `gdal/` tracked with no DLLs committed |
| Create | `orchid/_native/gdal/gdalplugins/.gitkeep` | Keeps `gdalplugins/` tracked |
| Create | `orchid/_native/gdal/maxrev.gdal.core.libshared/.gitkeep` | Keeps `maxrev.gdal.core.libshared/` tracked |
| Create | `tests/test_gdal_bootstrap.py` | Unit tests for the bootstrapper |
| Modify | `orchid/__init__.py` | Add `from . import _native` at line 19, before `import pythonnet` |
| Modify | `orchid/dot_net.py` | Add `configure_gdal()` and call it in `prepare_imports()` |
| Modify | `pyproject.toml` | Add `orchid/_native/**/*` to the `include` list |
| Modify | `.gitignore` | Add patterns to exclude DLLs from the `_native/gdal/` tree |

---

## Task 1: Create `_native/gdal/` directory structure and README

**Files:**
- Create: `orchid/_native/gdal/.gitkeep`
- Create: `orchid/_native/gdal/gdalplugins/.gitkeep`
- Create: `orchid/_native/gdal/maxrev.gdal.core.libshared/.gitkeep`
- Create: `orchid/_native/gdal/README.md`

- [ ] **Step 1: Create the directory skeleton with `.gitkeep` files**

Run these commands:
```
mkdir -p orchid/_native/gdal/gdalplugins
mkdir -p orchid/_native/gdal/maxrev.gdal.core.libshared
touch orchid/_native/gdal/.gitkeep
touch orchid/_native/gdal/gdalplugins/.gitkeep
touch orchid/_native/gdal/maxrev.gdal.core.libshared/.gitkeep
```

- [ ] **Step 2: Write `orchid/_native/gdal/README.md`**

```markdown
# GDAL Native Runtime

This directory must be populated with native DLLs from the
**MaxRev.Gdal.Core 3.3.3.120** NuGet package before using this package
with .NET assemblies that depend on GDAL 3.3.3.

## How to populate

1. Download or locate the NuGet package. The easiest source is the Orchid
   .NET build output:

       D:\source\Orchid\Orchid\Orchid.Application\bin\x64\Debug\runtimes\win-x64\native\

2. Copy the entire contents of that `native\` folder into **this** directory:

   - All `*.dll` files (gdal303.dll, osr_wrap.dll, gdal_wrap.dll, etc.)
   - The `gdalplugins\` subfolder (contains gdal_HDF4.dll, gdal_HDF5.dll)
   - The `maxrev.gdal.core.libshared\` subfolder (contains proj.db)

   Resulting layout:
   ```
   orchid/_native/gdal/
     gdal303.dll
     osr_wrap.dll
     gdal_wrap.dll
     gdalconst_wrap.dll
     ogr_wrap.dll
     ... (all other *.dll files)
     gdalplugins/
       gdal_HDF4.dll
       gdal_HDF5.dll
     maxrev.gdal.core.libshared/
       proj.db
   ```

3. If the NuGet package also contains a `gdal-data\` folder, copy that here
   too. The bootstrapper will set `GDAL_DATA` automatically if it finds
   `gdal/_native/gdal/gdal-data/` at runtime.

## Environment variables set by the bootstrapper

| Variable   | Value                                                  |
|------------|--------------------------------------------------------|
| GDAL_DATA  | `<this dir>/gdal-data` (only if that subdir exists)   |
| PROJ_LIB   | `<this dir>/maxrev.gdal.core.libshared`               |

## Why these DLLs are not committed

The native DLLs total ~100 MB and are Windows/architecture-specific.
They are excluded by `.gitignore`. Once the vendor strategy is confirmed
working, the team will decide on a long-term distribution mechanism
(e.g., fetching from the NuGet package at build time).
```

- [ ] **Step 3: Verify the directories exist**

Run: `ls orchid/_native/gdal/`
Expected: see `README.md`, `.gitkeep`, `gdalplugins/`, `maxrev.gdal.core.libshared/`

---

## Task 2: Write failing tests for the bootstrapper

**Files:**
- Create: `tests/test_gdal_bootstrap.py`

- [ ] **Step 1: Write the test file**

```python
#  Copyright (c) 2017-2026 KAPPA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# This file is part of Orchid and related technologies.
#

import os
import pathlib
import sys

import pytest


def test_configure_sets_proj_lib_when_libshared_exists(tmp_path, monkeypatch):
    fake_gdal = tmp_path / "gdal"
    fake_gdal.mkdir()
    (fake_gdal / "maxrev.gdal.core.libshared").mkdir()

    monkeypatch.delenv("PROJ_LIB", raising=False)

    from orchid._native import _configure
    _configure(fake_gdal)

    assert os.environ["PROJ_LIB"] == str(fake_gdal / "maxrev.gdal.core.libshared")


def test_configure_sets_gdal_data_when_dir_exists(tmp_path, monkeypatch):
    fake_gdal = tmp_path / "gdal"
    fake_gdal.mkdir()
    (fake_gdal / "gdal-data").mkdir()

    monkeypatch.delenv("GDAL_DATA", raising=False)

    from orchid._native import _configure
    _configure(fake_gdal)

    assert os.environ["GDAL_DATA"] == str(fake_gdal / "gdal-data")


def test_configure_skips_gdal_data_when_dir_missing(tmp_path, monkeypatch):
    fake_gdal = tmp_path / "gdal"
    fake_gdal.mkdir()

    monkeypatch.delenv("GDAL_DATA", raising=False)

    from orchid._native import _configure
    _configure(fake_gdal)

    assert "GDAL_DATA" not in os.environ


def test_configure_skips_proj_lib_when_libshared_missing(tmp_path, monkeypatch):
    fake_gdal = tmp_path / "gdal"
    fake_gdal.mkdir()

    monkeypatch.delenv("PROJ_LIB", raising=False)

    from orchid._native import _configure
    _configure(fake_gdal)

    assert "PROJ_LIB" not in os.environ


def test_bootstrap_is_idempotent(monkeypatch):
    import orchid._native as nat
    monkeypatch.setattr(nat, "_initialized", False)
    nat.bootstrap()
    first_proj = os.environ.get("PROJ_LIB")
    nat.bootstrap()
    assert os.environ.get("PROJ_LIB") == first_proj
```

- [ ] **Step 2: Run the tests and confirm they fail with ImportError (function not defined yet)**

Run: `pytest tests/test_gdal_bootstrap.py -v`
Expected: ERRORS — `ImportError: cannot import name '_configure' from 'orchid._native'`

---

## Task 3: Write `orchid/_native/__init__.py`

**Files:**
- Create: `orchid/_native/__init__.py`

- [ ] **Step 1: Write the bootstrapper**

```python
#  Copyright (c) 2017-2026 KAPPA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# This file is part of Orchid and related technologies.
#

import logging
import os
import pathlib
import sys

_logger = logging.getLogger(__name__)

_initialized = False
_dll_dir_cookies: list = []


def _configure(gdal_dir: pathlib.Path) -> None:
    """Register gdal_dir on the Windows DLL search path and set GDAL env vars."""
    if sys.platform == "win32" and sys.version_info >= (3, 8) and gdal_dir.is_dir():
        cookie = os.add_dll_directory(str(gdal_dir))
        _dll_dir_cookies.append(cookie)
        _logger.debug(f"orchid._native: added DLL directory {gdal_dir}")
    else:
        _logger.debug(f"orchid._native: skipped add_dll_directory "
                      f"(platform={sys.platform}, dir_exists={gdal_dir.is_dir()})")

    proj_dir = gdal_dir / "maxrev.gdal.core.libshared"
    if proj_dir.is_dir():
        os.environ["PROJ_LIB"] = str(proj_dir)
        _logger.debug(f"orchid._native: PROJ_LIB={proj_dir}")
    else:
        _logger.debug(f"orchid._native: skipped PROJ_LIB — {proj_dir} not found")

    gdal_data_dir = gdal_dir / "gdal-data"
    if gdal_data_dir.is_dir():
        os.environ["GDAL_DATA"] = str(gdal_data_dir)
        _logger.debug(f"orchid._native: GDAL_DATA={gdal_data_dir}")
    else:
        _logger.debug(f"orchid._native: skipped GDAL_DATA — {gdal_data_dir} not found")


def bootstrap() -> None:
    """Bootstrap the GDAL native runtime. Safe to call multiple times."""
    global _initialized
    if _initialized:
        return
    _initialized = True

    gdal_dir = pathlib.Path(__file__).parent / "gdal"
    _logger.debug(f"orchid._native: bootstrapping GDAL from {gdal_dir}")
    _configure(gdal_dir)


bootstrap()
```

- [ ] **Step 2: Run the tests and confirm they pass**

Run: `pytest tests/test_gdal_bootstrap.py -v`
Expected: 5 PASSED

- [ ] **Step 3: Commit**

```bash
git add orchid/_native/__init__.py orchid/_native/gdal/ tests/test_gdal_bootstrap.py
git commit -m "feat: add GDAL native runtime bootstrapper with vendored DLL directory"
```

---

## Task 4: Update `orchid/__init__.py` to run the bootstrap before pythonnet

**Files:**
- Modify: `orchid/__init__.py`

Current content (lines 19–24):
```python
# Load the appropriate runtime **before** executing `import clr`
import pythonnet
pythonnet.load('coreclr')

from .dot_net import prepare_imports
prepare_imports()
```

- [ ] **Step 1: Add the `_native` import at the very top of `orchid/__init__.py`, before the copyright block ends and before `import pythonnet`**

Insert `from . import _native  # registers GDAL DLL directory before pythonnet loads` on the line immediately before the `# Load the appropriate runtime` comment. The file currently has the copyright header ending at line 16, then blank lines, then the pythonnet block. Insert after line 17 (the blank line after the copyright).

The modified section should read:
```python
# Must run before pythonnet loads to register GDAL native DLL directory
from . import _native

# Load the appropriate runtime **before** executing `import clr`
import pythonnet
pythonnet.load('coreclr')

from .dot_net import prepare_imports
prepare_imports()
```

- [ ] **Step 2: Verify the import order is correct**

Read `orchid/__init__.py` and confirm `from . import _native` is the first non-comment, non-blank line of executable code in the file.

- [ ] **Step 3: Smoke-test that the import doesn't crash (no .NET needed)**

Run: `python -c "import logging; logging.basicConfig(level=logging.DEBUG); import sys; sys.path.insert(0, '.'); import orchid._native"`
Expected: no exception; DEBUG lines like `orchid._native: bootstrapping GDAL from ...`

Note: `import orchid` will fail here without a full Orchid installation — only test `orchid._native` directly.

- [ ] **Step 4: Commit**

```bash
git add orchid/__init__.py
git commit -m "feat: bootstrap GDAL native runtime before pythonnet in orchid.__init__"
```

---

## Task 5: Add `configure_gdal()` to `orchid/dot_net.py`

This calls `GdalBase.ConfigureAll()` from the managed side after Orchid assemblies are loaded. This step requires the full .NET environment to test.

**Files:**
- Modify: `orchid/dot_net.py`

- [ ] **Step 1: Add `logging` import and `configure_gdal()` function to `dot_net.py`**

Add `import logging` after the existing `import os` on line 19.
Add `_logger = logging.getLogger(__name__)` after the existing imports (after the `import clr` line).

Then add the new function after `add_orchid_assemblies()`:

```python
def configure_gdal() -> None:
    """Call GdalBase.ConfigureAll() from MaxRev.Gdal.Core if the assembly is available."""
    try:
        clr.AddReference('MaxRev.Gdal.Core')
        # noinspection PyUnresolvedReferences
        from MaxRev.Gdal.Core import GdalBase
        GdalBase.ConfigureAll()
        _logger.debug('orchid.dot_net: GdalBase.ConfigureAll() completed')
    except Exception as exc:
        _logger.warning(f'orchid.dot_net: GdalBase.ConfigureAll() skipped: {exc}')
```

- [ ] **Step 2: Call `configure_gdal()` inside `prepare_imports()`, after `add_orchid_assemblies()`**

Current `prepare_imports()`:
```python
def prepare_imports() -> None:
    with sac.ScriptAdapterContext():
        orchid.dot_net.add_orchid_assemblies()
```

Updated `prepare_imports()`:
```python
def prepare_imports() -> None:
    with sac.ScriptAdapterContext():
        orchid.dot_net.add_orchid_assemblies()
    configure_gdal()
```

Note: `configure_gdal()` is intentionally outside the `ScriptAdapterContext` because `GdalBase.ConfigureAll()` initializes global GDAL state that should not be torn down when the context exits.

- [ ] **Step 3: Verify `dot_net.py` is syntactically correct**

Run: `python -c "import ast; ast.parse(open('orchid/dot_net.py').read()); print('OK')"`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add orchid/dot_net.py
git commit -m "feat: call GdalBase.ConfigureAll() after loading Orchid assemblies"
```

---

## Task 6: Update `pyproject.toml` to include `_native/**/*`

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add the `_native` glob to the `include` list**

Current `include` block (lines 38–53):
```toml
include=[
    "LICENSE",
    "ReleaseNotes.md",
    "orchid/*.py",
    "orchid/VERSION",
    "orchid_python_api/examples/*.ipynb",
    "orchid_python_api/examples/*.py",
    "orchid_python_api/examples/low_level/*.ipynb",
    "orchid_python_api/examples/low_level/*.py",
    "orchid_python_api/tutorials/*.ipynb",
    "orchid_python_api/tutorials/*.py",
    "copy_orchid_examples.py",
    "copy_orchid_low_level_examples.py",
    "copy_orchid_manual_examples.py",
    "copy_orchid_tutorials.py",
]
```

Add these two lines after `"orchid/VERSION",`:
```toml
    "orchid/_native/*.py",
    "orchid/_native/gdal/**/*",
```

- [ ] **Step 2: Verify the TOML is syntactically valid**

Run: `python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb')); print('OK')" 2>/dev/null || python -c "import tomli; tomli.load(open('pyproject.toml', 'rb')); print('OK')"`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "build: include orchid/_native package data in sdist and wheel"
```

---

## Task 7: Update `.gitignore` to exclude native DLLs

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Append GDAL vendor exclusion block to `.gitignore`**

Add the following block at the end of `.gitignore`:
```gitignore

# Vendored GDAL native DLLs (populate manually from MaxRev.Gdal.Core NuGet package)
# Keep directory structure (.gitkeep files) but exclude the actual binaries
orchid/_native/gdal/*.dll
orchid/_native/gdal/**/*.dll
orchid/_native/gdal/maxrev.gdal.core.libshared/proj.db
```

- [ ] **Step 2: Verify `.gitkeep` files are still tracked despite the ignore rules**

Run: `git check-ignore -v orchid/_native/gdal/.gitkeep`
Expected: no output (meaning it is NOT ignored — it will be tracked)

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: gitignore vendored GDAL native DLLs in _native/gdal/"
```

---

## Manual Steps to Test End-to-End

After all tasks are complete, here is the exact sequence to copy the MaxRev native files and validate the fix:

```
# 1. Copy all DLLs and subdirectories from the Orchid build output native folder:
xcopy /E /I /Y "D:\source\Orchid\Orchid\Orchid.Application\bin\x64\Debug\runtimes\win-x64\native\" "D:\source\PythonApi\orchid\_native\gdal\"

# 2. Verify the key DLL is now present:
ls orchid/_native/gdal/osr_wrap.dll

# 3. Verify proj.db is in place:
ls orchid/_native/gdal/maxrev.gdal.core.libshared/proj.db

# 4. Test the bootstrapper in isolation (no full .NET environment needed):
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
import sys
sys.path.insert(0, '.')
import orchid._native
"
# Expected: DEBUG lines showing DLL directory added and PROJ_LIB set

# 5. Full integration test (requires ORCHID_ROOT configured):
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
import orchid
print('orchid imported OK')
"
# Expected: no DllNotFoundException; 'orchid imported OK'
```

---

## Self-Review Checklist

**Spec coverage:**
- [x] Step 1 — project structure inspected (done before plan; findings embedded above)
- [x] Step 2 — `_native/gdal/` directory + README
- [x] Step 3 — pyproject.toml `include` update (Task 6)
- [x] Step 4 — native bootstrapper with `add_dll_directory`, env vars, idempotency, logging (`_native/__init__.py`)
- [x] Step 5 — bootstrap imported at top of `orchid/__init__.py` before pythonnet (Task 4)
- [x] Step 6 — `configure_gdal()` helper calling `GdalBase.ConfigureAll()` (Task 5)
- [x] Step 7 — `.gitignore` entries for DLLs (Task 7)
- [x] Step 8 — manual copy steps provided at end of plan

**Type/name consistency:**
- `_configure(gdal_dir)` defined in Task 3, tested in Task 2 — consistent
- `bootstrap()` defined in Task 3, tested in Task 2 — consistent
- `configure_gdal()` defined and called in Task 5 — consistent
- `_initialized`, `_dll_dir_cookies` defined in Task 3, referenced in Task 2 tests — consistent
