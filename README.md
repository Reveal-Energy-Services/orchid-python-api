# Introduction 

This project defines the implementation of the Python API for Orchid*.

(*Orchid in a mark of Revel Energy Services. Inc.)

Specifically, the `orchid` package exposes the Orchid API to Python applications and the Python REPL.

# Getting Started

## Create a virtual environment

# Examples

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


## End-user preparation

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

We recommend the use of `pipenv`. This environment hides a number of details involved in managing a virtualenv
and yet provides a fairly simple interface. We will assume in this document that you are using `pipenv`.

# Step-by-step install

- Install python 3.7 by following [these instructions](https://docs.python.org/3/using/windows.html). To 
  ensure access from the command line, be sure to select the "Add Python 3.x to PATH" option on the
  [installer start page](https://docs.python.org/3/_images/win_installer.png). 
- Installing `pipenv` by following the 
  [install documentation](https://pipenv.pypa.io/en/latest/install/#installing-pipenv).
- Open a console using either `powershell` or the Windows console.
- Create a directory for the virtual environment. We will symbolically call it `/path/to/orchid-virtualenv`.
- Change the current working directory to by `chdir /path/to/orchid-virtualenv`.
- Create an empty virtual environment by running `pipenv install`.
- Activate the virtual environment by running `pipenv shell`
- Install orchid by running `pip install orchid-python-api`.
- Optionally install jupyter lab or jupyter notebook if you wish to use these tools to explore.

# Verify installation

## Jupyter lab

- In your activated virtual environment, run `jupyter lab` to open a browser tab.
- In the first cell, enter `import orchid`.
- Run the cell.
- Wait patiently.

The import should complete with no errors.

## Python REPL

- In your activated virtual environment, run `python` to open a REPL.
- Enter `import orchid`.
- Wait patiently.

The import should complete with no errors.

# Run orchid examples

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
- Activate your virtual environment by `pipenv shell` if not already activated
- Open Jupyter by running `jupyter lab` in the shell
- Within Jupyter,
    Run the notebook, `plot_trajectories.ipynb`
        1. Open notebook
        2. Run all cells of notebook
        3. Wait patiently
        4. Verify that no exceptions occurred
    - Repeat for remaining notebooks:
        - `plot_monitor_curves.ipynb`
        - `plot_treatment.ipynb`
        - `completion_analysis.ipynb`
