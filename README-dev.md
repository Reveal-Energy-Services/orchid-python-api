# Introduction 

(This document targets people *developing* the Orchid Python. If you plan to simply use the API, look at 
`README.md` instead.)

This project defines the implementation of the Python API for Orchid*.

(*Orchid is a mark of Reveal Energy Services, Inc.)

Specifically, the `orchid` package makes Orchid features available to Python applications and to the Python
REPL. Additionally, this project includes five examples in the `examples` directory of the `orchid-python-api`
package:

- `plot_trajectories.ipynb`
- `plot_monitor_curves.ipynb`
- `plot_treatment.ipynb`
- `completion_analysis.ipynb`
- `volume_2_first_response.ipynb`

The first three notebooks plot:

- The well trajectories for a project
- The monitor curves for a project
- The treatment curves (pressure, slurry rate and concentration) for a specific stage of a well in a project
 
The notebook, `completion_analysis.ipynb`, provides a more detailed analysis of the completion
performed on two different wells in a project. Finally, the notebook, `volume_2_first_response.ipynb`, uses
typical Python packages to calculate derivatives in order to calculate the fluid volume pumped before the 
first response.
 
To use these examples: 

- You may need to 
  [configure the Orchid Python API to find the Orchid installation](#configure-the-orchid-python-api)
- You **must** 
  [configure the Orchid Python API to find the Orchid training data](#configure-the-orchid-training-data)
- You may want to invoke the command, `copy_orchid_examples`

    This command copies the example files into an optionally specified (virtual environment) directory. (The 
    default destination is your current working directory.) Note that this command is a command-line script 
    that runs in a console or terminal. Additionally, this command supports a help flag (`-h` / `--help`) to 
    provide you with help on running this command.

# Getting Started

## Development Overview

To understand the structure of the code, the file, `./docs_dev/README.md`, in the source repository, contains 
an overview of the application / package design.

## Development

We use a virtual environment to make changes to and to test the Orchid Python API. This choice avoids putting
Orchid-specific-packages in your system Python environment and avoids version conflicts between the Orchid
Python API and other packages.

Although the Python ecosystem supports several tools to create and manage virtual environments, development 
uses `poetry` because of its support for developer tasks such as packaging and publishing. For information on 
`poetry` see [the poetry documentation](https://python-poetry.org/docs/).

### Install Python

Install python 3.8 by following [these instructions](https://docs.python.org/3/using/windows.html). To ensure
access from the command line, be sure to select the "Add Python 3.x to PATH" option on the
[installer start page](https://docs.python.org/3/_images/win_installer.png). 

### Ensure Command Line Access To Python

Although you may be able to perform development without command line access using, for example, `PyCharm`, many
instructions, including these instructions, will assume command line access. To verify command line access:

- Open a command prompt
- Type the command `python -V`

You should see a result like "Python 3.x".

### Install Poetry

To use `poetry`, you may need to perform up to three steps. First, if you do not have python **3** installed,
you need to install it. To determine if python 3 is installed:

- In the Windows 10, search bar, type "add or remove programs".
- On the "Apps & features" page, search for "python"
- If you see an item named "Python 3.x", you have python 3 installed.

To install `poetry`:

- Open a command prompt
- Invoke the command `pip install poetry`.

This will install the `poetry` package in your system python installation. (Note that python 3.x, by default,
installs `pip`. If Python is available from the command line, `pip` will also be available from the command
line.)

### Create development environment

To create the development environment using `poetry`:

- Clone the `PythonApi` repository into a directory on your workstation. For convenience, we'll call that
  directory `/path/to/repo`.
- Open a command prompt
- Navigate to the `/path/to/repo`
- Execute the command `poetry install`

Wait patiently. This command will install **both** the run-time and development-time packages to support 
changing and running in your local, development environment.

#### Alternative development environments

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

##### Sharing PyCharm configurations

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

# Build and test locally

## Package a distribution

- Open a terminal and navigate to the project repository root.
- Remove the `dist` directory if present.
- Invoke the command `invoke poetry.package`
- Review the built packages. Ensure that:
    - The version number is correct.
    - The build process builds both 
        - A source distribution (`.tar.gz` file)
        - A binary (wheel) distribution (`.whl` file)
    - The distribution contains the correct `ReleaseNotes.md` For example one can view the file contents by
      using the command `vim dist/<package>.tar.gz` or by using an tool like 7-zip.
        
## Install local package

- [Create a new, clean virtualenv](#create-a-new-clean-virtualenv)
- In a Powershell window, navigate to the directory of the new virtualenv
- Activate the virtualenv (run `pipenv shell`)
- Install the package distribution by running `pip install </path/to/package-distribution>`
- [Ensure installation of correct Orchid version](#ensure-correct-orchid)
- [Configure the Orchid Python API to find the Orchid installation](#configure-the-orchid-python-api)

Finally, [Run Orchid examples](#run-installed-orchid-examples).

# Publish a release

Publishing a release has a number of general steps. These steps are optional except for 
[the last step](#publish-to-pypi). Here are the steps:

- [Update dependencies](#update-dependencies)
- [Update API version](#update-api-version)
- [Build and test locally](#build-and-test-locally)
- [Publish to TestPyPI](#publish-to-testpypi)
- [Publish to PyPI](#publish-to-pypi)

Throughout these tasks, you will repeatedly [Run common tasks](#common-tasks)

Remember that the file, `tasks.py`, defines many common tasks. Be sure to use commands like:
    - `invoke --help` for general help on `invoke`
    - `invoke --list` to list the available tasks
    - `invoke poetry.venv.remove --help` (for help on a specific command listed)
to perform these tasks.

## Update dependencies

To update the project dependencies:

- [Create a new, clean development virtualenv](#create-a-new-clean-development-virtualenv)
- In a Powershell window, navigate to the directory of the new virtualenv
- Activate the virtualenv (run `poetry shell`)
- Update the dependencies
    - Run `poetry update`

## Update API version

- Open the file `orchid/VERSION` for editing
- Change the version in the file to the updated value. The safest way to update the value is copying the 
  value if at all possible. The log files print the version number in the banner at the beginning of each
  execution of Orchid. 

  (NOTE: the Orchid Python API only uses
  the [release segment](https://www.python.org/dev/peps/pep-0440/#public-version-identifiers) of its version. Further,
  for the release segment, it only supports three parts:
  the [major](https://packaging.pypa.io/en/latest/version.html#packaging.version.Version.major)
  , [minor](https://packaging.pypa.io/en/latest/version.html#packaging.version.Version.minor),
  and [micro](https://packaging.pypa.io/en/latest/version.html#packaging.version.Version.micro) (aka, maintenance) parts
  of a [release](https://packaging.pypa.io/en/latest/version.html#packaging.version.Version.micro) or version.
  Consequently, only include three components in the release specification in `orchid/VERSION`.)
    
- Open the file `pyproject.toml` for editing.
- Copy the version number from `orchid/VERSION` to the value of the `version` key of the file. (The automated
  task, `update-ver`, visible when running `invoke --list` performs this task automatically. However, as a 
  "side effect", this task *removes* all the comment lines from the `.toml` file. The author does not 
  believe that we are ready to lose all those reminders yet.)
  
## Publish to TestPyPI

The steps to publish to TestPyPi are very similar to the steps for 
[Build and install locally](#build-and-test-locally) and for [Publish to PyPI](#publish-to-pypi). For an 
introduction to the process (but some different steps), review the 
[Python Packaging Guide](https://packaging.python.org/guides/using-testpypi/).

- [Package a distribution](#package-a-distribution)

### Configure TestPyPI as a `poetry` repository

- Determine if TestPyPI is already configured by running either:
    - `invoke poetry.config.list`
    - `poetry config --list`
- Examine the output for the key, `repositories.test-pypi.url`
- If key is present, `poetry` is already configured so skip to 
  [Publish distribution to TestPyP](#publish-distribution-to-testpypi)
- To configure the TestPyPI repository, run either
    - `invoke poetry.config.test-pypi` or
    - `poetry config repositories.test-pypi https://test.pypi.org/legacy/`
    
Once configured, you will also need to configure the API token for the TestPyPI website. Because the API 
token is a security token, the author is unaware of any way to examine if the token has already been 
configured. However, configuring an already configured token **does not** cause an error. 

To generate an API token, complete the steps described at [PyPI help](https://pypi.org/help/#apitoken) but for
the TestPyPI website.

Once generated, add it to the `poetry` configuration by executing either:

- `invoke poetry.config.api-token -r test-pypi -t <token>` or
- `poetry config pypi-token.test-pypi <token>`
    
### Publish distribution to TestPyPI

To publish the distribution to TestPyPI execute either:

- `invoke poetry.publish test-pypi` or
- `poetry publish --repository=test-pypi`

Once published, test the published distribution by:

- [Create a new, clean virtualenv](#create-a-new-clean-virtualenv)
- In a Powershell window, navigate to the directory of the new virtualenv
- Activate the virtualenv (run `pipenv shell`)
- Install the package distribution by running the command, 
  `pip install --index-url https://test.pypi.org/simple/ orchid-python-api`. 
- [Run Orchid examples](#run-installed-orchid-examples).

If an error occurs, read the error message(s) and consult the section 
[Possible installation errors and resolutions](#possible-installation-errors-and-resolutions).
  
## Publish to PyPI

**Before** publishing to PyPI, ensure that:

- All outstanding PR's have been completed.
- You have merged all changes to the `develop` branch
- You have changed your current branch to the `develop` branch

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
- Install the package distribution by running the command, 
  `pip install orchid-python-api`. 
  
Finally, [Run Orchid examples](#run-installed-orchid-examples).
  
## Common tasks

### Ensure correct Orchid

By default, the Python API for Orchid expects to find the Orchid binaries in a specific location on your local
system. To ensure the correct version of Orchid is installed, 

- Navigate to the orchid installation directory, `$PROGRAMFILES\Reveal Energy Services\Orchid`
- List that directory
- You should see a directory named something like, `Orchid-<python-api-version>`, where `<python-api-version>` 
  is a symbolic reference for the version number in which you are interested.
- Navigate into the version specific information. For example, `Orchid-2020.4.232`
- You should see a directory like `PythonApiLibs`
- Navigate into this directory
- You should see files like:
    - `appSettings.json`
    - `Orchid.FractureDiagnostics.dll`
    - Many, many others
    
To make doubly certain, you could run `Orchid.Application.exe` and ensure that the application displays the 
correct version number in the main window title bar.

If it is not installed, you'll need to:

- Install the appropriate version from the [Web portal](https://portal.reveal-energy.com)
- Perhaps repeat these steps

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
      Python interpreter to use for  the environment (currently Python 3.8.7 for the Orchid Python API).

If using `python invoke`,

- Navigate to the repository root
- Remove the existing virtualenv if any
    - Run `invoke poetry.venv.remove --venv=<virtual-env>`. NOTE: If no such virtualenv exists, running this
      task will produce a message like:
    ```
    invoke poetry.venv.remove --dirname=c:/inst/orchid/pipenv
    No virtualenv has been created for this project yet!
    Aborted!
    ```
  
Delete any leftover files
- If present, delete all leftover files from the virtualenv directory.

Create a new skeleton virtual environment
  - Run `invoke poetry.venv.create`.
    
To test that you were successful,

- Navigate to the virtual environment directory if not there already
- Activate the virtualenv by executing, `poetry shell`
- Execute the command, `pip list --local`. You should see output like the following (but probably with
  different version numbers)

  ```
  Package    Version
  ---------- -------
  pip        20.1.1
  setuptools 46.4.0
  ```

### Create a new, clean virtualenv

These instructions assume you will create a test virtual directory using `pipenv`. This tool is simpler to
use than `poetry` but does not have the convenient development features of `poetry`. Further, these 
instructions assume that your test directory is something like `<path/to/inst/orchid/pipenv>`

If using the command line,

- Remove any existing virtual directory by:
    - Navigate to the root directory of the virtual environment.
    - Execute the command `pipenv --rm` to remove the virtual environment itself. NOTE: If no such virtualenv
      exists, running this command produces a message like:
     
      ```No virtualenv has been created for this project yet!```
      
    - Execute the command `del Pipfile Pipfile.lock` to remove the `pipenv` supporting files.
    - Remove any other files remaining in the virtual environment directory.
    
- Create a new, clean virtual environment by:
    - Execute the command `pipenv install --python=<python_ver>` where `python_ver` is the version of Python
    used by the Orchid Python API (currently 3.8.7).    

If using `python invoke`,

- Navigate to the repository root
- Remove the existing virtualenv if any
    - Run `invoke pipenv.venv.remove --dirname=<path/to/inst/orchid/pipenv>`. NOTE: If no such virtualenv 
    exists, running this task will produce a message like:
    
    ```
    invoke pipenv.venv.remove --dirname=c:/inst/orchid/pipenv
    No virtualenv has been created for this project yet!
    Aborted!
    ```
    
- If present, delete all leftover files from the virtualenv directory.
                                                                                                                                                                                                                    
- Create a new skeleton virtual environment
    - Run `invoke pipenv.venv.create --dirname=<path/to/inst/orchid/pipenv>`.
    
To test that you were successful,

- Navigate to the virtual environment directory if not there already
- Activate the virtualenv by executing, `pipenv shell`
- Execute the command, `pip list --local`. You should see output like the following (but probably different 
  version numbers)

  ```
  Package    Version
  ---------- -------
  pip        20.1.1
  setuptools 46.4.0
  wheel      0.34.2
  ```
    
### Run all orchid tests

To run all orchid tests
- Run unit tests
- Run acceptance (feature) tests
- [Run examples](#run-development-orchid-examples)

### Run development orchid examples

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
            - `copy ./orchid_python_api/examples/*.ipynb </path/to/orchid_repo>`
- Activate `poetry shell` if not activated
- Open Jupyter by running `jupyter lab` in the shell
- Within Jupyter,
    - Successfully run notebook, `plot_trajectories.ipynb`
        1. Open notebook
        2. Run all cells of notebook
        3. Wait patiently
        4. Verify that no exceptions occurred
    - Repeat for remaining notebooks:
        - `plot_monitor_curves.ipynb`
        - `plot_treatment.ipynb`
        - `completion_analysis.ipynb`
        - `volume_2_first_response.ipynb`

### Run installed Orchid examples

- Prepare to run examples
    - If you have not already done so, 
      [configure the Orchid Python API to find the Orchid installation](#configure-the-orchid-python-api)
    - You **must** 
      [configure the Orchid Python API to find the Orchid training data](#configure-the-orchid-training-data)
    - If you are testing a `pipenv` virtual environment
        - Navigate to the directory associated with the virtual environment
        - If necessary, activate the virtual environment.
        - Run `python </path/to/virtualenv/Lib/site-packages/copy_orchid_examples.py`. Be sure to specify 
          `python` to run the script with the version of python install in the virtual environment and **not**
          the system version of python.
        - If the script reports that it skipped notebooks, repeat the command with an additional argument:  
          `python </path/to/virtualenv/Lib/site-packages/copy_orchid_examples.py --overwrite`
        - Verify that the current directory has five notebooks:
            - `completion_analysis.ipynb`
            - `plot_monitor_curves.ipynb`
            - `plot_trajectories.ipynb`
            - `plot_treatment.ipynb`
            - `volume_2_first_response.ipynb`
    - If you are testing a `poetry` virtual environment
        - If orchid-python-api is installed in the virtual environment,
            - Run `python ./copy_orchid_examples.py` to copy the examples to the current directory
        - If orchid-python-api not (yet) installed,
            - Copy the example notebooks to the orchid project repository root
                - `copy ./orchid_python_api/examples/*.ipynb </path/to/orchid_repo>`
- Open Jupyter by running `jupyter lab` in the shell
- Within Jupyter,
    - Successfully run notebook, `plot_trajectories.ipynb`
        1. Open notebook
        2. Run all cells of notebook
        3. Wait patiently
        4. Verify that no exceptions occurred
    - Repeat for remaining notebooks:
        - `plot_monitor_curves.ipynb`
        - `plot_treatment.ipynb`
        - `completion_analysis.ipynb`
        - `volume_2_first_response.ipynb`

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

## Configure the Orchid Python API

The Orchid Python API requires a licensed Orchid installation on your workstation. Depending on the details of
the installation, you may need to configure the Orchid Python API to refer to different locations.

### Using the fallback configuration

If you installed the latest version Orchid using the installation defaults, and you installed the 
`orchid-python-api` , you need to take **no** additional steps to configure the Orchid Python API to find this
installation. For your information, the default installation location is,
`%ProgramFiles%\Reveal Energy Services\Orchid`. The Orchid Python API uses its version to find and use
the corresponding version of Orchid.

### Using an environment variable

This mechanism is perhaps the easiest procedure to create an Orchid Python API configuration that changes 
rarely and is available to all your tools. It works best with a system restart. (Environment variables can be 
made available for a narrow set of tools on your system or available to all your tools depending on arcane
technical rules that you need not understand.) 

To use environment variables to configure the Orchid Python API, you will need to create the environment 
variable `ORCHID_ROOT` and set its value to the root Orchid installation directory. (For your information, the
version-specific Orchid binary files, `.exe`'s and `.dll`'s should be in a subdirectory of `ORCHID_ROOT` 
with a name like `Orchid-2020.4.232`.) 

This document assumes you want to create a long-term configuration that survives a system restart and is 
available to all your tools. Symbolically, this document will refer to the root of the Orchid installation as
`/path/to/orchid-installation`. 

To create the required environment variable, enter the search term "environment variables" in the Windows-10 
search box and select the item named, "Edit environment variables for your account." The system will then 
present you with the "Environment Variables" dialog. Under the section named "User variables for 
<your.username>", click the "New" button. In the "Variable name" text box, enter "ORCHID_ROOT". (These two 
words are separated by the underscore symbol.)

Navigate to the "Variable Value" text box. Click the "Browse Directory" button to select the directory into 
which Orchid is installed, `/path/to/orchid-installation`. This will paste the directory name into the 
"Variable Value" text box. Verify that the directory is copied directly, and the click "OK". Verify that you
see the name `ORCHID_ROOT` with the correct value in the "User variables for <your.username>" list. Finally,
click "OK" to dismiss the "Environment Variables" dialog.

Although you have now created the `ORCHID_ROOT` environment variable with the appropriate value, "new" tools 
could now use that variable. However, the details of "new" is technical and may not correspond to what you
expect. If you understand these details, you can return to your original task.
If you are not confident of these details, restart your system before returning to your original task.

### Using a configuration file

Another option to configure the Orchid Python API is by creating a configuration file. A configuration file is
easier to change than an environment variable and does not require a system restart to work best. However, it
requires more knowledge and work on your part. In general, a configuration file is better if your requirements
change "often". For example, if you are working with multiple, side-by-side Orchid versions and Orchid Python 
API versions, you may find it faster and easier to create a configuration file once and change it as you 
change Orchid / Orchid Python API versions.

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
[Step-by step install](#step-by-step-install), you can find this example file, `python_api.yaml.example`, in
the directory, `/path/to/orchid-virtualenv/Lib/site-packages/orchid_python_api/examples`. 

To use this configuration file as an example:

- Copy the file to the expected location. For example, assuming the symbolic names referenced above, execute
  `copy /path/to/orchid-virtualenv/Lib/site-packages/orchid_python_api/examples/python_api.yaml.example
   /path/to/home-directory/.orchid/python_api.yaml`
- Edit the copied file, `/path/to/home-directory/.orchid/python_api.yaml`, using your favorite **text** editor.

The example file, contains comments, introduced by a leading octothorpe character (#, number sign, or hash), 
that describe the information expected by the Orchid Python API. In summary, you'll need to provide a value
for the 'orchid' > 'root' key that contains the pathname of the directory containing the Orchid binaries
corresponding to the installed version of the `orchid-python-api` package.

## Configure the Orchid training data

The Orchid Python API **requires** a licensed Orchid installation on your workstation. However, configuring
the Orchid Python API to find the Orchid training data is only needed to run the example Jupyter notebooks.

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
(These two words are separated by the underscore symbol.)

Navigate to the "Variable Value" text box. Click the "Browse Directory" button to select the directory 
containing the Orchid training data, `/path-to/orchid/training-data`. This action pastes the directory name
 into the "Variable Value" text box. Verify that the directory is correct, and the click "OK". Verify that you
see the name `ORCHID_TRAINING_DATA` with the correct value in the "User variables for <your.username>" list. 
Finally, click "OK" to dismiss the "Environment Variables" dialog.

Although you have now created the `ORCHID_ROOT` environment variable with the appropriate value, only "new"
tools can now use that variable. However, the details of "new" is technical and may not correspond to your 
what you expect. If you understand these details, you can return to your original task.
If you are not confident of these details, restart your system before returning to your original task.

### Using a configuration file

Another option to configure the Orchid Python API to find the Orchid training data is by creating a 
configuration file. A configuration file is easier to change than an environment variable and does not require 
a system restart to work best. However, it requires more knowledge and work on your part. In general, a 
configuration file is better if your requirements change "often". For example, if you are working with 
multiple, side-by-side Orchid versions and Orchid Python API versions, you may find it faster and easier to 
create a configuration file once and change it as you change Orchid / Orchid Python API versions.

To create a configuration file used by the Orchid Python API, you create a file named `python_api.yaml`
and put it in the directory, `/path/to/home-directory/.orchid`, where `/path/to/home-directory` is a 
symbolic reference to your home directory. Technically, the format of the file is `YAML` ("YAML Ain't Markup
Language"), a "human friendly data serialization standard". (For technical details, visit 
[the website](https://yaml.org/). For a gentler introduction, visit 
[the Wikipedia entry](https://en.wikipedia.org/wiki/YAML) or read / watch on of the many `YAML` 
introductions / tutorials.)

## View Orchid Configuration Details

To "debug" the Orchid Python API configuration, perform the following steps:

- Change to the directory associated with your Python virtual environment.
- If necessary, activate the virtual environment.
- Within that virtual environment, invoke Python. It is important to create a new REPL so that you start with
  a "clean" environment.
- Within the Python REPL, execute the following commands.
  ```
  import logging
  logging.basicConfi(level=logging.DEBUG)
  import orchid
  ```

Enabling logging **before** importing is critical. If you have already imported `orchid`, the simplest solution
is to close this REPL and create another, "clean" REPL.

You should see output like the following:

```
DEBUG:orchid.configuration:fallback configuration={'orchid': {'root': 'C:\\Program Files\\Reveal Energy Services\\Orchid\\Orchid-2020.4.361'}}
DEBUG:orchid.configuration:file configuration={'orchid': {'root': 'c:\\path-to\\bin\\x64\\Debug\\net48', 'training_data ': 'c:\\path-to\\installed-training-data'}}
DEBUG:orchid.configuration:environment configuration = {'orchid': {'root': 'c:\\another\\path-to\bin\\x64\\Debug\\net48'}}
DEBUG:orchid.configuration:result configuration={'orchid': {'root': 'c:\\another\\path-to\bin\\x64\\Debug\\net48'}}
```

This output describes four details of the configuration.

| Configuration | Explanation |
| ------------- | ----------- |
| result | The configuration used by the Orchid Python API |
| fallback | The always available configuration |
| file | The configuration specified in your configuration file |
| environment | The configuration specified using environment variables | 

# Contribute

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
