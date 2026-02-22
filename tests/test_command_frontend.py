import unittest, os, sys
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from click import exceptions

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
        r = runner.invoke(frontend.app,
                            ["run", "undo-app"],
                            catch_exceptions=False)
        # print(r.output)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        echo_tests = [
            "Frontend undo-app selected..",
            "\tnpm run dev"
        ]
        for t in echo_tests:
            self.assertIn(t, r.output, "Should have spat out text based on input")