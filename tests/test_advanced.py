# -*- coding: utf-8 -*-

from .context import image_frac

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(image_frac.hmm())


if __name__ == '__main__':
    unittest.main()
