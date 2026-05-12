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
    if sys.platform == "win32" and sys.version_info >= (3, 8):
        if gdal_dir_exists:
            cookie = os.add_dll_directory(str(gdal_dir))
            _dll_dir_cookies.append(cookie)
            _logger.debug(f"Added DLL directory: {gdal_dir}")
        else:
            _logger.warning(f"gdal dir not found at {gdal_dir} — "
                            f"DLLs not registered; copy native files per _native/gdal/README.md")
    else:
        _logger.debug(f"Skipped add_dll_directory (platform={sys.platform})")

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
