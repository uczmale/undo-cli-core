import unittest, os, sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from click import exceptions

# project specific imports
from undo.utils import test_utils

# the module being tested
from undo.commands.secret import secret

runner = CliRunner()

class SecretTestCase(unittest.TestCase):
    def setUp(self):
        pass

    @patch("subprocess.run")
    def test_command_secret_command_generate(self, mock_run):
        r = runner.invoke(secret.app,
                            ["generate", "-c", "100"],
                            catch_exceptions=False)
        # print(r.output)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        echo_tests = [
            "\nPassword generated!"
        ]
        for t in echo_tests:
            self.assertIn(t, r.output, "Should have spat out text based on input")