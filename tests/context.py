# -*- coding: utf-8 -*-

import sys
import os

# PyCharm reports a warning for the following imports. This warning occurs because I have an import statement
# at the top-level of a module after other executable code.
#
# The reason for this choice is to ensure that our unit tests **do not** find either our specific modules or
# modules with the same names in our installed Python packages.
#
# We accomplish this goal by inserting the parent directory of this file **at the beginning** of our system
# path. Since Python stops after finding the first instance of the named module, we ensure that we find the
# modules in this project before finding any others.

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
