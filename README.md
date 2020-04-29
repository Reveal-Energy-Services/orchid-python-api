# Introduction 

This project defines the implementation of the Python API for ImageFrac4.

Specifically, the `image_frac` package exposes the ImageFrac4 API to Python applications and the Python REPL.
Additionally, this project contains a number of demonstration applications:

- `plot_trajectories.py`
- `plot_time_series.py`
- `plot_treatment.py`
- `summarize_treatment.py`

The first three applications plot:

- The well trajectories for a project
- The time series for a project
- The treatment curves (pressure, slurry rate and concentration) for a specific stage of a well in a project

The last application demonstrates using `image_frac` package and Pandas to perform some typical treatment calculations.

# Getting Started

## Development

## End-user Usage

TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test

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
