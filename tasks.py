#
#  Copyright 2017-2021 Reveal Energy Services, Inc 
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

import json
import logging
import os
import pathlib
import shutil

# noinspection PyPackageRequirements
from invoke import task, Collection
# noinspection PyPackageRequirements
import toml


# Commented out for ease of introducing DEBUG logging.
# logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


@task
def setup_build(context, docs=False):
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
        log.debug(f'Removing path, {str(to_remove.resolve())}')
        try:
            try:
                to_remove.unlink(missing_ok=True)
            except TypeError:
                try:
                    if to_remove.is_dir():
                        shutil.rmtree(to_remove)
                    else:
                        to_remove.unlink()
                except FileNotFoundError:
                    # Skip if Python less than 3.8
                    pass
            log.debug(f'Removed path, {str(to_remove.resolve())}')
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
def setup_package(context, skip_source=False, skip_binary=False):
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


def example_notebooks_names():
    """Returns the sequence of example notebook names."""
    example_notebook_stems = ['completion_analysis', 'plot_monitor_curves', 'plot_trajectories', 'plot_treatment']
    result = map(lambda s: pathlib.Path(s).with_suffix('.ipynb'), example_notebook_stems)
    return result


@task
def examples_clean_notebooks(_context, directory='.'):
    """
    Remove all the example notebooks from a specified directory.

    Args:
        _context: The task context (unused).
        directory: The directory from which I remove the example notebooks. (Default: current directory)
    """
    notebook_paths_to_remove = map(lambda n: pathlib.Path(directory).joinpath(n), example_notebooks_names())
    for notebook_path_to_remove in notebook_paths_to_remove:
        notebook_path_to_remove.unlink(missing_ok=True)


@task
def examples_copy_notebooks(_context, target_dir='.'):
    """
    Copy all the example notebooks to a specified directory.

    Args:
        _context: The task context (unused).
        target_dir: The directory into which I copy the example notebooks. (Default: current directory)
    """
    source_files = map(lambda fn: pathlib.Path('./orchid_python_api/examples').joinpath(fn), example_notebooks_names())
    for source_file in source_files:
        shutil.copy2(source_file, target_dir)


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
def pipenv_create_venv(context, dirname='.', python_ver='3.8.7'):
    """
    Create the virtual environment associated with `dirname` (Python interpreter only).
    Args:
        context: The task context.
        dirname (str): The pathname of the directory whose virtual environment is to be created. (Default '.')
        python_ver (str): The version of Python to install in the virtual environment (Default: 3.8.7).
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


@task
def poetry_build(context, skip_source=False, skip_binary=False):
    """
    Package this project for distribution. By default, create *both* a source and binary distribution.

    Args:
        context: The task context (unused).
        skip_source (bool) : Flag set `True` if you wish to *not* building a source distribution.
        skip_binary (bool): Flag set `True` if you wish to *not* building a binary (skip_binary) distribution.
        Note that either `skip_source` or `skip_binary` can be set `True`, but *not* both.
    """
    assert not (skip_source and skip_binary), 'Cannot skip both source and binary.'

    chosen_format = ''
    if skip_source:
        chosen_format = 'wheel'
    elif skip_binary:
        chosen_format = 'sdist'
    format_option = '' if not chosen_format else f'--format={chosen_format}'
    context.run(f'poetry build {format_option}')


@task
def poetry_configure_api_token(context, token, repository='pypi'):
    """
    Set the (PyPI) API token for configured poetry repository.

    Args:
        context: The task context (unused).
        token (str): The generated API token (including  the `pypi` prefix).
        repository (str) : The name of the configured repository (default: `pypi`).
    """
    context.run(f'poetry config pypi-token.{repository} {token}')


@task
def poetry_configure_list(context):
    """
    List the configuration of poetry.

    Args:
        context: The task context (unused).
    """
    context.run('poetry config --list')


@task
def poetry_configure_test_pypi(context):
    """
    Add the test.pypi.org repository to the poetry configuration.

    Args:
        context: The task context (unused).
    """
    context.run('poetry config repositories.test-pypi https://test.pypi.org/legacy/')


@task
def poetry_create_venv(context, dirname='.', python_ver='3.8.7'):
    """
    Create the virtual environment associated with `dirname` (Python interpreter only).
    Args:
        context: The task context.
        dirname (str): The pathname of the directory whose virtual environment is to be created. (Default '.')
        python_ver (str): The version of Python to install in the virtual environment (Default: 3.8.7).
    """
    python_minor_versions = ['37', '38']
    python_exe_relative_paths = [pathlib.Path('Programs').joinpath('Python', f'Python{v}', 'python.exe') for
                                 v in python_minor_versions]
    python_paths = [pathlib.Path(os.environ['LOCALAPPDATA']).joinpath(rp) for rp in python_exe_relative_paths]
    python_option_map = {version: path for version, path in zip(('3.7.7', '3.8.7'), python_paths)}
    python_option = python_option_map.get(python_ver, '')
    with context.cd(dirname):
        context.run(f'poetry env use {python_option}')


@task
def poetry_list_env(context):
    """
    List all the poetry environments.
    Args:
        context: The task context.
    """
    context.run('poetry env list')


@task
def poetry_publish(context, repository):
    """
    Publish the created source and binary distributions to the specified repository.

    Args:
        context: The task context (unused).
        repository (str) : The name of the configured repository (either `pypi` or `test-pypi`).
    """
    # Although the documentation seems to indicate that `pypi` is the alias for PyPI, supplying the string,
    # `pypi` did not work when I tried. (Given the subsequent behavior, I may not have waited long enough.)
    # Consequently, if I supply `pypi` to the task, I invoke `publish` with *no arguments*.
    if repository == 'pypi':
        context.run(f'poetry publish')
    elif repository == 'test-pypi':
        context.run(f'poetry publish --repository={repository}')
    else:
        raise ValueError(f'Unexpected repository, "{repository}." Only "pypi" and "test-pypi" allowed.')


@task
def poetry_remove_venv(context, dirname='.', venv_name=None, python_path=None):
    """
    Remove the virtual environment associated with `dirname`.
    Args:
        context: The task context.
        dirname (str): The optional pathname of the directory whose virtual environment is to be removed.
            (Default '.')
        venv_name (str): The name of the virtual environment to delete (and associated with `dirname`).
        python_path (str): The full path to the python interpreter used to create the environment.
            Note: specify either `venv_name` or `python-path` but not both.
    """
    assert not (venv_name and python_path), "Specify either `venv_name` or `python_path` but not both."

    with context.cd(dirname):
        context.run(f'poetry env remove {venv_name or python_path}')


@task
def poetry_update_version(_context):
    """
    Update the poetry version in `pyproject.toml` to the version stored in orchid/VERSION.

    Args:
        _context: The task context (unused).
    """
    with open('pyproject.toml') as in_stream:
        source_toml = toml.loads(in_stream.read())

    project_slug = source_toml['tool']['poetry']['name'].lower().replace('-', '_').replace(' ', '_')
    # TODO: move version to `orchid_python_api`
    # Use the `packaging` package to handle version parsing correctly
    # Calculate the `orchid` project name from the `project_slug`
    orchid_package_name = project_slug.replace('_python_api', '')
    with open(os.path.join(pathlib.Path(__file__).parent, orchid_package_name, 'VERSION')) as f:
        version_text = f.read().strip()

    target_toml = source_toml.copy()
    target_toml['tool']['poetry']['version'] = version_text

    with open('pyproject.toml', 'w') as out_stream:
        out_stream.write(toml.dumps(target_toml))


# Create and organize namespaces

# Namespace root
ns = Collection()
ns.add_task(clean)
ns.add_task(pipfile_to_poetry)

examples_ns = Collection('examples')
examples_ns.add_task(examples_clean_notebooks, name='clean-notebooks')
examples_ns.add_task(examples_copy_notebooks, name='copy-notebooks')

pipenv_ns = Collection('pipenv')

pipenv_venv_ns = Collection('venv')
pipenv_venv_ns.add_task(pipenv_remove_venv, name='remove')
pipenv_venv_ns.add_task(pipenv_create_venv, name='create')

pipenv_ns.add_collection(pipenv_venv_ns)

poetry_ns = Collection('poetry')
# According to the documentation, aliases should be an iterable of alias names; however, the "build" aliases
# appears neither in listing available tasks nor does `invoke` recognize the name as a sub-task. Finally, if
# I add the alias to the task itself, it *is* handled correctly.
#
# Right now, my best guess as to the cause of the error is line 273 of `collection.py`:
#
#   `self.tasks.alias(self.transform(alias), to=name)`
#
# In this line, `self.tasks` is of type `Lexicon`; however, line 15 of `vendor/lexicon/__init__.py` seems to
# set the attribute to be *aliases*. (Singular in the former case but *plural* in the latter.)
#
# At some time, we need to file a bug and perhaps submit a patch.
poetry_ns.add_task(poetry_build, name='package', aliases=('build',))
poetry_ns.add_task(poetry_publish, name='publish')
poetry_ns.add_task(poetry_update_version, name='update-ver')

poetry_config_ns = Collection('config')
poetry_config_ns.add_task(poetry_configure_api_token, name='api-token')
poetry_config_ns.add_task(poetry_configure_list, name='list')
poetry_config_ns.add_task(poetry_configure_test_pypi, name='test-pypi')
poetry_ns.add_collection(poetry_config_ns)

poetry_env_ns = Collection('env')
poetry_env_ns.add_task(poetry_list_env, name='list')
poetry_ns.add_collection(poetry_env_ns)

setup_ns = Collection('setup')
setup_ns.add_task(setup_build, name='build')
setup_ns.add_task(setup_package, name='package')

poetry_venv_ns = Collection('venv')
poetry_venv_ns.add_task(poetry_create_venv, name='create')
poetry_venv_ns.add_task(poetry_remove_venv, name='remove')
poetry_ns.add_collection(poetry_venv_ns)

ns.add_collection(examples_ns)
ns.add_collection(pipenv_ns)
ns.add_collection(poetry_ns)
ns.add_collection(poetry_venv_ns)
ns.add_collection(setup_ns)
