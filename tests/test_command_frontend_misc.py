import unittest, os, sys
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from click import exceptions

# the module being tested
from undo.commands.frontend import frontend_misc

runner = CliRunner()

class FrontendMiscTestCase(unittest.TestCase):
    def setUp(self):
        pass

    @patch("subprocess.run")
    @patch("typer.secho")
    def test_command_frontend_misc_run(self, mock_echo, mock_run):
        context = Path("tests/testproject")
        r = frontend_misc.run(context)

        # there are actually three cuz the first is some generic user feedback
        args, kwargs = mock_echo.call_args_list[1]
        self.assertIn("npm run dev", args[0], "Should've printed the run command")

        args, kwargs = mock_run.call_args
        a = args[0]
        self.assertEqual(a, "npm run dev", "Should've npm run dev")