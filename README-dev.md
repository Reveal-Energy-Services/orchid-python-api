# Introduction 

(This document targets people *developing* the Orchid Python. If you plan to simply use the API, look at 
`README.md` instead.)

This project defines the implementation of the Python API for Orchid*.

(*Orchid in a mark of Revel Energy Services. Inc.)

Specifically, the `orchid` package exposes the Orchid API to Python applications and the Python REPL.
Additionally, this project includes four examples in the `examples` directory of the `orchid-python-api`
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

## Development Overview

To understand the structure of the code, the file, `./docs_dev/README.md`, in the source repository, contains an
overview of the application / package design.

## Development

We use a virtual environment to make changes to and to test the Orchid Python API. This choice avoids putting
Orchid-specific-packages in your system Python environment and avoids version conflicts between the Orchid
Python API and other packages.

Although the Python ecosystem supports several tools to create and manage virtual environments, development 
uses `poetry` because of its support for developer tasks such as packaging and publishing. For information on 
`poetry` see [the poetry documentation](https://python-poetry.org/docs/).

### Install Poetry

To use `poetry`, you may need to perform up to three steps. First, if you do not have python **3** installed,
you need to install it. To determine if python 3 is installed:

- In the Windows 10, search bar, type "add or remove programs".
- On the "Apps & features" page, search for "python"
- If you see an item named "Python 3.x", you have python 3 installed.

If Python is not installed, follow [these instructions](https://docs.python.org/3/using/windows.html). To 
ensure access from the command line, be sure to select the "Add Python 3.x to PATH" option on the
[installer start page](https://docs.python.org/3/_images/win_installer.png). 

### Ensure Command Line Access To Python

Although you may be able perform development without command line access using, for example, `PyCharm`, many
instructions, including these instructions, will assume command line access. To verify command line access:

- Open a command prompt
- Type the command `python -V`

You should see a result like "Python 3.x".

### Install poetry

To install `poetry`:

- Open a command prompt
- Invoke the command `pip install poetry`.

This will install the `poetry` package in your system python installation. (Note that python 3.x, by default,
installs `pip`. If Python is available from the command line, `pip` will also be available from the command
line.)

### Create development environment

To create the development environment using `poetry`:

- Clone the `PyhonApi` repository into a directory on your workstation. For convenience, we'll call that
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

To use Visual Studio, a recommended tool is [Python Tools for Visual
Studio](https://visualstudio.microsoft.com/vs/features/python/). The author assumes you are familiar with (or
will become familiar with) this tool and its capabilities.

If you prefer a "lighter" development environment, consider [Visual Studio
Code](https://code.visualstudio.com/docs/languages/python). Again, the author assumes you are familiar with (or will
become familiar) with this tool and its capabilities.

Finally, many, many, many other tools exist to support Python ranging from "editors" (Emacs and Vim) to tools like Atom
and Sublime. You can most likely use whatever editing environment you are familiar with (or, like me, more than one).
Remember the recommendation from the book, _The Pragmatic Programmer_: "Find one editor and stick to it."

# Build and Test Locally

## Package a distribution

- Open a terminal and navigate to the project repository root.
- Remove the `dist` directory if present.
- Invoke the command `invoke poetry.package`
- Review the built packages. Ensure that:
    - The version number is correct.
    - The build process builds both 
        - A source distribution (`.tar.gz` file)
        - A binary (wheel) distribution (`.whl` file)
        
## Install local package

- [Create a new, clean virtualenv](#create-a-new-clean-virtualenv)
- In a Powershell window, navigate to the directory of the new virtualenv
- Activate the virtualenv (run `pipenv shell`)
- Install the package distribution by running `pip install </path/to/package-distribution>`

- Install "jupyter lab" by running `pip install jupyterlab`

Finally, [Run orchid examples](#run-installed-orchid-examples).

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
- [Run examples](#run-development-orchid-examples)

### Run development orchid examples

- Prepare to run examples
    - Navigate to `/path/to/repo`
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

### Run installed orchid examples

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
