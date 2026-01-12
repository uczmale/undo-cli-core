import unittest, os
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from click import exceptions

# project specific imports
from undo.utils import dir_utils

# project specific imports
from undo import cli

# the module being tested
from undo.commands.function import function

runner = CliRunner(mix_stderr=False)


class FunctionTestCase(unittest.TestCase):
    def setUp(self):
        # start the session in a specific, mock project location
        self.reset_cwd = os.getcwd()
        os.chdir("tests/testproject")

    def tearDown(self):
        # reset to where we ran this test from, since we chdir a bunch
        os.chdir(self.reset_cwd)

    @patch("subprocess.run")
    @patch.dict(os.environ, { "UNDO_ROOT_CHECK_FILE": ".mock" })
    def test_command_function_command_wrapper(self, mock_run):
        r = runner.invoke(cli.app,
                            ["function", "wrapper", "api",
                                "--routes", "/undo",
                                "--port", "8080"],
                            catch_exceptions=False)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        echo_tests = [
            "Function undo-api-publisher selected..",
            "\tsource .venv/bin/activate",
            "wrapper.py 8080 /undo\n"
        ]
        for t in echo_tests:
            self.assertIn(t, r.output, "Should have spat out text based on input")


    @patch("subprocess.run")
    @patch.dict(os.environ, { "UNDO_ROOT_CHECK_FILE": ".mock" })
    def test_command_function_command_properties(self, mock_run):
        r = runner.invoke(cli.app,
                            ["function", "properties", "event"],
                            catch_exceptions=False)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        test_terms = [
            "Function undo-event-publisher selected..",
            "\tfunction_name=undo-event",
            "\tfunction_version=1.2.3"
        ]
        for term in test_terms:
            self.assertIn(term, r.output, "Should have spat out text based on input")
