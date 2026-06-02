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

_GDAL_NUGET_URL = (
    'https://api.nuget.org/v3-flatcontainer/maxrev.gdal.windowsruntime.minimal/3.3.3.110'
    '/maxrev.gdal.windowsruntime.minimal.3.3.3.110.nupkg'
)
_NON_GDAL_DLLS = frozenset({
    'ParquetSharpNative.dll', 'SDL2.dll', 'WebView2Loader.dll',
    'duckdb.dll', 'e_sqlite3.dll', 'libSkiaSharp.dll', 'libveldrid-spirv.dll',
})


def _fetch_gdal(gdal_dir: pathlib.Path) -> None:
    """Download GDAL native DLLs from NuGet if not already present."""
    import tempfile
    import urllib.request
    import zipfile

    marker = gdal_dir / '.gdal_fetched'
    if marker.exists():
        return

    gdal_dir.mkdir(parents=True, exist_ok=True)
    _logger.info('GDAL native DLLs not found — downloading from NuGet...')

    try:
        with tempfile.NamedTemporaryFile(suffix='.nupkg', delete=False) as tmp:
            urllib.request.urlretrieve(_GDAL_NUGET_URL, tmp.name)
            tmp_path = pathlib.Path(tmp.name)

        native_prefix = 'runtimes/win-x64/native/'
        with zipfile.ZipFile(tmp_path) as zf:
            for member in zf.namelist():
                if not member.startswith(native_prefix):
                    continue
                rel = member[len(native_prefix):]
                if not rel or rel.endswith('/'):
                    continue
                if pathlib.Path(rel).name in _NON_GDAL_DLLS:
                    continue
                target = gdal_dir / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as src, open(target, 'wb') as dst:
                    dst.write(src.read())

        tmp_path.unlink(missing_ok=True)
        marker.touch()
        _logger.info('GDAL native DLLs downloaded successfully.')
    except Exception as exc:
        _logger.warning('Failed to download GDAL native DLLs: %s: %s', type(exc).__name__, exc)
        if not (gdal_dir / 'osr_wrap.dll').exists():
            raise RuntimeError(
                f"GDAL native DLLs are missing from {gdal_dir} and could not be downloaded automatically. "
                "Run `invoke gdal.fetch` manually to populate them, or install via the PyPI wheel."
            ) from exc


def _configure(gdal_dir: pathlib.Path) -> None:
    """Register gdal_dir on the Windows DLL search path and set GDAL env vars."""
    gdal_dir_exists = gdal_dir.is_dir()
    if sys.platform == "win32":
        if gdal_dir_exists:
            gdal_dir_str = str(gdal_dir)
            # Add to PATH so .NET Core P/Invoke (LoadLibraryExW) can find the DLLs.
            # os.add_dll_directory() alone is insufficient — it only affects
            # LoadLibraryEx with LOAD_LIBRARY_SEARCH_USER_DIRS, which the CLR does not use.
            path_dirs = os.environ.get("PATH", "").split(os.pathsep)
            if gdal_dir_str not in path_dirs:
                os.environ["PATH"] = gdal_dir_str + os.pathsep + os.environ.get("PATH", "")
            # Also call add_dll_directory for Python extension modules (Python 3.8+)
            if sys.version_info >= (3, 8):
                cookie = os.add_dll_directory(gdal_dir_str)
                _dll_dir_cookies.append(cookie)
            _logger.debug(f"Registered GDAL DLL directory: {gdal_dir}")
        else:
            _logger.warning(f"gdal dir not found at {gdal_dir} — "
                            f"DLLs not registered; copy native files per _native/gdal/README.md")

    proj_dir = gdal_dir / "maxrev.gdal.core.libshared"
    if (proj_dir / "proj.db").exists():
        os.environ["PROJ_LIB"] = str(proj_dir)
        _logger.debug(f"PROJ_LIB={proj_dir}")
    else:
        _logger.debug(f"Skipped PROJ_LIB — proj.db not found in {proj_dir}")

    gdal_data_dir = gdal_dir / "gdal-data"
    if gdal_data_dir.is_dir():
        os.environ["GDAL_DATA"] = str(gdal_data_dir)
        _logger.debug(f"GDAL_DATA={gdal_data_dir}")
    else:
        _logger.debug(f"Skipped GDAL_DATA — {gdal_data_dir} not found")


def bootstrap() -> None:
    """Bootstrap the GDAL native runtime. Safe to call multiple times."""
    global _initialized
    if _initialized:
        return
    _initialized = True

    gdal_dir = pathlib.Path(__file__).parent / "gdal"
    _logger.debug(f"Bootstrapping GDAL from {gdal_dir}")
    if sys.platform == "win32":
        _fetch_gdal(gdal_dir)
    _configure(gdal_dir)


bootstrap()
