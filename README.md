# Introduction 

This project defines the implementation of the Python API for Orchid.

Specifically, the `orchid` package exposes the Orchid API to Python applications and the Python REPL.
Additionally, this project contains a number of demonstration applications:

- `plot_trajectories.py`
- `plot_time_series.py`
- `plot_treatment.py`
- `summarize_treatment.py`

The first three applications plot:

- The well trajectories for a project
- The time series for a project
- The treatment curves (pressure, slurry rate and concentration) for a specific stage of a well in a project

The last application demonstrates using `orchid` package and Pandas to perform some typical treatment calculations.

# Getting Started

## Overview

To understand the structure of the code, the [development README](./docs_dev/README.md) contains an overview of 
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

## End-user Usage

TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test Locally

TODO: Describe and show how to build your code and run the tests. 

# Contribute

To contribute to this project, follow our typical development process:

- Clone this repository using [HTTPS](https://reveal-energy.visualstudio.com/ImageFrac/_git/PythonApi) or
  [SSH](reveal-energy@vs-ssh.visualstudio.com:v3/reveal-energy/ImageFrac/PythonApi)
- Create a branch for you work typically branching from `develop`
- Make changes on your branch
- Push your branch to the Azure DevOps repository
- Create a pull request to have have others review your branch
- When approved, complete your pull request to merge you work onto `develop`

Although not yet enforced, any changes will need to pass all unit tests and any integration tests that are part of the
project before the pull request can be completed.

If you want to learn more about creating good readme files then refer the following
[guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also
seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
