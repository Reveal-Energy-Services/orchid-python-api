#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = "orchid"
DESCRIPTION = "Defines the Python API for Orchid*. (*Orchid is a mark of Reveal Energy Services, Inc.)"
URL = "https://github.com/me/myproject"
EMAIL = "support@reveal-energy.com"
AUTHOR = "Reveal Energy Services, Inc."
REQUIRES_PYTHON = ">=3.7.7"
VERSION = ""

# What packages are required for this module to be executed?
REQUIRED = [
    # 'requests', 'maya', 'records',
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(include=["orchid", "tests"]),
    # Including the `jupyter_demo` notebook is merely for example.
    scripts=['plot_trajectories.py', 'plot_monitor_pressures.py', 'plot_treatment.py', 'jupyter_demo.ipynb'],
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    # install_requires=REQUIRED,
    install_requires=[
        "astroid==2.4.2; python_version >= '3.5'",
        "attrs==19.3.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "cycler==0.10.0",
        "deal==3.9.0",
        "hypothesis==5.19.3; python_full_version >= '3.5.2'",
        "kiwisolver==1.2.0; python_version >= '3.6'",
        "lazy-object-proxy==1.4.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "matplotlib==3.2.2",
        "more-itertools==8.4.0",
        "numpy==1.19.0",
        "pandas==1.0.5",
        "pycparser==2.20; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "python-dateutil==2.8.1",
        "pythonnet==2.5.1",
        "pytz==2020.1",
        "pyyaml==5.3.1",
        "scipy==1.5.1; python_version >= '3.6'",
        "seaborn==0.10.1",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "sortedcontainers==2.2.2",
        "toolz==0.10.0",
        "typed-ast==1.4.1; python_version < '3.8' and implementation_name == 'cpython'",
        "typeguard==2.9.1; python_full_version >= '3.5.3'",
        "typing-extensions==3.7.4.2",
        "vaa==0.2.1",
        "vectormath==0.2.2",
        "wrapt==1.12.1",
    ],
    dependency_links=[],
    # extras_require=EXTRAS,
    extras_require={},
    include_package_data=True,
    license="Apache-2.0",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",
        "Intended Audience :: Other Audience",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache-2.0 License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    # $ setup.py publish support.
    cmdclass={"upload": UploadCommand,},
)
