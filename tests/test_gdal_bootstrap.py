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
    monkeypatch.delenv("PROJ_LIB", raising=False)
    monkeypatch.delenv("GDAL_DATA", raising=False)
    monkeypatch.setattr(nat, "_initialized", False)
    nat.bootstrap()
    assert nat._initialized is True
    first_proj = os.environ.get("PROJ_LIB")
    nat.bootstrap()
    assert nat._initialized is True
    assert os.environ.get("PROJ_LIB") == first_proj
