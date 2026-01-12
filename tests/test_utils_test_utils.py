import os
from pathlib import Path
import unittest
from unittest.mock import patch
from click import exceptions

# the module being tested
from undo.utils import test_utils

class TestUtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_utils_test_utils_print_buffer(self):
        with test_utils.PrintBuffer() as p:
            print("catch me!", end="")

        self.assertEqual(p.output, "catch me!", "Should've caught it, innit")
