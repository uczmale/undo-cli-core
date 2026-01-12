import unittest, os
from pathlib import Path
from unittest.mock import patch
import tempfile
from click import exceptions

# test imports
from tests import assert_utils 

# project specific imports
from undo.utils import dir_utils

# the module being tested
from undo.commands.function import function_misc


class FunctionMiscTestCase(unittest.TestCase):
    def setUp(self):
        # start the session in the mock project folder
        self.reset_cwd = os.getcwd()
        os.chdir("tests/testproject")
        
    def tearDown(self):
        # reset to where we ran this test from, since we chdir a bunch
        os.chdir(self.reset_cwd)

    @patch("typer.secho")
    def test_command_function_properties(self, mockery):
        context = Path("functions/undo_api_publisher")
        r = function_misc.properties(context)

        t = {
            "name": "undo-api-publisher",
            "version": "0.1.0"
        }
        self.assertEqual(r, t, "Should've captured vars, inc. overwrite and ignore")

        # there are actually three cuz the first is some generic user feedback
        args, kwargs = mockery.call_args_list[1]
        self.assertIn("undo-api-publisher", args[0], "Should've printed the func name")

        args, kwargs = mockery.call_args_list[2]
        self.assertIn("0.1.0", args[0], "Shouldn've printed the function version")