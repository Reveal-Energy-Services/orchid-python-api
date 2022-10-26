## Introduction 

(This document targets people *developing* the Orchid Python. If you plan to simply use the API, look at 
[README](./README.md) instead.)

This project defines the implementation of the Python API for Orchid*.

Specifically, the `orchid` package makes Orchid features available to Python applications and to the Python REPL.

(*Orchid is a mark of Reveal Energy Services, Inc.)

## Caution Multiple Repositories

The Orchid Python API is different from other products in terms of its source code. The source code is present is Azure
DevOps but is also available from GitHub. The benefit of this dichotomy is that consumers of the Python API can access 
the source code without access to our internal repositories. The difficulty with this choice is that developers must
coordinate changes between these two repositories. Consequently, working with these two repositories are similar to
forking a GitHub repository and working with both `origin` (the forked repository) and the original repository (often
called the `upstream` repository). The main synchronization point of these two repositories are releases. For more
details, read the section [Managing multiple code repositories](#managing-multiple-code-repositories).

## Examples

### High-level examples

This project includes eight scripts and six notebooks in the `examples` directory of the `orchid-python-api` package:

| Name                            | Demonstrates...                                                                     |
|---------------------------------|-------------------------------------------------------------------------------------|
| `completion_analysis.ipynb`     | A detailed analysis of the completion performed on two different wells in a project |
| `plot_trajectories.ipynb`       | Plotting the well trajectories for a project                                        |
| `plot_time_series.ipynb`        | Plotting the monitor curves for a project                                           |
| `plot_treatment.ipynb`          | Plotting the treatment curves for a specific stage of a well in a project           | 
| `search_data_frames.ipynb`      | Searching object collections and our data frame access                              | 
| `volume_2_first_response.ipynb` | Using derivatives to calculate the fluid volume pumped before the first response    | 

Six of the eight scripts contain the same code as the notebooks but run either at the command line or in a REPL. The
last two scripts:

| Name                            | Demonstrates using the high-level Python API to...                               |
|---------------------------------|----------------------------------------------------------------------------------|
| `stage_qc_results.py`           | Read and write QC results for a stage. (Replaces low-level `stage_qc_status.py`) |
| `change_stage_times.py`         | Change the start and stop times (the time range) of a stage                      |
| `add_stages.py`                 | Add one or more stages to a well. (Improvement over `add_stages_low.py`)         |

### Low-level examples

In addition, this project includes five scripts and a notebook in the `examples/low_level` directory of the
`orchid-python-api` package:

| Name                                      | Demonstrates...                                                  |
|-------------------------------------------|------------------------------------------------------------------|
| `auto_pick.py`                            | Automatically pick observations and save them to an .ifrac file  |
| `auto_pick_and_create_stage_attribute.py` | Create and save stage attributes                                 |
| `auto_pick_iterate_example.py`            | Use iteration to find visible stages instead of .NET method      |
| `monitor_time_series.py`                  | Find high-level time series from a low-level monitor time series | 
| `add_stages_low.py`                       | Adds newly created stages to a well of a project                 | 
| `multi_picking_events.py`                 | Creates and adds a number of multi-picking events                |

The notebook, `auto_pick.ipynb` contain the same code as the script, `auto_pick.py`, but runs in a Jupyter
notebook.

To use these examples:

- You may need to
  [configure the Orchid Python API to find the Orchid installation](#configure-the-orchid-python-api)
- You **must**
  [configure the Orchid Python API to find the Orchid training data](#configure-the-orchid-training-data)
- You may need to [view the Orchid API configuration details](#view-orchid-configuration-details)
- You may want to invoke the command, `copy_orchid_examples`

  This command copies the example files into an optionally specified (virtual environment) directory. (The
  default destination is your current working directory.) Note that this command is a command-line script
  that runs in a console or terminal. Additionally, this command supports a help flag, `-h` or `--help`, to
  provide you with help on running this command.

More detailed instructions for running the examples can be found at:

- [Run development Orchid high-level examples](#run-development-orchid-high-level-examples)
- [Run installed Orchid high-level examples](#run-installed-orchid-high-level-examples)

## Tutorials

Additionally, this project includes one notebook and one script in the `tutorials` directory of the
`orchid-python-api` package:

- `dom_navigation_tutorial.ipynb`
- `dom_navigation_tutorial.py`

The notebook, `dom_navigation_tutorial.ipynb`, demonstrates using the Orchid Python API class,
`SearchableProjectObjects`, to navigate a project. The `SearchableProjectObjects` provides:

- Three query methods:
    - `all_names()`
    - `all_display_names()`
    - `all_object_ids()`
- Three specific search methods:
    - `find_by_name()`
    - `find_by_display_name()`
    - `find_by_object_id()`
- A general search method:
    - `find()` - This method expects a predicate to identify project objects of interest
- Two general iteration methods:
  - `all_objects()`
  - `SearchableProjectObjects` is an _iterator_

The script contains code similar to the notebook but runs either at the command line or in a REPL.

To use these tutorials:

- You may need to
  [configure the Orchid Python API to find the Orchid installation](#configure-the-orchid-python-api)
- You **must**
  [configure the Orchid Python API to find the Orchid training data](#configure-the-orchid-training-data)
- You may need to [view the Orchid API configuration details](#view-orchid-configuration-details)
- You may want to invoke the command, `copy_orchid_tutorials`

  This command copies the tutorial files into an optionally specified (virtual environment) directory. (The
  default destination is your current working directory.) Note that this command is a command-line script
  that runs in a console or terminal. Additionally, this command supports a help flag, `-h` or `--help`, to
  provide you with help on running this command.

More detailed instructions for running the tutorials can be found at:

- [Run development Orchid tutorials](#run-development-orchid-tutorials) or at
- [Run installed Orchid tutorials](#run-installed-orchid-tutorials)

## Tests

This project contains a large number of unit tests in the `tests` directory and three benchmark tests in the 
`benchmark_tests` directory. The unit tests can be run using a development environment like PyCharm. Consult the 
documentation for the development environment to understand how to run these different tests.

At the command line, one can also run the unit tests at the command line by executing 
`python -m unittest discover --start-directory=tests`.

Additionally, the project includes [pytest](https://docs.pytest.org/en/stable/) as  development dependency. `pytest`
supports executing both our unit tests and our benchmark tests. Our benchmark tests are marked as "slow" allowing a
developer to run unit tests and benchmark tests separately if desired.

To run these tests using `pytest`,

- In a Powershell window, navigate to the directory of a development virtualenv if not there already
- Activate the virtualenv (run `poetry shell`)
- Then in the root directory of the development virtualenv:

| To run...       | Execute the command... |
|-----------------|------------------------|
| Unit tests      | `pytest -m "not slow"` |
 | Benchmark tests | `pytest -m "slow"`     |
 | All tests       | `pytest`               |

## A Reading Suggestion

This document is one of several documents you may want to read:

- [README](./README.md) - The project README file.
- [README-dev.md](./README-dev.md) - This file.
- [ReleaseNotes.md](./ReleaseNotes.md) - The release notes for this project.

Although one can read this document in any text editor since it is simply a text file, consider installing
the [Python grip utility](https://pypi.org/project/grip/). This application allows one to "render local readme
files before sending off to GitHub". Although you need not send any of these file to `GitHub`, by using `grip` 
to render the file, you can much more easily navigate the document links.

## Getting Started

### Development Overview

To understand the structure of the code, the file, `./docs_dev/README.md`, in the source repository, contains 
an overview of the application / package design.

### Development

We use a virtual environment to make changes to and to test the Orchid Python API. This choice avoids putting
Orchid-specific-packages in your system Python environment and avoids version conflicts between the Orchid
Python API and other packages.

Although the Python ecosystem supports several tools to create and manage virtual environments, development 
uses `poetry` because of its support for developer tasks such as packaging and publishing. For information on 
`poetry` see [the poetry documentation](https://python-poetry.org/docs/).

#### Install Python

Install python 3.8 by following [these instructions](https://docs.python.org/3/using/windows.html). To ensure
access from the command line, be sure to select the "Add Python 3.x to PATH" option on the
[installer start page](https://docs.python.org/3/_images/win_installer.png). 

#### Ensure Command Line Access To Python

Although you may be able to perform development without command line access using, for example, `PyCharm`, many
instructions, including these instructions, will assume command line access. To verify command line access:

- Open a command prompt
- Type the command `python -V`

You should see a result like "Python 3.x".

#### Install Poetry

To use `poetry`, you may need to perform up to three steps. First, if you do not have python **3** installed,
you need to install it. To determine if python 3 is installed:

- In the Windows 10, search bar, type "add or remove programs".
- On the "Apps & features" page, search for "python"
- If you see an item named "Python 3.x", you have python 3 installed.

To install `poetry`:

If using Powershell (recommended):

- Open a Powershell terminal
- Execute the command

  ```
  (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
  ```
  
If using Windows command shell:

- Open a command prompt
- Invoke the command `pip install poetry`.

This will install the `poetry` package in your system python installation. (Note that python 3.x, by default,
installs `pip`. If Python is available from the command line, `pip` will also be available from the command
line.)

#### Create development environment

To create the development environment using `poetry`:

- Clone the `PythonApi` repository into a directory on your workstation. For convenience, we'll call that
  directory `/path/to/repo`.
- Open a command prompt
- Navigate to the `/path/to/repo`
- Execute the command `poetry install`

Wait patiently. This command will install **both** the run-time and development-time packages to support 
changing and running in your local, development environment.

##### Alternative development environments

Many people, including this author, use an IDE for python development. It is not necessary, but provides a 
number of conveniences for development.

To use [PyCharm](https://www.jetbrains.com/pycharm/) from [JetBrains](https://www.jetbrains.com/):

Determine the location of the created virtual directory:
- Navigate in your terminal to `/path/to/repo`
- Run the command, `poetry env list --full-path`
- Remember, or better yet, copy, the pathname of the virtualenv someplace where you can easily retrieve it 
  later. (The system clipboard may not be the best location because it is so easily overwritten.) 
  Symbolically, we will refer to this environment as `/path/to/virtual-env`

Open the Orchid Python API project:
- Start `PyCharm`
- Select `Open an existing project`.
- Select the `/path/to/repo` directory

Configure the project interpreter:
- Select `File > Settings > Project > Python Interpreter`
- Pull down the "Python interpreters" list
- Select "Show All"
- If `/path/to/virtual-env/Scripts/python.exe` is *not* listed,
    - Press the add button ('+')
    - Select the "Existing environment" radio button
    - Enter the pathname to the python interpreter, `/path/to/virtual-env/Scripts/python.exe`
    - Press "OK" to add the interpreter
- If `/path/to/virtual-env/Scripts/python.exe` is (now) listed in the "Python Interpreters" dialog, select it.
- Press "OK"

###### Sharing PyCharm configurations

When you configure the Python interpreter for PyCharm, `PyCharm` creates a "name" for this interpreter. By
default, it uses the name of the Python virtual environment in which it finds that interpreter. This choice 
works for a single individual, but fails when attempting to share configurations because `poetry` creates a
virtual environment name that seems to depend on data specific to either the currently logged-in user or to
the workstation. 

To avoid these conflicting changes to `PythonApi.iml` and `.idea/misc.xml`, we use a technique recommended by
JetBrains in [this YouTrack issue](https://youtrack.jetbrains.com/issue/PY-20228). We have agreed to name our
`PyCharm` interpreter configuration using the "well known" name, "orchid-python-api-dev-py3.8". This choice
replaces the suffix specific to the user or machine with `dev`. It does encode the Python interpreter
version, but `poetry`, we believe, uses this encoding to support use of different interpreters.

To use Visual Studio, a recommended tool is 
[Python Tools for Visual Studio](https://visualstudio.microsoft.com/vs/features/python/). The author assumes 
you are familiar with (or will become familiar with) this tool and its capabilities.

If you prefer a "lighter" development environment, consider 
[Visual Studio Code](https://code.visualstudio.com/docs/languages/python). Again, the author assumes you are 
familiar with (or will become familiar) with this tool and its capabilities.

Finally, many, many, many other tools exist to support Python ranging from "editors" (Emacs and Vim) to tools 
like Atom and Sublime. You can most likely use whatever editing environment you are familiar with (or, like 
me, more than one). Remember the recommendation from the book, _The Pragmatic Programmer_: "Find one editor 
and stick to it."

## Build and test locally

### Package a distribution

- Open a terminal and navigate to the project repository root.
- Remove the `dist` directory if present.
- Invoke the command `invoke poetry.package`
- Review the built packages. Ensure that:
    - The version number is correct.
    - The build process builds both 
        - A source distribution (`.tar.gz` file)
        - A binary (wheel) distribution (`.whl` file)
    - The distribution contains the correct `ReleaseNotes.md` For example one can view the file contents by
      using the command `vim dist/<package>.tar.gz` or by using a tool like 7-zip.
        
### Install local package

#### Install and test locally in pipenv virtual environment

- [Create a new, clean virtualenv](#create-a-new-clean-virtualenv)
- In a Powershell window, navigate to the directory of the new virtualenv
- Activate the virtualenv (run `pipenv shell`)
- Install the package distribution by running `pip install </path/to/package-distribution>`
- [Ensure installation of correct Orchid version](#ensure-correct-orchid)
- [Configure the Orchid Python API to find the Orchid installation](#configure-the-orchid-python-api)
- [Configure the Orchid Python API to find the Orchid training data](#configure-the-orchid-training-data)

Finally, 

- [Run Orchid examples](#run-installed-orchid-high-level-examples)
- [Run Orchid tutorials](#run-installed-orchid-tutorials)
- Optionally, [Run Orchid low-level examples](#run-installed-orchid-low-level-examples)
- Optionally, [Run Orchid manual examples](#run-installed-orchid-manual-examples)

#### Install and test locally in conda environment

- [Create a clean conda environment](#create-a-clean-conda-environment)
- In an Anaconda Powershell window, navigate to the directory of the test directory
- Activate the virtualenv (run `conda activate orchid`)
- Optionally install `spyder`
- Install the package distribution by running `pip install </path/to/package-distribution>`
- [Ensure installation of correct Orchid version](#ensure-correct-orchid)
- [Configure the Orchid Python API to find the Orchid installation](#configure-the-orchid-python-api)
- [Configure the Orchid Python API to find the Orchid training data](#configure-the-orchid-training-data)

Finally,

- [Run Orchid examples](#run-installed-orchid-high-level-examples)
- [Run Orchid tutorials](#run-installed-orchid-tutorials)
- Optionally, [Run Orchid low-level examples](#run-installed-orchid-low-level-examples)
- Optionally, [Run Orchid manual examples](#run-installed-orchid-manual-examples)

## Publish a release

Publishing a release has a number of general steps. These steps are optional except for
[the last step](#publish-to-pypi). Here are the steps:

- Update the release notes
- [Update poetry](#update-poetry)
- [Update dependencies](#update-dependencies)
- [Update API version](#update-api-version)
- [Generate requirements file](#generate-requirements-file)
- [Generate documentation](#generate-documentation)
- [Build and test locally](#build-and-test-locally)
- [Publish to TestPyPI](#publish-to-testpypi)
- [Publish to PyPI](#publish-to-pypi)
- Merge `develop` into `master`
- Push `master` to GitHub
- Merge `master` into `master-reveal` (that is, `reveal-energy/master`)
- Push `master-reveal` to Azure DevOps
- Send email announcing release

Throughout these tasks, you will repeatedly [Run common tasks](#common-tasks)

Remember that the file, `tasks.py`, defines many common tasks. Be sure to use commands like:

- `invoke --help` for general help on `invoke`
- `invoke --list` to list the available tasks
- `invoke poetry.venv.remove --help` (for help on a specific command listed)

to perform these tasks.

### Update poetry

- Terminate all processes, including PyCharm, that use the `poetry` virtual environment anchored at the
  repository directory to allow poetry to update its files.
- Navigate to the repository directory
- Execute the command `poetry self update`

**Warning**

When the author attempted to execute this command, he encountered an error that the update **could not**
update a library. This same message occurred both in a Git Bash shell and in a Powershell (1.0) shell. After
receiving this message, the installation of was corrupted. (The author received a message like "Could not
import `poetry.console`".) To resolve this issue, the author simply installed `poetry` again. This repaired the
`poetry.console` error and updated `poetry` to the latest version.

When encountering this error a second time, the author noticed an "access denied" error in the stack trace.
The author also noticed that PyCharm, which **uses** the virtual machine anchored at the repository directory,
was running during this update. The author hypothesized that the running instance of PyCharm is what causes
the error.

#### Uninstall poetry

To work around this issue, one may need to uninstall `poetry` by:

- Navigate to the repository root
- If using a `Powershell` command prompt (recommended):
  - Download the poetry installer by executing
    ```
    (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python - --uninstall
    ```
    
- If using a `bash` shell:
  - Download the poetry installer by executing
    ```
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - 
    ```

See [Poetry Issue 2245](https://github.com/python-poetry/poetry/issues/2245) for similar instructions. After
removing `poetry`, reinstall it by following the
[installation instructions](https://python-poetry.org/docs/#installation).

### Update dependencies

To update the project dependencies:

- [Create a new, clean development virtualenv](#create-a-new-clean-development-virtualenv)
- In a Powershell window, navigate to the directory of the new virtualenv if not there already
- Activate the virtualenv (run `poetry shell`)
- Update the dependencies
  - Run `poetry update`

### Update API version

#### Edit the internal version

- Open the file `orchid/VERSION` for editing.
- Change the version in the file to the updated value. The safest way to update the value is copying the
  value if at all possible. The log files print the version number in the banner at the beginning of each
  execution of Orchid.

  NOTE: the Orchid Python API only uses the
  [release segment](https://www.python.org/dev/peps/pep-0440/#public-version-identifiers) of its version to
  calculate the corresponding Orchid version. Consequently, one shall:
  - Copy only the first three components of the Orchid version (the major, minor and patch components). This
    choice means **not** copying the fourth or build component of the Orchid API version. This action results
    in an API version identifier like `2021.1.399`.
  - If the Orchid Python API has either a
    [post-release](https://www.python.org/dev/peps/pep-0440/#post-releases) or a
    [pre-release](https://www.python.org/dev/peps/pep-0440/#post-releases) segment, append this segment to the
    version identifier in `orchid/VERSION`. This action results in an API version identifier like
    - `2021.1.399post1` - a post-release or
    - `2021.1.399b3` - a "beta-3" pre-release

#### Edit the package version number

- Open the file `pyproject.toml` for editing.
- Copy the version identifier from `orchid/VERSION` to the value of the `version` key of the file.
- Search for the `classifiers` element of `pyproject.toml`.
  - If the Orchid Python API version identifier is a pre-release version identifier,
    - Uncomment the `Development Status :: 4 - Beta` item.
    - Comment out the `Development Status :: 5 Production/Stable` item.
  - If the Orchid Python API version identifier is a
    [final release](https://www.python.org/dev/peps/pep-0440/#final-releases) version identifier,
    - Comment out the `Development Status :: 4 - Beta` item.
    - Uncomment the `Development Status :: 5 Production/Stable` item.

#### Edit the version number in the release notes

- Open the file `ReleaseNotes.md` for editing.
- Copy the version identifier from `orchid/VERSION` to the version number for the release.

#### Edit the version number in the documentation

- Navigate to the `docs` directory
- Open the file `conf.py` for editing.
- Search for the `release` value in the file
- Copy the version identifier from `orchid/VERSION` to the `release` value.

### Publish to TestPyPI

The steps to publish to TestPyPi are very similar to the steps for
[Build and install locally](#build-and-test-locally) and for [Publish to PyPI](#publish-to-pypi). For an
introduction to the process (but some different steps), review the
[Python Packaging Guide](https://packaging.python.org/guides/using-testpypi/).

- [Package a distribution](#package-a-distribution)

#### Configure TestPyPI as a `poetry` repository

- Determine if TestPyPI is already configured by running either:
  - `invoke poetry.config.list`
  - `poetry config --list`
- Examine the output for the key, `repositories.test-pypi.url`
- If key is present, `poetry` is already configured so skip to
  [Publish distribution to TestPyP](#publish-distribution-to-testpypi)
- To configure the TestPyPI repository, run either
  - `invoke poetry.config.test-pypi` or
    ```
    poetry config repositories.test-pypi https://test.pypi.org/legacy/
    ```

Once configured, you will also need to configure the API token for the TestPyPI website. Because the API
token is a security token, the author is unaware of any way to examine if the token has already been
configured. However, configuring an already configured token **does not** cause an error.

To generate an API token, complete the steps described at [PyPI help](https://pypi.org/help/#apitoken) but for
the TestPyPI website.

Once generated, add it to the `poetry` configuration by executing either:

- `invoke poetry.config.api-token -r test-pypi -t <token>` or
- `poetry config pypi-token.test-pypi <token>`

#### Publish distribution to TestPyPI

To publish the distribution to TestPyPI execute either:

- `invoke poetry.publish test-pypi` or
- `poetry publish --repository=test-pypi`

Once published, test the published distribution by:

- [Create a new, clean virtualenv](#create-a-new-clean-virtualenv)
- In a powershell window, navigate to the directory of the new virtualenv
- Activate the virtualenv (run `pipenv shell`)
- Install the package distribution by running the command,
  ```
  pip install --index-url https://test.pypi.org/simple/ orchid-python-api
  ```

If an error occurs, read the error message(s) and consult the section
[Possible installation errors and resolutions](#possible-installation-errors-and-resolutions).

Once installed, 

- [Run Orchid examples](#run-installed-orchid-high-level-examples)
- [Run Orchid tutorials](#run-installed-orchid-tutorials)
- Optionally, [Run Orchid low-level examples](#run-installed-orchid-low-level-examples)

Optionally, test the published distribution in a conda environment by:

- [Create a clean conda environment](#create-a-clean-conda-environment)
- In a powershell window, navigate to the directory of the new virtualenv
- Activate the virtualenv (run `conda activate orchid`)
- Optionally install `spyder`
- Install the package distribution by running the command,
  ```
  pip install --index-url https://test.pypi.org/simple/ orchid-python-api
  ```

If an error occurs, read the error message(s) and consult the section
[Possible installation errors and resolutions](#possible-installation-errors-and-resolutions).

Once installed,

- [Run Orchid examples](#run-installed-orchid-high-level-examples)
- [Run Orchid tutorials](#run-installed-orchid-tutorials)
- Optionally, [Run Orchid low-level examples](#run-installed-orchid-low-level-examples)

### Publish to PyPI

**Before** publishing to PyPI, ensure that:

- All outstanding PR's have been completed.
- You have merged all changes to the `develop` branch
- You have changed your current branch to the `develop` branch
- You have tagged `develop` with the release API version
- You have pushed the tags to our repositories, GitHub and Azure DevOps, by executing commands like:
  - `git push origin 2022.2.324` (assumes `origin` maps to GitHub)
  - `git push reveal-origin 2022.2.324` (assumes `reveal-energy` maps to Azure DevOps)

You will most likely need to configure the API token for PyPI.

To generate an API token, complete the steps described at [PyPI help](https://pypi.org/help/#apitoken).

Once generated, add it to the `poetry` configuration by executing either:

- `invoke poetry.config.api-token -r pypi -t <token>` or
- `poetry config pypi-token.pypi <token>`

To publish the distribution to PyPI execute either:

- `invoke poetry.publish pypi` or
- `poetry publish`

If you navigate to `https://pypi.org/` and search for "orchid-python-api" (no quotation marks), you should
see the version of the distribution you have created. If not, but no error was reported, you most likely \
**have not** configured your API token correctly.

Once published, test the published distribution by:

- [Create a new, clean virtualenv](#create-a-new-clean-virtualenv)
- In a Powershell window, navigate to the directory of the new virtualenv
- Activate the virtualenv (run `pipenv shell`)
- Install the package distribution by running the command, `pip install orchid-python-api`.

- [Run Orchid examples](#run-installed-orchid-high-level-examples)
- [Run Orchid tutorials](#run-installed-orchid-tutorials)
- Optionally, [Run Orchid low-level examples](#run-installed-orchid-low-level-examples)

Optionally, test the published distribution in a conda environment by:

- [Create a clean conda environment](#create-a-clean-conda-environment)
- In a powershell window, navigate to the directory of the new virtualenv
- Activate the virtualenv (run `conda activate orchid`)
- Optionally install `spyder`
- Install the package distribution by running the command, `pip install orchid-python-api`.
- [Run Orchid examples](#run-installed-orchid-high-level-examples)
- [Run Orchid tutorials](#run-installed-orchid-tutorials)
- Optionally, [Run Orchid low-level examples](#run-installed-orchid-low-level-examples)

## Common tasks

### Install Orchid release

You have two options:

- [Install from web portal](#install-from-web-portal)
- [Install from build pipelines](#install-from-build-pipelines)

### Install from web portal

- Open the [Orchid web portal](https://portal.reveal-energy.com)
- Click the "Sign In" link
- Click the "Reveal Energy Employee Sign In"
- If prompted, enter your Profile information
- Select "Downloads"
- Find the desired version
- Install the version by clicking the "download" or "alternative download" link

This will download the installer to your workstation.

Once finished, click on the downloaded installer and follow the wizard prompts to install the executable.

### Install from build pipelines

- Navigate to the [ImageFrac Pipelines](https://reveal-energy.visualstudio.com/ImageFrac/_build)
- Select the "Orchid Release Pipeline"
- Select the version you wish to install, for example, "#2021.2.316...", to install version 2021.2.316
  of Orchid
- Find the "Stages" tab (you may need to scroll the web page)
- Find the "Create Installer" stage
- Select the "artifacts" link of the "Create Installer" stage
- Open the "Orchid-Application-Installer" link
- Click on the installer, for example, "Orchid-2021.2.316-Installer.exe"

This will download the installer to your workstation.

Once finished, click on the downloaded installer and follow the wizard prompts to install the executable.

### Upgrade pipenv

- Navigate to the repository root
- Execute the command `pip install pipenv --upgrade`

### Update conda

- Open an Anaconda Powershell console
- Activate the "base" `conda` environment if not already activated
- Execute the command `conda update conda`

### Ensure correct Orchid

By default, the Python API for Orchid expects to find the Orchid binaries in a specific location on your local
system. To ensure the correct version of Orchid is installed,

- Navigate to the orchid installation directory, `$PROGRAMFILES\Reveal Energy Services\Orchid`
- List that directory
- You should see a directory named something like, `Orchid-<python-api-version>.<build>`, where
  `<python-api-version>` is a symbolic reference for the version number in which you are interested and
  `<build>` is a symbolic reference to the build number which **does not matter** for our purposes.
- Navigate into the version specific information. For example, `Orchid-2021.4.283.27327`
- You should see a directory like `PythonApiLibs`
- Navigate into this directory
- You should see files like:
  - `appSettings.json`
  - `Orchid.FractureDiagnostics.dll`
  - Many, many others

To make doubly certain, you could run `Orchid.Application.exe` and ensure that the application displays the
correct version number in the main window title bar.

If it is not installed, you'll need to [Install the appropriate Orchid release](#install-orchid-release)

### Create a new, clean development virtualenv

If using the command line,

- Remove any existing virtual directory by:
  - Navigate to the root directory of the repository
  - Execute the command `poetry env remove <virtual-env>` to remove the virtual environment itself. The
    argument, `virtual-env`, is the short name identifying the virtual environment associated with the
    repository root.

  NOTE: If no such virtualenv exists, running this command produces a message like:
    ```
    [ValueError]
    Environment "orchid-python-api-_tsnD6Qt-py3.7" does not exist.
    ```

- Create a new, clean virtual environment by:
  - Execute the command `poetry env use <python-path>` where `<python-path>` is the pathname of the
    Python interpreter to use for  the environment (currently Python 3.8.10 for the Orchid Python API).

If using `python invoke`,

- Navigate to the repository root
- Remove the existing virtualenv if any
  - Run `invoke poetry.venv.remove --venv=<virtual-env>`. NOTE: If no such virtualenv exists, running this
    task will produce a message like:
    ```
    No virtualenv has been created for this project yet!
    Aborted!
    ```

Delete any leftover files
- If present, delete all leftover files from the virtualenv directory.

Create a new skeleton virtual environment
- Run `invoke poetry.venv.create`.

To test that you were successful,

- Navigate to the root directory of the repository if not there already
- Activate the virtualenv by executing, `poetry shell`
- Execute the command, `pip list --local`. You should see output like the following (but probably with
  different version numbers)

  ```
  Package    Version
  ---------- -------
  pip        21.1.1
  setuptools 56.2.0
  wheel      0.36.2
  ```

### Create a new, clean virtualenv

These instructions assume you will create a test virtual directory using `pipenv`. This tool is simpler to
use than `poetry` but does not have the convenient development features of `poetry`. Further, these
instructions assume that your test directory is something like `<path/to/inst/orchid/pipenv>`

Consider [Upgrade pipenv](#upgrade-pipenv)

If using the command line,

- Remove any existing virtual directory by:
  - Navigate to the root directory of the directory attached to the virtual environment. For example,
    navigate to `C:\inst\orchid\pipenv`.
  - Execute the command `pipenv --rm` to remove the virtual environment itself. NOTE: If no such virtualenv
    exists, running this command produces a message like:

    ```No virtualenv has been created for this project yet!```

  - Remove `Pipfile` and `Pipfile.lock` using the command supported by your shell.
  - Remove any other files remaining in the virtual environment directory.
  - Be sure to remove any **hidden** files or directories. For example, a file or a directory starting with
    a dot ("."), like `.ipynb_checkpoints`, is hidden to typical listings of Unix-like shells.

- Create a new, clean virtual environment by:
  - Execute the command `pipenv install --python=<python_ver>` where `python_ver` is the version of Python
    used by the Orchid Python API (currently 3.8.10).

If using `python invoke`,

- Navigate to the repository root
- Remove the existing virtualenv if any
  - Run `invoke pipenv.venv.remove --dirname=<path/to/inst/orchid/pipenv>`. NOTE: If no such virtualenv
    exists, running this task will produce a message like:

    ```
    No virtualenv has been created for this project yet!
    Aborted!
    ```

- If present, delete all leftover files from the virtualenv directory.

- Create a new skeleton virtual environment by running
  ```
  invoke pipenv.venv.create --dirname=<path/to/inst/orchid/pipenv>
  ```

To test that you were successful,

- Open a Powershell console
- Navigate to the virtual environment directory if not there already
- Activate the virtualenv by executing, `pipenv shell`
- Execute the command, `pip list --local`. You should see output like the following (but probably different
  version numbers)

  ```
  Package    Version
  ---------- -------
  pip        21.1.1
  setuptools 56.2.0
  wheel      0.36.2
  ```

### Create a clean conda environment

These instructions assume you will create a virtual environment using `conda`. This tool is simpler to use
than `poetry` but does not have the convenient development features of `poetry`. Further, these instructions
assume that your test directory is something like `<path/to/inst/orchid/conda>` and that your `conda`
environment is named `orchid`. Finally, these assumptions assume you will use an Anaconda Powershell
environment. Although many of the commands should work unchanged in an Anaconda `cmd` shell, we have not
tested these instructions in that environment.

- Consider [Update conda](#update-conda)
- Remove any existing environment by:
  - Navigate to the test directory. For example, navigate to `C:\inst\orchid\conda`.
  - List all available `conda` environments by executing `conda env list`. This command produces output like:
    ```
    # conda environments:
    #
    learn-pint               C:\Users\larry.jones\.conda\envs\learn-pint
                             C:\Users\larry.jones\.julia\conda\3
    base                  *  C:\Users\larry.jones\Miniconda3
    data-science-2e          C:\Users\larry.jones\Miniconda3\envs\data-science-2e
    orchid                   C:\Users\larry.jones\Miniconda3\envs\orchid
    orchid-doctest           C:\Users\larry.jones\Miniconda3\envs\orchid-doctest 
    ```
  - If the `orchid` environment exists,
    - Remember the pathname of the virtual environment. In our case, the pathname is
      `C:\Users\larry.jones\Miniconda3\envs\orchid`
    - Execute the command `conda env remove --name orchid` to remove the environment itself.
    - Remove the virtual directory itself by executing 
      ```
      remove-item /path/to/conda-environments/orchid -recurse
      ```
    - Remove any other files remaining in the test directory.
    - Be sure to remove any **hidden** files or directories. For example, a file or a directory starting with
      a dot ("."), like `.ipynb_checkpoints`, is hidden to typical listings of Unix-like shells.


- Create a new, clean virtual environment by:
  - Execute the command 
    ```
    conda create --name orchid python=<python-version>
    ```
    where `python_ver` is the version of Python used by the Orchid Python API (currently 3.8.10).
  - If you see errors or warnings, attempt to [resolve conda create issues](#resolve-conda-create-issues)
    and then execute the previous command.

- Test that you were successful by:
  - Execute `conda env list`. You should see output like:

    ```
    # conda environments:
    #
    learn-pint               C:\Users\larry.jones\.conda\envs\learn-pint
                             C:\Users\larry.jones\.julia\conda\3
    base                  *  C:\Users\larry.jones\Miniconda3
    data-science-2e          C:\Users\larry.jones\Miniconda3\envs\data-science-2e
    orchid                   C:\Users\larry.jones\Miniconda3\envs\orchid
    orchid-doctest           C:\Users\larry.jones\Miniconda3\envs\orchid-doctest
    ```

Ensure that the `orchid` environment exists.

#### Resolve conda create issues

- If you see a warning like,

  ```
  WARNING: A directory already exists at the target location 'C:\Users\larry.jones\Miniconda3\envs\orchid'
  but it is not a conda environment.
  Continue creating environment (y/[n])?
  ```

  Enter 'y' to overwrite the existing directory.

### Run all Orchid tests

To run all orchid tests
- Run unit tests
- Run acceptance (feature) tests
- [Run development Orchid high-level examples](#run-development-orchid-high-level-examples)

### Run development Orchid high-level examples

- Prepare to run examples
  - If you have not already done so,
    [configure the Orchid Python API to find the Orchid installation](#configure-the-orchid-python-api)
  - You **must**
    [configure the Orchid Python API to find the Orchid training data](#configure-the-orchid-training-data)
  - Navigate to `/path/to/repo`
  - If orchid-python-api is installed in the virtual environment,
    - Run `python ./copy_orchid_examples.py` to copy the examples to the current directory
  - If orchid-python-api not (yet) installed,
    - Copy the example notebooks to the orchid project repository root
      ```
      copy ./orchid_python_api/examples/*.ipynb </path/to/orchid_repo>
      ```
- Activate `poetry shell` if not activated

#### Run example scripts

- Run the first script
  - Execute the command `python plot_trajectories.py`
  - Wait patiently for the `matplotlib` plot window to appear.
  - Ensure the plot is correct.
  - Dismiss the `matplotlib` window.
- Repeat for these scripts:
  - `plot_treatment.py`
  - `plot_time_series.py`
  - `completion_analysis.py` (This script prints multiple messages and presents **multiple** plots.
    You must dismiss each plot to continue.)
  - `volume_2_first_response.py`
  - `search_data_frames.py`
- Run the `stage_qc_results.py` script.
- Run the `change_stage_times.py` script.
- Run the `add_stages.py` script.

The scripts, `stage_qc_results.py`, `change_stage_times.py`, and `add_stages.py`, differ from the other scripts. These
scripts require a number of command line arguments to run correctly. 

For example, to see an explanation of these arguments, execute any of this scripts with the `--help` option.
The most typical arguments are described in the following paragraphs.

To both read and write stage QC results, run the command:
```
python stage_qc_results.py -v2 /path/to/orchid-traing-data/frankNstein_Bakken_UTM13_FEET.v11.ifrac 
```

To only read the existing stage QC data, run the command
```
python stage_qc_results.py -v2 --read-only /path/to/orchid-traing-data/frankNstein_Bakken_UTM13_FEET.ifrac
```

To change the stage start and stop times (the time range), run the command
```
python change_stage_times.py -v2 /path/to/orchid-traing-data/frankNstein_Bakken_UTM13_FEET.v11.ifrac 
```

To add stages to a well, run the command
```
python add_stages.py -v2 /path/to/orchid-traing-data/frankNstein_Bakken_UTM13_FEET.ifrac 
```

#### Run example notebooks

- Open Jupyter by running `jupyter lab` in the shell
- Within Jupyter,
  - Successfully run notebook, `plot_trajectories.ipynb`
    1. Open notebook
    2. Run all cells of notebook
    3. Wait patiently
    4. Verify that no exceptions occurred
  - Repeat for remaining notebooks:
    - `plot_treatment.ipynb`
    - `plot_time_series.ipynb`
    - `completion_analysis.ipynb`
    - `volume_2_first_response.ipynb`
    - `search_data_frames.ipynb`

### Run installed Orchid high-level examples

If testing against an Orchid release, [Install Orchid release](#install-orchid-release)

- Prepare to run examples
    - If you have not already done so, 
      [configure the Orchid Python API to find the Orchid installation](#configure-the-orchid-python-api)
    - You **must** 
      [configure the Orchid Python API to find the Orchid training data](#configure-the-orchid-training-data)
- If you are testing a `pipenv` virtual environment or a `conda` environment,
    - Navigate to the directory associated with the virtual environment
    - If necessary, activate the virtual environment.
    - Run `copy_orchid_examples`.
    - If the executable reports that it skipped files, repeat the command with an additional argument:  
      `copy_orchid_examples --overwrite`
    - Verify that the current directory has six example notebooks:
        - `completion_analysis.ipynb`
        - `plot_time_series.ipynb`
        - `plot_trajectories.ipynb`
        - `plot_treatment.ipynb`
        - `search_data_frames.ipynb`
        - `volume_2_first_response.ipynb`
    - Verify that the current directory has nine example scripts:
      - `add_stages.py`
      - `change_stage_times.py`
      - `completion_analysis.py`
      - `plot_time_series.py`
      - `plot_trajectories.py`
      - `plot_treatment.py`
      - `search_data_frames.py`
      - `stage_qc_results.py`
      - `volume_2_first_response.py`
- If you are testing a `poetry` virtual environment
    - If orchid-python-api is installed in the virtual environment,
        - Run `python ./copy_orchid_examples.py` to copy the examples to the current directory
    - If orchid-python-api not (yet) installed,
        - Copy the example notebooks to the orchid project repository root
          ```
          copy ./orchid_python_api/examples/*.ipynb </path/to/orchid_repo>
          ```

#### Run example scripts

- Run the first script
  - Execute the command `python plot_trajectories.py`
  - Wait patiently for the `matplotlib` plot window to appear.
  - Ensure the plot is correct.
  - Dismiss the `matplotlib` window.
- Repeat for these scripts:
  - `plot_treatment.py`
  - `plot_time_series.py`
  - `completion_analysis.py` (This script prints multiple messages and presents **multiple** plots.
    You must dismiss each plot to continue.)
  - `volume_2_first_response.py`
  - `search_data_frames.py`
- Run the `stage_qc_results.py` script.
- Run the `change_stage_times.py` script.
- Run the `add_stages.py` script.

The scripts, `stage_qc_results.py`, `change_stage_times.py`, and `add_stages.py`, differ from the other scripts. These
scripts require a number of command line arguments to run correctly.

For example, to see an explanation of these arguments, execute any of this scripts with the `--help` option.
The most typical arguments are described in the following paragraphs.

To both read and write stage QC results, run the command:
```
python stage_qc_results.py -v2 /path/to/orchid-traing-data/frankNstein_Bakken_UTM13_FEET.ifrac 
```

To only read the existing stage QC data, run the command
```
python stage_qc_results.py -v2 --read-only /path/to/orchid-traing-data/frankNstein_Bakken_UTM13_FEET.v11.ifrac
```

To change the stage start and stop times (the time range), run the command
```
python change_stage_times.py -v2 /path/to/orchid-traing-data/frankNstein_Bakken_UTM13_FEET.ifrac 
```

To add stages to a well, run the command
```
python add_stages.py -v2 /path/to/orchid-traing-data/frankNstein_Bakken_UTM13_FEET.v11.ifrac 
```

#### Run example notebooks

- Open Jupyter by running `jupyter lab` in the shell
- Within Jupyter,
    - Successfully run notebook, `plot_trajectories.ipynb`
        1. Open notebook
        2. Run all cells of notebook
        3. Wait patiently
        4. Verify that no exceptions occurred
    - Repeat for remaining notebooks:
      - `plot_treatment.ipynb`
        - `plot_time_series.ipynb`
        - `completion_analysis.ipynb`
        - `volume_2_first_response.ipynb`
        - `search_data_frames.ipynb`

### Run installed Orchid low-level examples

If testing against an Orchid release, [Install Orchid release](#install-orchid-release)

- Prepare to run examples
  - If you have not already done so,
    [configure the Orchid Python API to find the Orchid installation](#configure-the-orchid-python-api)
  - You **must**
    [configure the Orchid Python API to find the Orchid training data](#configure-the-orchid-training-data)
- If you are testing a `pipenv` virtual environment or a `conda` environment,
  - Navigate to the directory associated with the virtual environment
  - If necessary, activate the virtual environment.
  - Run `copy_orchid_low_level_examples`.
  - If the executable reports that it skipped files, repeat the command with an additional argument:  
    `copy_orchid_low_level_examples --overwrite`
  - Verify that the current directory has one example notebooks:
    - `auto_pick.ipynb`
  - Verify that the current directory has three example scripts:
    - `add_stages_low.py`
    - `auto_pick.py`
    - `auto_pick_and_create_stage_attribute.py`
    - `auto_pick_iterate_example.py`
    - `monitor_time_series.py`
    - `multi_picking_events.py`
- If you are testing a `poetry` virtual environment
  - If orchid-python-api is installed in the virtual environment,
    - Run `python ./copy_orchid_low_level_examples.py` to copy the examples to the current directory
  - If orchid-python-api not (yet) installed,
    - Copy the low-level examples to the orchid project repository root by executing the commands:
      ```
      copy ./orchid_python_api/examples/low_level/*.ipynb </path/to/orchid_repo>
      copy ./orchid_python_api/examples/low_level/*.py </path/to/orchid_repo>
      ```

#### Run low-level example scripts

- Run the scripts
  - Execute the command 
    ```
    python auto_pick.py --verbosity=2 /path/to/training-data/frankNstein_Bakken_UTM13_FEET.v11.ifrac
    ```
    where `/path/to/training-data` is a symbolic reference to the path to the Orchid training data
  - Review the output and ensure the script finishes without errors.
  - Optionally test the newly created `.ifrac` file in Orchid
  - Execute the command 
    ```
    python auto_pick_and_create_stage_attribute.py --verbosity=2 /path/to/training-data/frankNstein_Bakken_UTM13_FEET.ifrac
    ```
    where `/path/to/training-data` is a symbolic reference to the path to the Orchid training data
  - Review the output and ensure the script finishes without errors.
  - Optionally test the newly created `.ifrac` file in Orchid
  - Execute the command
    ```
    python auto_pick_iterate_example.py --verbosity=2 /path/to/training-data/frankNstein_Bakken_UTM13_FEET.v11.ifrac
    ```
    where `/path/to/training-data` is a symbolic reference to the path to the Orchid training data
  - Review the output and ensure the script finishes without errors.
  - Optionally test the newly created `.ifrac` file in Orchid
  - Execute the command `python monitor_time_series.py`
  - Review the output and ensure the script finishes without errors.
  - Optionally test the newly created `.ifrac` file in Orchid
  - Execute the command
    ```
    python add_stages_low.py --verbosity=2 /path/to/training-data/frankNstein_Bakken_UTM13_FEET.ifrac
    ```
    where `/path/to/training-data` is a symbolic reference to the path to the Orchid training data
  - Review the output and ensure the script finishes without errors.
  - Optionally test the newly created `.ifrac` file in Orchid
  - Execute the command
    ```
    python multi_picking_events.py --verbosity=2 /path/to/training-data/frankNstein_Bakken_UTM13_FEET.ifrac
    ```
    where `/path/to/training-data` is a symbolic reference to the path to the Orchid training data
  - Review the output and ensure the script finishes without errors.
  - Optionally test the newly created `.ifrac` file in Orchid

#### Run low-level example notebook

- Open Jupyter by running `jupyter lab` in the shell
- Within Jupyter,
  - Successfully run notebook, `auto_pick.ipynb`
    1. Open notebook
    2. Run all cells of notebook
    3. Wait patiently
    4. Verify that no exceptions occurred
  - Review the output and ensure the script finishes without errors.
  - Optionally test the newly created `.ifrac` file in Orchid

### Run installed Orchid manual examples

If testing against an Orchid release, [Install Orchid release](#install-orchid-release)

- Prepare to run examples
  - If you have not already done so,
    [configure the Orchid Python API to find the Orchid installation](#configure-the-orchid-python-api)
  - You **must**
    [configure the Orchid Python API to find the Orchid training data](#configure-the-orchid-training-data)
- If you are testing a `pipenv` virtual environment or a `conda` environment,
  - Navigate to the directory associated with the virtual environment
  - If necessary, activate the virtual environment.
  - Run `copy_orchid_manual_examples`.
  - If the executable reports that it skipped files, repeat the command with an additional argument:  
    `copy_orchid_manual_examples --overwrite`
  - Verify that the current directory has one example notebook:
    - `data_frame_with_guid.ipynb`
  - Verify that the current directory has one example script:
    - `data_frame_with_guid.py`
- If you are testing a `poetry` virtual environment
  - If orchid-python-api is installed in the virtual environment,
    - Run `python ./copy_orchid_manuel_examples.py` to copy the examples to the current directory
  - If orchid-python-api not (yet) installed,
    - Copy the example notebooks to the orchid project repository root
      ```
      copy ./orchid_python_api/examples/manual/*.ipynb </path/to/orchid_repo>
      copy ./orchid_python_api/examples/manual/*.py </path/to/orchid_repo>
      ```

#### Run manual example scripts

- Run the first script
  - Execute the command `python data_frame_with_guid.py`
  - Wait patiently for the script to complete
  - Verify that the script prints a warning like the following:
    ```
    KNOWN ISSUE: Multiple data frames with duplicate object IDs detected.

    Workarounds:
    - **DO NOT** use `find_by_object_id`; use `find_by_name` or `find_by_display_name` to search.
    - Delete and recreate all data frames in a release of Orchid > 2022.3.
    ``` 
  - Verify that the script prints the data frame similar to:
    ```
                  ProjectName WellName WellDisplayName  ...  StageLengthTopTop ClusterNumber  FormationConnectionType
    0   PermianProjectQ3_2022       C1              C1  ...              200.0           1.0              PlugAndPerf
    1   PermianProjectQ3_2022       C1              C1  ...              220.0           1.0              PlugAndPerf
    2   PermianProjectQ3_2022       C1              C1  ...              220.0           1.0              PlugAndPerf
    3   PermianProjectQ3_2022       C1              C1  ...              220.0           1.0              PlugAndPerf
    4   PermianProjectQ3_2022       C1              C1  ...              220.0           1.0              PlugAndPerf
    ..                    ...      ...             ...  ...                ...           ...                      ...
    81  PermianProjectQ3_2022       C3              C3  ...              151.0           1.0              PlugAndPerf
    82  PermianProjectQ3_2022       C3              C3  ...              153.0           1.0              PlugAndPerf
    83  PermianProjectQ3_2022       C3              C3  ...              143.0           1.0              PlugAndPerf
    84  PermianProjectQ3_2022       C3              C3  ...              153.0           1.0              PlugAndPerf
    85  PermianProjectQ3_2022       P1              P1  ...                NaN           NaN                     None 
    ```

#### Run example manual notebooks

- Open Jupyter by running `jupyter lab` in the shell
- Within Jupyter,
  - Successfully run notebook, `data_frame_with_guid.ipynb`
    - Open notebook
    - Run all cells of notebook
    - Wait patiently
    - Verify that the script prints a warning like the following:
      ```
      KNOWN ISSUE: Multiple data frames with duplicate object IDs detected.

      Workarounds:
      - **DO NOT** use `find_by_object_id`; use `find_by_name` or `find_by_display_name` to search.
      - Delete and recreate all data frames in a release of Orchid > 2022.3.
      ``` 
    - Verify that the script prints the data frame similar to:
      ```
                    ProjectName WellName WellDisplayName  ...  StageLengthTopTop ClusterNumber  FormationConnectionType
      0   PermianProjectQ3_2022       C1              C1  ...              200.0           1.0              PlugAndPerf
      1   PermianProjectQ3_2022       C1              C1  ...              220.0           1.0              PlugAndPerf
      2   PermianProjectQ3_2022       C1              C1  ...              220.0           1.0              PlugAndPerf
      3   PermianProjectQ3_2022       C1              C1  ...              220.0           1.0              PlugAndPerf
      4   PermianProjectQ3_2022       C1              C1  ...              220.0           1.0              PlugAndPerf
      ..                    ...      ...             ...  ...                ...           ...                      ...
      81  PermianProjectQ3_2022       C3              C3  ...              151.0           1.0              PlugAndPerf
      82  PermianProjectQ3_2022       C3              C3  ...              153.0           1.0              PlugAndPerf
      83  PermianProjectQ3_2022       C3              C3  ...              143.0           1.0              PlugAndPerf
      84  PermianProjectQ3_2022       C3              C3  ...              153.0           1.0              PlugAndPerf
      85  PermianProjectQ3_2022       P1              P1  ...                NaN           NaN                     None 
      ```

### Run development Orchid tutorials

- Prepare to run tutorials
    - If you have not already done so,
      [configure the Orchid Python API to find the Orchid installation](#configure-the-orchid-python-api)
    - You **must**
      [configure the Orchid Python API to find the Orchid training data](#configure-the-orchid-training-data)
    - Navigate to `/path/to/repo`
    - If orchid-python-api is installed in the virtual environment,
        - Run `python ./copy_orchid_tutorials.py` to copy the tutorials to the current directory
    - If orchid-python-api not (yet) installed,
        - Copy the tutorial notebooks to the orchid project repository root
          ```
          copy ./orchid_python_api/tutorials/*.ipynb </path/to/orchid_repo>
          ```
- Activate `poetry shell` if not activated

#### Run tutorial script

- Run the `dom_navigation_tutorial.py` script
    - Execute the command `python dom_navigation_tutorial.py`
    - Follow the on-screen messages to advance through the tutorial

#### Run tutorial notebook

- Open Jupyter by running `jupyter lab` in the shell
- Within Jupyter,
    - Run the notebook, `dom_navigation_tutorial.ipynb`
        1. Open the notebook in `jupyter`
        2. Run each cell of the notebook. Typically, this process involves
            - Read the instructions or comments preceding the code cell(s)
            - Observe the result of executing the code

### Run installed Orchid tutorials

If testing against an Orchid release, [Install Orchid release](#install-orchid-release)

- Prepare to run tutorials
    - If you have not already done so,
      [configure the Orchid Python API to find the Orchid installation](#configure-the-orchid-python-api)
    - You **must**
      [configure the Orchid Python API to find the Orchid training data](#configure-the-orchid-training-data)
    - If you are testing a `pipenv` virtual environment or a `conda` environment
        - Navigate to the directory associated with the virtual environment
        - If necessary, activate the virtual environment.
        - Run `copy_orchid_tutorials`.
        - If the executable reports that it skipped files, repeat the command with an additional argument:  
          `copy_orchid_tutorials --overwrite`
        - Verify that the current directory has one tutorial notebooks:
            - `dom_navigation_tutorial.ipynb`
        - Verify that the current directory has one tutorial scripts:
            - `dom_navigation_tutorial.py`
    - If you are testing a `poetry` virtual environment
        - If orchid-python-api is installed in the virtual environment,
            - Run `python ./copy_orchid_tutorials.py` to copy the tutorials to the current directory
        - If orchid-python-api not (yet) installed,
            - Copy the tutorial notebooks to the orchid project repository root
              ```
              copy ./orchid_python_api/tutorials/*.ipynb </path/to/orchid_repo>
              ```

#### Run tutorial script

- Run the `dom_navigation_tutorial.py` script
    - Execute the command `python dom_navigation_tutorial.py`
    - Follow the on-screen messages to advance through the tutorial

#### Run tutorial notebook

- Open Jupyter by running `jupyter lab` in the shell
- Within Jupyter,
    - Run the notebook, `dom_navigation_tutorial.ipynb`
        1. Open the notebook in `jupyter`
        2. Run each cell of the notebook. Typically, this process involves
            - Read the instructions or comments preceding the code cell(s)
            - Observe the result of executing the code

### Generate requirements file

To generate a `requirements.txt` file,

- Navigate to the repository root
- Activate the virtualenv (run `poetry shell`)
- Run the command 
  ```
  poetry export --without-hashes -f requirements.txt --output requirements.txt
  ```

#### Test the requirements file in  a pipenv virtual environment

To test the generated requirements file using a `pipenv` virtual environment,

- [Create a new, clean virtualenv](#create-a-new-clean-virtualenv)
- In a Powershell window, navigate to the directory of the new virtualenv
- Activate the virtualenv (run `pipenv shell`)
- Install the package requirements by running 
  ```
  pip install -r /path/to/repo/requirements.txt
  ```
  If you see an error when executing this command, see 
  [require hashes error when installing dependencies](#require-hashes-error-when-installing-dependencies)
  for possible resolutions.
- Execute the command, `pip list --local`. 
  - If you have `git-bash` installed, you may be able to use the `less` command to search for package names;
    for example, by executing the following command and searching by entering `/<package_name>` at the prompt (':')

    ```
    pip list --local | & 'C:\Program Files\Git\usr\bin\less.exe'
    ```

Sample the package list. You should see output like the following (but with different version numbers)

| Package    | Version |
|------------|---------|
| jupyterlab | 2.3.2   |
| matplotlib | 3.5.1   |
| numpy      | 1.22.0  |
| pandas     | 1.3.5   |
| scipy      | 1.6.1   |

#### Test the requirements file in  a conda environment

To test the generated requirements file using a `conda` environment,

- [Create a clean conda environment](#create-a-clean-conda-environment)
- In an Anaconda Powershell window, navigate to the directory of the test environment
- Activate the environment by running `conda activate orchid`
- If you are using `pip` to manage packages in your environment:
  - Install the package requirements by running:
    - `pip install -r /path/to/repo/requirements.txt`
  - Execute the command:
    - `pip list --local`
  - If you have `git-bash` installed, you may be able to use the `less` command to search for package names;
    for example, by executing the following command and searching by entering `/<package_name>` at the prompt (':')

    ```
    pip list --local | & 'C:\Program Files\Git\usr\bin\less.exe'
    ```

Sample the package list. You should see output like the following (but with different version numbers)

| Package    | Version |
|------------|---------|
| jupyterlab | 2.3.2   |
| matplotlib | 3.5.1   |
| numpy      | 1.22.0  |
| pandas     | 1.3.5   |
| scipy      | 1.6.1   |

### Generate documentation

- Navigate to the repository root within your virtual development environment
- If necessary, activate the virtual environment by executing `poetry shell`
- Change to the `docs` directory by executing `chdir docs`
- Clean the build directory by executing `make.bat clean`
- Ensure that the `_build` directory is clean by executing `gci _build`
- Generate the latest documentation by executing `make.bat html`
- If you see a warning message like, "WARNING: html_static_path entry '_static' does not exist", you can ignore it
- Resolve any other warnings or errors
- Sample the documentation by opening the file, `/path-to/repository/docs/_build/html/index.html`, and navigating the
  generated documentation to ensure it is correct. Specifically, check for **new** classes and methods and ensure we
  have generated documentation for these items. 
- If necessary, correct any errors and repeat the "clean, make html and test" steps.

## Possible installation errors and resolutions

### Package not installed from TestPyPI

Because TestPyPI is **not** a complete replacement for PyPi, when installing you may encounter an error
stating that a package version is unavailable. For example,

> pip install --index-url https://test.pypi.org/simple/ orchid-python-api
> Looking in indexes: https://test.pypi.org/simple/
> Collecting orchid-python-api
>  Downloading https://test-files.pythonhosted.org/packages/90/89/cf9fd41f8dea07ae54898cc6b6951280d4509e55caec703d4b540a57135a/orchid_python_api-2020.4.232-py3-none-any.whl (55 kB)
>     |████████████████████████████████| 55 kB 622 kB/s
> ERROR: Could not find a version that satisfies the requirement numpy==1.19.0 (from orchid-python-api) (from versions 1.9.3)
> ERROR: No matching distribution found for numpy==1.19.0 (from orchid-python-api)

We have seen this issue occur for:
- `NumPy`
- `DateTimeRange`

The workaround for this issue is to:

- [Install a local distribution](#install-local-package) **but do not**

    - Run the tests

  This action will install all the dependent packages available on your workstation.

- Remove orchid by running the command, `pip uninstall orchid-python-api <version>` where `<version>` is
  replaced by a version identifier like, '2020.4.232'.
- Verify that `orchid-python-api` is uninstalled by either:
    - Execute `pip list --local`
    - Verify that `orchid-pyhon-api` is **not** present
- Or by:
    - Executing `pip list --local | select-string "orchid-python-api"` and observing no lines

Then repeat the command, `pip install --index-url https://test.pypi.org/simple/ orchid-python-api`.

### Pip reports resolution impossible

#### Incompatible pip and packaging

It is possible that you see the following error:

> ERROR: Cannot install orchid-python-api==2020.4.151, orchid-python-api==2020.4.151.post1,
> orchid-python-api==2020.4.191, orchid-python-api==2020.4.232, orchid-python-api==2020.4.361,
> orchid-python-api==2020.4.459, orchid-python-api==2020.4.595, orchid-python-api==2020.4.690 and
> orchid-python-api==2021.1.399 because these package versions have conflicting dependencies.
>
> The conflict is caused by:                                                                                          
>    orchid-python-api 2021.1.399 depends on packaging<21.0 and >=20.9
>    orchid-python-api 2020.4.690 depends on deal<4.0.0 and >=3.9.0
>    orchid-python-api 2020.4.595 depends on toolz==0.10.0
>    orchid-python-api 2020.4.459 depends on toolz==0.10.0
>    orchid-python-api 2020.4.361 depends on toolz==0.10.0
>    orchid-python-api 2020.4.232 depends on toolz==0.10.0
>    orchid-python-api 2020.4.191 depends on toolz==0.10.0
>    orchid-python-api 2020.4.151.post1 depends on toolz==0.10.0
>    orchid-python-api 2020.4.151 depends on toolz==0.10.0
>
> To fix this you could try to:
> 1. loosen the range of package versions you've specified
> 2. remove package versions to allow pip attempt to solve the dependency conflict

> ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/user_guide/#fixing-conflicting-dependencies

Here are possible resolutions.
- From the [open pypa issue 2364](https://github.com/pypa/pipenv/issues/2364)
  > I don’t think Pipenv did anything here, and I even filed #1884 specifically because it’s not very
  > convenient to upgrade them. IIRC there is some code to explicitly prevent Pipenv from touching them during
  > installation. Maybe you can try pipenv run pip install setuptools<=38.5.2 and see if pipenv install
  > updates it? Also you may want to check how they are locked in Pipfile.lock.
- Try the resolutions from [Package not installed from TestPyPI](#package-not-installed-from-testpypi)
  
### Require hashes error when installing dependencies

`pipenv` may report an error similar to the following when attempting to install required packages using a 
`requirements.txt` file generated by `poetry`:

```
ERROR: In --require-hashes mode, all requirements must have their versions pinned with ==. These do not:
    cffi>=1.0.1 from https://files.pythonhosted.org/packages/b6/15/a50bf922c5f025665a9671c5ef063c3f384303d422f6b1d3134510cc044e/cffi-1.15.0-cp38-cp38-win_amd64.whl#sha256=181dee03b1170ff1969489acf1c26533710231c58f95534e3edac87fff06c443
    (from argon2-cffi-bindings==21.2.0->-r C:\src\orchid-python-api\requirements.txt (line 4))
```

Based on these three `poetry` posts:

- [Poetry issue 3472](https://github.com/python-poetry/poetry/issues/3472)
- [Export requirements.txt error](https://debugah.com/pip-install-poetry-export-requirements-txt-error-error-in-require-hashes-mode-all-requirements-must-have-their-versions-pinned-with-these-do-not-cffi1-1-from-https-19552/)
- [Incorrect requirements for transitive dependencies](https://issueexplorer.com/issue/python-poetry/poetry/4719)

And a number of `pip` posts, for example, [Pip Issue 9243](https://github.com/pypa/pip/issues/9243), the root
issue seems to be a change in the `pip` resolver introduced in 2020 that has not yet been resolved.

Some suggested workarounds are:

- Do not include hashes in the generated `requirements.txt` file by using the `--without-hashes` option to
  the export command; that is, `poetry export --without-hashes -f requirements.txt --output requirements.txt`
- Downgrading `pip` to a version earlier than 20.3. For example, by executing the command 
  `python -m pip install --upgrade pip=20.2.4`

Since we do not typically use `requirements.txt` to install `orchid_python_api` dependencies, the 
Orchid Python API development team is ignoring this issue for `pipenv` but is testing its generated
requirements file using `conda`.

## Configure the Orchid Python API

The Orchid Python API requires a licensed Orchid installation on your workstation. Depending on the details of
the installation, you may need to configure the Orchid Python API to refer to different locations.

### Using the fallback configuration

If you installed the latest version Orchid using the installation defaults, and you installed the
`orchid-python-api` using the [step-by-step pipenv install](./README.md#step-by-step-pipenv-install) or
using the [step-by-step conda install](./README.md#step-by-step-conda-install), you need to
take **no** additional steps to configure the Orchid Python API to find this installation. For your
information, the default installation location is, `%ProgramFiles%\Reveal Energy Services\Orchid`. The Orchid
Python API uses the API version to find and use the required Orchid Python API assemblies.

### Using an environment variable

This mechanism is perhaps the easiest procedure to create an Orchid Python API configuration that changes 
rarely and is available to all your tools. It works best with a system restart. (Environment variables can be 
made available for a narrow set of tools on your system or available to all your tools depending on arcane
technical rules that you need not understand.) 

To use environment variables to configure the Orchid Python API, you will need to create the environment
variable `ORCHID_ROOT` and set its value to the path of the `PythonApiLibs` directory beneath the Orchid
installation directory. (For your information, the `PythonApiLibs` directory containing the version-specific
Orchid binary and configuration files should be in a subdirectory like 
`ORCHID_ROOT/Orchid-2020.4.232/PythonApiLibs` when you accept the installation defaults.) 

This section assumes you want to create a long-term configuration that survives a system restart and is
available to all your tools. Symbolically, this document will refer to the directory containing the binaries
required by the Orchid Python API as `/path-to/orchid/version/python-api-libs`. 

To create the required environment variable, enter the search term "environment variables" in the Windows-10 
search box and select the item named, "Edit environment variables for your account." The system will then 
present you with the "Environment Variables" dialog. Under the section named "User variables for 
<your.username>", click the "New" button. In the "Variable name" text box, enter "ORCHID_ROOT". (These two 
words are separated by the underscore symbol.)

Navigate to the "Variable Value" text box. Click the "Browse Directory" button to select the directory into
which Orchid is installed, `/path-to/orchid/version/python-api-libs`. This action pastes the directory
name into the "Variable Value" text box. Verify that the directory is correct, and then click "OK". Verify
that you see the name `ORCHID_ROOT` with the correct value in the "User variables for <your.username>" list.
Finally, click "OK" to dismiss the "Environment Variables" dialog.

Although you have created the `ORCHID_ROOT` environment variable with the appropriate value, only "new" opened
tools can use that variable. However, the details of "new" is technical and may not correspond to what you
expect. If you understand these details, you can jump to 
[Verify Installation](./README.md#verify-installation). If you are not confident of these details, restart
your system before proceeding to [Verify Installation](./README.md#verify-installation).

### Using a configuration file

Another option to configure the Orchid Python API is by creating a configuration file. A configuration file is
easier to change than an environment variable and does not require a system restart to work best. However, it
requires more knowledge and work on your part. In general, a configuration file is better if your requirements
change "often". For example, if you are working with multiple, side-by-side Orchid versions and Orchid Python 
API versions, you may find it faster and easier to create a configuration file once and change it as you 
change Orchid / Orchid Python API versions. 

To use a file to configure the Orchid Python API, you will need to create a configuration file named 
`python_api.yaml` and set the value of the `orchid` > `root` key to the path of the `PythonApiLibs` directory
beneath the Orchid installation directory. (For your information, the `PythonApiLibs` directory containing the
version-specific Orchid binary and configuration files should be in a subdirectory like 
`ORCHID_ROOT/Orchid-2020.4.232/PythonApiLibs` when you accept the installation defaults.)

Symbolically, this document will refer to the directory containing the binaries required by the 
Orchid Python API as `/path-to/orchid/version/python-api-libs`. 

To create a configuration file used by the Orchid Python API, you must:

- Create the directory, `/path/to/home-directory/.orchid`, where `/path/to/home-directory` is a symbolic
  reference to your home directory.
- Create the file, `python_api.yaml` in `/path/to/home-directory/.orchid`.

Technically, the format of the file is `YAML` ("YAML Ain't Markup Language"), a "human friendly data
serialization standard". (For technical details, visit [the website](https://yaml.org/). For a gentler
introduction, visit [the Wikipedia entry](https://en.wikipedia.org/wiki/YAML) or read / watch on of the many
`YAML` introductions / tutorials.)

Because these articles describe `YAML` generally, they **do not** describe the details of the `YAML` document
expected by the Orchid Python API. We, however, distribute an example file name `python_api.yaml.example` in
each installed `orchid-python-api` package. Assuming you created a virtual environment as described in
the [step-by-step pipenv install](./README.md#step-by-step-pipenv-install) or the
[step-by-step conda install](./README.md#step-by-step-conda-install) section, you can find this example file,
`python_api.yaml.example`, in the directory,
`/path/to/orchid-virtualenv/Lib/site-packages/orchid_python_api/examples`. 

To use this configuration file as an example:

- If this file is not already in the expected location, copy the file. For example, assuming the symbolic names
  referenced above, execute
  ```
  copy /path/to/orchid-virtualenv/Lib/site-packages/orchid_python_api/examples/python_api.yaml.example /path/to/home-directory/.orchid/python_api.yaml
  ```
- Edit the copied file, `/path/to/home-directory/.orchid/python_api.yaml`, using your favorite **text** editor.

The example file, contains comments, introduced by a leading octothorpe character (#, number sign, or hash),
that describe the information expected by the Orchid Python API. In summary, you'll need to provide a value
for the `orchid` > `root` key that contains (symbolically), `/path-to/orchid/version/python-api-libs`.

If you want to ensure your configuration is correct,
[view the Orchid API configuration details](#view-orchid-configuration-details).

## Configure the Orchid training data

Using the Orchid Python API **requires** a licensed Orchid installation on your workstation. However,
to use the example Jupyter notebooks or scripts, you must configure the Orchid Python API to find the
Orchid training data.

### Using an environment variable

This mechanism is perhaps the easiest procedure to create an Orchid Python API configuration that changes 
rarely and is available to all your tools. It works best with a system restart. (Environment variables can be 
made available for a narrow set of tools on your system or available to all your tools depending on arcane
technical rules that you need not understand.) 

To use environment variables to configure the Orchid Python API to find the Orchid training data, you will 
need to create the environment variable `ORCHID_TRAINING_DATA` and set its value to the location of the Orchid 
training data.

This document assumes you want to create a long-term configuration that survives a system restart and is 
available to all your tools. Symbolically, this document will refer to the Orchid training data location as
`/path-to/orchid/training-data`. 

To create the required environment variable, enter the search term "environment variables" in the Windows-10 
search box and select the item named, "Edit environment variables for your account." The system will then 
present your with the "Environment Variables" dialog. Under the section named "User variables for 
<your.username>", click the "New" button. In the "Variable name" text box, enter "ORCHID_TRAINING_DATA".
(These three words are separated by the underscore symbol.)

Navigate to the "Variable Value" text box. Click the "Browse Directory" button to select the directory 
containing the Orchid training data, `/path-to/orchid/training-data`. This action pastes the directory name
into the "Variable Value" text box. Verify that the directory is correct, and then click "OK". Verify that
you see the name `ORCHID_TRAINING_DATA` with the correct value in the "User variables for <your.username>"
list. Finally, click "OK" to dismiss the "Environment Variables" dialog.

Although you have now created the `ORCHID_TRAINING_DATA` environment variable with the appropriate value,
only "new" tools can now use that variable. However, the details of "new" is technical and may not correspond
to your what you expect. If you understand these details, you can jump to
[Verify Installation](./README.md#verify-installation). If you are not confident of these details, restart
your system before proceeding to [Verify Installation](./README.md#verify-installation).

### Using a configuration file

Another option to configure the Orchid Python API to find the Orchid training data is by creating a 
configuration file. A configuration file is easier to change than an environment variable and does not require 
a system restart to work best. However, it requires more knowledge and work on your part. In general, a 
configuration file is better if your requirements change "often". For example, if you are working with 
multiple, side-by-side Orchid versions and Orchid Python API versions, you may find it faster and easier to
create a configuration file once and change it as you change Orchid / Orchid Python API versions or training
data locations.

To create a configuration file used by the Orchid Python API, you create a file named `python_api.yaml`
and put it in the directory, `/path/to/home-directory/.orchid`, where `/path/to/home-directory` is a 
symbolic reference to your home directory. Technically, the format of the file is `YAML` ("YAML Ain't Markup
Language"), a "human friendly data serialization standard". (For technical details, visit 
[the website](https://yaml.org/). For a gentler introduction, visit 
[the Wikipedia entry](https://en.wikipedia.org/wiki/YAML) or read / watch on of the many `YAML` 
introductions / tutorials.)

Because these articles describe `YAML` generally, they **do not** describe the details of the `YAML` document
expected by the Orchid Python API. We, however, distribute an example file name `python_api.yaml.example` in
each installed `orchid-python-api` package. Assuming you created a virtual environment as described in
the [step-by-step pipenv install](./README.md#step-by-step-pipenv-install) or the 
[step-by-step conda install](./README.md#step-by-step-conda-install), you can find this example file,
`python_api.yaml.example`, in the directory,
`/path/to/orchid-virtualenv/Lib/site-packages/orchid_python_api/examples`.

To use this configuration file as an example:

- If this file is not already in the expected location, copy the file. For example, assuming the symbolic names
  referenced above, execute
  ```
  copy /path/to/orchid-virtualenv/Lib/site-packages/orchid_python_api/examples/python_api.yaml.example /path/to/home-directory/.orchid/python_api.yaml`
  ```
  
- Edit the copied file, `/path/to/home-directory/.orchid/python_api.yaml`, using your favorite **text** editor.

The example file, contains comments, introduced by a leading octothorpe character (#, number sign, or hash),
that describe the information expected by the Orchid Python API. In summary, you'll need to provide a value
for the 'orchid' > 'training_data' key that contains the pathname of the directory containing the Orchid
training data files.

If you want to ensure your configuration is correct,
[view the Orchid API configuration details](#view-orchid-configuration-details).

## View Orchid Configuration Details

To "debug" the Orchid Python API configuration, perform the following steps:

- Change to the directory associated with your Python virtual environment.
- If necessary, activate the virtual environment.
- Within that virtual environment, invoke Python. It is important to create a new REPL so that you start with
  a "clean" environment.
- Within the Python REPL, execute the following commands.

  ```
  import logging
  logging.basicConfig(level=logging.DEBUG)
  import orchid
  ```
  
Enabling logging **before** importing is critical. If you have already imported `orchid`, the simplest
solution is to close this REPL and create another, "clean" REPL.

You should see output like the following:

```
DEBUG:orchid.configuration:fallback configuration={'orchid': {'root': 'C:\\Program Files\\Reveal Energy Services\\Orchid\\Orchid-2020.4.361'}}
DEBUG:orchid.configuration:file configuration={'orchid': {'root': 'c:\\path-to\\bin\\x64\\Debug\\net48', 'training_data ': 'c:\\path-to\\installed-training-data'}}
DEBUG:orchid.configuration:environment configuration = {'orchid': {'root': 'c:\\another\\path-to\bin\\x64\\Debug\\net48'}}
DEBUG:orchid.configuration:result configuration={'orchid': {'root': 'c:\\another\\path-to\bin\\x64\\Debug\\net48'}}
```

This output describes four details of the configuration.

| Configuration | Explanation                                                            |
|---------------|------------------------------------------------------------------------|
| fallback      | The always available configuration (may be empty)                      |
| file          | The configuration specified in your configuration file (may be empty)  |
| environment   | The configuration specified using environment variables (may be empty) | 
| result        | The configuration used by the Orchid Python API (should not be empty)  |

## Managing multiple code repositories

As mentioned earlier, the source code for the Orchid Python API exists in two synchronized repositories. The "working"
repository for most developers is the
[Azure DevOps PythonApi repository](https://reveal-energy.visualstudio.com/ImageFrac/_git/PythonApi). However, for 
developers (and "readers") outside of Reveal, the primary repository is
[the GitHub repository](https://github.com/Reveal-Energy-Services/orchid-python-api). Two repositories introduces an
additional task for developers: coordinating these repositories so that they are "synchronized". 

The key issue with two repositories, similar to managing a fork of an existing repository is coordinating branches with
the same name on two different remotes. Specifically, both the Azure DevOps repository and the GitHub repository have
branches named:

- `master`
- `develop`

As a developer, whenever you work with these branches locally, you must be very aware of which remote branch you are
tracking. The author currently tracks these branches as follows:

- The remote, `origin`, refers to the GitHub repository
- The remote, `reveal-energy`, refers to the Azure DevOps repository
- Local `develop` tracks the remote `origin/develop`
- Local `develop-reveal` tracks `reveal-energy/develop`
- Local `master` tracks the remote `origin/master`
- Local `master-reveal` tracks `reveal-energy/master`

Other developers prefer the "opposite" mapping

- The remote, `origin`, refers to the Azure DevOps repository
- The remote, `github`, refers to the GitHub repository
- Local `develop` tracks the remote `origin/develop`
- A local branch named, for example, `develop-githib` tracks `github/develop`
- Local `master` tracks the remote `origin/master`
- Local `master-github` tracks `github/master`

The author does not believe that either mapping provides a better developer experience; the key is to be **aware** of 
the mapping and the required coordination.

We have two coordination points: completing PR requests and publishing a release. When we complete a PR, it is valuable
to ensure that this latest "accepted" code is available from either Azure DevOps or from GitHub. Consequently, when we
complete a PR, we must ensure that:

- `github/develop` and `reveal-energy/develop` refer to the same commit.

For the author's set up, this involves:

- Merging the latest commits to `reveal-energy/develop` to the local `develop-reveal` 
- Merging local `develop-reveal` into local `develop`
- Push changes from local `develop` to remote `origin/develop` (GitHub)

If you are using the "opposite" mapping, one must

- Merging the latest commits to `origin/develop` to the local `develop`
- Merging local `develop` into local `develop-github`
- Push changes from local `develop-github` to remote `github/develop` (GitHub)

The second coordination point is a release. In addition to the previous steps (since the last step before publishing to
a distribution to PyPI is completing a PR), we must ensure that:

- `github/master` and `reveal-energy/master` refer to the same commit (which should be the same as `github/develop` and
  `reveal-energy/develop`).

To ensure this end state, one must use similar steps to synchronizing a completed PR. For the author's set up, this
coordination involves:

- Merge the local `develop` commits to local `master`
- Push local `master` to remote `origin/master` (GitHub)
- Merge the local `master` to local `master-reveal`
- Push changes to `master-reveal` to remote `reveal-energy/master` (Azure DevOps)

If you are using the "opposite" mapping, one must

- Merge the local `develop` commits to local `master`
- Push local `master` to remote `origin/master` (Azure DevOps)
- Merge the local `master` to local `master-github`
- Push changes to local `master-github` to remote `github/master` (GitHub)

Finally, when pushing the tags for a release one must also use a similar process. For example, if we have tagged a
commit with `2022.2.234` and one is using the author's set up, one must:

- Push the tags to the remote `origin` (GitHub) using the command, `git push origin 2022.2.234`
- Push the tags to the remote `reveal-energy` (Azure DevOps) using the command, `git push reveal-energy 2022.2.234`

For the "opposite" set up, one must:

- Push the tags to the remote `origin` (Azure DevOps) using the command, `git push origin 2022.2.234`
- Push the tags to the remote `github` (GitHub) using the command, `git push 'github' 2022.2.234`

If you have questions about synchronizing these repositories, please talk to other members of the team. Strongly
consider using "pair programming" during this synchronization process to avoid "fast" but more error-prone habits.
Since this synchronization is **not** part of the typical Orchid workflow, this synchronization is outside all of our
typical GitHub / Azure DevOps experience.

## Contribute

To contribute to this project, follow our typical development process:

- Clone this repository using [HTTPS](https://github.com/Reveal-Energy-Services/orchid-python-api.git) or
  [SSH](git@github.com:Reveal-Energy-Services/orchid-python-api.git)
- Create a branch for you work typically branching from `develop`
- Make changes on your branch
- Push your branch to the Azure DevOps repository
- Create a pull request to have others review your branch
- When approved, complete your pull request to merge you work onto `develop`

Although not enforced automatically, any changes will need to pass all existing unit and integration tests.
In addition, it is expected that any changes will add **both** unit and integration tests before the pull 
request can be completed.
