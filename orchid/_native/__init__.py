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
    else:
        _logger.debug(f"Skipped DLL registration (platform={sys.platform})")

    proj_dir = gdal_dir / "maxrev.gdal.core.libshared"
    if proj_dir.is_dir():
        os.environ["PROJ_LIB"] = str(proj_dir)
        _logger.debug(f"PROJ_LIB={proj_dir}")
    else:
        _logger.debug(f"Skipped PROJ_LIB — {proj_dir} not found")

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
    _configure(gdal_dir)


bootstrap()
