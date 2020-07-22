#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import json
import logging
import pathlib
import shutil
import sys

# noinspection PyPackageRequirements
from invoke import task, Collection
import toml


# logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


@task
def build(context, docs=False):
    """
    Build this project, optionally building the project documentation.

    Args:
        context: The task context (unused).
        docs (bool): Flag set `True` if you wish to build the project documentation.
    """
    context.run("python setup.py build")
    if docs:
        context.run("sphinx-build docs docs/_build")


# Remember: the `invoke` package does not (yet) support parameter annotations.
def remove_files_matching_pattern(glob_pattern):
    """
    Remove all files matching (using glob) `glob_pattern`.

    If this function cannot remove a file because of on instance of `OSError`, it prints a message instead of
    failing. Additionally, if a file initially found by our search is subsequently not fund, print no message
    and continue processing.

    Args:
        glob_pattern (str): The glob pattern that identifies files to remove.
    """

    root_dir = pathlib.Path('.')
    log.debug(f'root_dir={str(root_dir.resolve())}')
    for to_remove in root_dir.glob(glob_pattern):
        try:
            # Not until 3.8
            # to_remove.unlink(missing_ok=True)
            log.debug(f'Removing path, {str(to_remove.resolve())}')
            if to_remove.is_dir():
                shutil.rmtree(to_remove)
            else:
                to_remove.unlink()
            log.debug(f'Removed path, {str(to_remove.resolve())}')
        except FileNotFoundError:
            # Skip if Python less than 3.8
            pass
        except OSError as ose:
            print(f'Error removing path, {str(to_remove.resolve())}: {ose}')


@task
def clean(_context, docs=False, bytecode=False, extra=''):
    """
    Remove the specified artifacts for this project.

    Args:
        _context: The task context (unused)
        docs (bool): Flag set `True` if you wish to clean the generated documentation.
        bytecode (bool): Flag set `True` if you wish to clean the generated python byte-code files.
        extra (str): A glob pattern identifying additional files to remove.
    """
    patterns = ['build', 'dist']
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/*.pyc')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        remove_files_matching_pattern(pattern)


@task
def package(context, skip_source=False, skip_binary=False):
    """
    Package this project for distribution. By default, create *both* a source and binary distribution.

    Args:
        context: The task context (unused).
        skip_source (bool) : Flag set `True` if you wish to *not* building a source distribution.
        skip_binary (bool): Flag set `True` if you wish to *not* building a binary (skip_binary) distribution.
    """
    source_option = 'sdist' if not skip_source else ''
    wheel_option = 'bdist_wheel' if not skip_binary else ''
    context.run(f'python setup.py {source_option} {wheel_option} ')


@task
def pipfile_to_poetry(_context):
    """
    Print `poetry` commands to add Pipfile dependencies to the poetry project file (`pyproject.toml`).
    Args:
        _context: The task context (unused).
    """
    pipfile = toml.load(pathlib.Path("Pipfile").open())
    pipfile_lock = json.load(pathlib.Path("Pipfile.lock").open())

    for required_package in pipfile["packages"]:
        try:
            version = pipfile_lock["default"][str(required_package)]["version"]
            print(f"poetry add {required_package}={version.replace('==', '')}")
        except KeyError:
            pass

    for dev_package in pipfile["dev-packages"]:
        try:
            version = pipfile_lock["develop"][str(dev_package)]["version"]
            print(f"poetry add --dev {dev_package}={version.replace('==', '')}")
        except KeyError:
            pass


@task
def pipenv_create_venv(context, dirname='.', python_ver='3.7.7'):
    """
    Create the virtual environment associated with `dirname` (Python interpreter only).
    Args:
        context: The task context.
        dirname (str): The pathname of the directory whose virtual environment is to be removed. (Default '.')
        python_ver (str): The version of Python to install in the virtual environment (Default: 3.7.7).
    """
    with context.cd(dirname):
        context.run(f'pipenv install --python={python_ver}')


@task
def pipenv_remove_venv(context, dirname='.'):
    """
    Remove the virtual environment associated with `dirname`.
    Args:
        context: The task context.
        dirname: The optional pathname of the directory whose virtual environment is to be removed. (Default '.')
    """
    with context.cd(dirname):
        context.run('pipenv --rm')
        context.run('del Pipfile Pipfile.lock')


# Create and organize namespaces

# Namespace root
ns = Collection()
ns.add_task(build)
ns.add_task(clean)
ns.add_task(package)
ns.add_task(pipfile_to_poetry)

pipenv_venv_ns = Collection('pipenv-venv')
pipenv_venv_ns.add_task(pipenv_remove_venv, name='remove')
pipenv_venv_ns.add_task(pipenv_create_venv, name='create')

ns.add_collection(pipenv_venv_ns)
