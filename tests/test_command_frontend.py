import unittest, os, sys
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from click import exceptions

# project specific imports
from undo.utils import dir_utils

# project specific imports
from undo import cli

# the module being tested
from undo.commands.frontend import frontend

runner = CliRunner()

class FrontendTestCase(unittest.TestCase):
    def setUp(self):
        # start the session in a specific, mock project location
        self.reset_cwd = os.getcwd()
        os.chdir("tests/testproject")
        
    def tearDown(self):
        # reset to where we ran this test from, since we chdir a bunch
        os.chdir(self.reset_cwd)

    @patch("subprocess.run")
    @patch.dict(os.environ, { "UNDO_ROOT_CHECK_FILE": ".mock" })
    def test_command_frontend_command_run(self, mock_run):
        r = runner.invoke(cli.app,
                            ["frontend", "run", "undo-app" ],
                            catch_exceptions=False)
        print(r.output)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        echo_tests = [
            "Frontend undo-app selected..",
            "\tnpm run dev"
        ]
        for t in echo_tests:
            self.assertIn(t, r.output, "Should have spat out text based on input")


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_command_frontend_command_run_frontend(self, mock_echo, mock_run):
        context = Path("tests/testproject")
        r = frontend.run(context)

        # there are actually three cuz the first is some generic user feedback
        args, kwargs = mock_echo.call_args_list[1]
        self.assertIn("npm run dev", args[0], "Should've printed the run command")

        args, kwargs = mock_run.call_args
        a = args[0]
        self.assertEqual(a, "npm run dev", "Should've npm run dev")