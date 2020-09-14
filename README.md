# Introduction 

This project defines the implementation of the Python API for Orchid*.

(*Orchid in a mark of Revel Energy Services. Inc.)

Specifically, the `orchid` package exposes the Orchid API to Python applications and the Python REPL.
Additionally, this project installs four examples in the `examples` directory of the `orchid-python-api`
package:

- `plot_trajectories.ipynb`
- `plot_monitor_curves.ipynb`
- `plot_treatment.ipynb`
- `completion_analysis.ipynb`

The first three notebooks plot:

- The well trajectories for a project
- The monitor curves for a project
- The treatment curves (pressure, slurry rate and concentration) for a specific stage of a well in a project
 
Additionally, the notebook, `completion_analysis.ipynb`, provides a more detailed analysis of the completion
performed on two different wells in a project.
 
To use these examples, you may want to invoke the commands

- `copy_orchid_examples`
- `use_orchid_test_data`

Use the first command to copy the example files into your an optionally specified (virtual environment)
directory. (The default destination is your current working directory.) Use the second command to change the
examples in an optionally specified directory (your current directory) to refer to the specified location of 
the Orchid test data files. Both commands are 
    - Command line commands that run in a console / terminal
    - Support a help flag (`-h` / `--help`) to provide you with help on running the commands

# Getting Started

## End-user Usage

We recommend the use of virtual environments to use the Orchid Python API. This choice avoids putting 
Orchid-specific-packages in your system Python environment.

You have several options to create and manage virtual environments: `venv`, `pipenv`, `poetry`, and `conda`.
The `venv ` is available as a standard Python package and is a spartan tool to manage environments. `poetry`
is a tool targeting developers but can be used by end-users. Our recommended tool is `pipenv`. It provides a 
good balance between `venv ` and `poetry`. Remember, both `pipenv` and `poetry` must be installed in your 
Python environment separately from Python itself, but can be installed using `pip`. Finally, `conda` supports 
the creation of virtual environments, but assumes that you have installed a Python distribution using Anaconda
or miniconda. We will not describe `conda` further.

Using any of `pipenv`, `venv` or `poetry`, your first step is to create a directory for *your* project. Then, 
change into *your* project directory.

### Pipenv

- Create virtual environment (using Powershell (recommended) or Windows console)
    - `</path/to/python-3.7/installation/Scripts/pipenv install`
    - `pipenv shell`
    - `pip install orchid-python-api`
        
## Venv

- Create a directory to host all your virtual environments. A good choice is 
`</path/to/user/directory/.virtualenvs>`. In subsequent steps, I will use the directory, 
`</path/to/user/directory/.virtualenvs/orchid-python-api>`, to hold my virtual environment.
- Create virtual environment (using Powershell (recommended) or Windows console)
    - Create an empty virtual environment
        - `</path/to/python-3.7/installation/python -m venv </path/to/user/directory/.virtualenvs/orchid-python-api>`
    - Activate the virtual environment
        - `</path/to/user/directory/.virtualenvs/orchid-python-api/bin/Activate.ps1>` in Powershell or
        - `</path/to/user/directory/.virtualenvs/orchid-python-api/bin/Activate.bat>` in Windows console
    - Install orchid-python-api
        - `pip install orchid-python-api`
        
### Poetry

- Create a an empty virtual environment (using Powershell (recommended) or Windows console) by executing,
    `poetry env use </path/to/python-3.7-executable>`
- Install packages into the empty virtual environment
    - `poetry shell`
    - `pip install orchid-python-api`

## Development Overview

To understand the structure of the code, the file, `./docs_dev/README.md`, contains an overview of 
the application / package design.

## Development

To avoid "contamination" of other python environments, we use [pipenv](https://pipenv.pypa.io/en/stable/) to manage our
development (and target) environment. (See this [tutorial](https://realpython.com/pipenv-guide/) for a gentler
introduction to using `pipenv`.)

### Install Python

To use `pipenv`, you'll may need to perform up to three steps. First, if you do not have python **3** installed, you'll need to
install it. To determine if python 3 is installed:

- In the Windows 10, search bar, type "add or remove programs".
- On the "Apps & features" page, search for "python"

If you see an item named "Python 3.x", you have python 3 installed.

If Python is not installed, follow [these instructions](https://docs.python.org/3/using/windows.html). To ensure access
from the command line, be sure to select the "Add Python 3.x to PATH" option on the [installer start
page](https://docs.python.org/3/_images/win_installer.png). 

### Ensure Command Line Access To Python

Although you may be able perform development without command line access using, for example, `PyCharm`, many
instructions, including these instructions, will assume command line access. To verify command line access:

- Open a command prompt
- Type the command `python -V`

You should see a result like "Python 3.x".

### Install Pipenv

To install `pipenv`:

- Open a command prompt
- Invoke the command `pip install pipenv`.

This will install the `pipenv` package in your system python installation. (Note that python 3.x, by default, installs
`pip`. And if Python is available from the command line, `pip` will also be available from the command line.)

### Create development environment

To create the development environment using `pipenv`:

- Clone the `PyhonApi` repository into a directory on your workstation. For convenience, we'll call that directory
  `$PYTHON_API_ROOT`.
- Open a command prompt
- Navigate to the `$PYTHON_API_ROOT`directory by executing `cd $PYTHON_API_ROOT`
- Execute the command `pipenv install --ignore-pipfile`

For an explanation of this last command, see either the [reference documentation](https://pipenv.pypa.io/en/stable/) or
the [tutorial](https://realpython.com/pipenv-guide/).

Wait patiently. This command will install **both** the run-time and development-time packages to support changing and
running in your local, development environment.

#### Alternative development environments

Many people, including this author, use an IDE for python development. It is not necessary, but provides a number of
conveniences for development.

To use [PyCharm](https://www.jetbrains.com/pycharm/) from [JetBrains](https://www.jetbrains.com/):

- Start `PyCharm`
- Select `Open an existing project`.
- Select the `$PYTHON_API_ROOT` directory

(I believe it will detect your `Pipfile` / `Pipfile.lock` and use that to configure the project settings correctly.)

To use Visual Studio, a recommended tool is [Python Tools for Visual
Studio](https://visualstudio.microsoft.com/vs/features/python/). The author assumes you are familiar with (or will
become familiar with) this tool and its capabilities.

If you prefer a "lighter" development environment, consider [Visual Studio
Code](https://code.visualstudio.com/docs/languages/python). Again, the author assumes you are familiar with (or will
become familiar) with this tool and its capabilities.

Finally, many, many, many other tools exist to support Python ranging from "editors" (Emacs and Vim) to tools like Atom
and Sublime. You can most likely use whatever editing environment you are familiar with (or, like me, more than one).
Remember the recommendation from the book, _The Pragmatic Programmer_: "Find one editor and stick to it."

# Build and Test Locally

TODO: Describe and show how to build your code and run the tests. 

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
    - `invoke --help` (for general help on `invoke`)
    - `invoke --list` (to list the available tasks)
    - `invoke poetry.venv.remove --help` (for help on a specific command listed)
to perform these tasks.

## Update dependencies

To update the project dependencies:

- [Create a new, clean virtualenv](#create-a-new-clean-virtualenv)
- In a Powershell window, navigate to the directory of the new virtualenv
- Activate the virtualenv (run `poetry shell`)
- Update the dependencies
    - Run `poetry update`

## Update API version

- Open the file `orchid/VERSION` for editing
- Change the version in the file to the updated value. Copying it is safest if at all possible. The log files
  print the version number as part of the banner which eases the ability to copy that version number. (Beware, 
  currently a version containing anything but numeric values will cause the Orchid Python API to fail 
  at run-time. During the beta program, we are manually removing the "-beta" suffix from the version.)
- Open the file `pyproject.toml` for editing.
- Copy the version number from `orchid/VERSION` to the value of the `version` key of the file. (The automated
  task, `update-ver`, visible when running `invoke --list` performs this task automatically. However, as a 
  "side-effect", this task *removes* all the comment lines from the `.toml` file. The author does not 
  believe that we are ready to lose all those reminders yet.)

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
        
### Install local package

- [Create a new, clean virtualenv](#create-a-new-clean-virtualenv)
- In a Powershell window, navigate to the directory of the new virtualenv
- Activate the virtualenv (run `pipenv shell`)
- Install the package distribution by running `pip install </path/to/package-distribution>`

- Install "jupyter lab" by running `pip install jupyterlab`
Finally, [Run all examples](#run-orchid-examples)

Finally, [Run orchid examples](#run-orchid-examples).

## Publish to TestPyPI

## Publish to PyPI

## Common tasks

### Create a new, clean virtualenv

These instructions assume you have created a test virtual directory using `pipenv`. This tool is simpler to
use than `poetry` but does not have the convenient development features of `poetry`. Further, these 
instructions assume that your test directory is something like `<path/to/inst/orchid/pipenv>`
- Navigate to the repository root
- Remove the existing virtualenv if any
    - Run `invoke pipenv.venv.remove --dirname=<path/to/inst/orchid/pipenv>`. NOTE: If no such virtualenv 
    exists, running this task will produce a message like:
    
    >> invoke pipenv.venv.remove --dirname=/c/inst/orchid/pipenv
    >> No virtualenv has been created for this project yet!
    >> Aborted!
                                                                                                                                                                                                                    
- Create a new skeleton virtual environment
    - Run `invoke pipenv.venv.create --dirname=<path/to/inst/orchid/pipenv>`.

### Run all orchid tests

To run all orchid tests
- Run unit tests
- Run acceptance (feature) tests
- [Run examples](#run-orchid-examples)

### Run orchid examples

- Prepare to run examples
    - If you are testing a `pipenv` virtual environment
        - Navigate to the directory associated with the virtual environment
        - Run `python </path/to/virtualenv/Lib/site-packages/copy_orchid_examples.py`
        - If the script reports that it skipped notebooks, repeat the command with an additional argument:  
          `python </path/to/virtualenv/Lib/site-packages/copy_orchid_examples.py --overwrite`
        - Verify that the current directory has four notebooks:
            - `plot_trajectories.ipynb`
            - `plot_monitor_curves.ipynb`
            - `plot_treatment.ipynb`
            - `completion_analysis.ipynb`
        - The notebooks, as installed, contain a symbolic reference to the Orchid training data. Change this
          symbolic reference to an actual reference by:
            - Either running 
              `python </path/to/virtualenv/Lib/site-packages/use_orchid_test_data.py </path/to/training-data>`
            - Or by editing each notebook replacing the symbolic strings, "/path/to", with a concrete path to
              your installed training data.
    - If you are testing a `poetry` virtual environment
        - If orchid-python-api is installed in the virtual environment,
            - Run `python ./copy_orchid_examples.py` to copy the examples to the current directory
            - Run `python ./use_orchid_test_data.py </path/to/integration-test-data>`
        - If orchid-python-api not (yet) installed,
            - Copy the example notebooks to the orchid project repository root
                - `copy ./orchid_python_api/examples/*.ipynb </path/to/orchid_repo>`
           - Run `python ./use_orchid_test_data.py </path/to/integration-test-data>`
- Activate `poetry shell` if not activated
- Open Jupyter by running `jupyter lab` in the shell
- Within Jupyter,
    Successfully run notebook, `plot_trajectories.ipynb`
        1. Open notebook
        2. Run all cells of notebook
        3. Wait patiently
        4. Verify that no exceptions occurred
    - Repeat for remaining notebooks:
        - `plot_monitor_curves.ipynb`
        - `plot_treatment.ipynb`
        - `completion_analysis.ipynb`

# Contribute

To contribute to this project, follow our typical development process:

- Clone this repository using [HTTPS](https://github.com/Reveal-Energy-Services/orchid-python-api.git) or
  [SSH](git@github.com:Reveal-Energy-Services/orchid-python-api.git)
- Create a branch for you work typically branching from `develop`
- Make changes on your branch
- Push your branch to the Azure DevOps repository
- Create a pull request to have have others review your branch
- When approved, complete your pull request to merge you work onto `develop`

Although not yet enforced, any changes will need to pass all unit tests and any integration tests that are part of the
project before the pull request can be completed.
