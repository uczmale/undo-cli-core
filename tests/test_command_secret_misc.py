import unittest, os, sys
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from click import exceptions

# project specific imports
from undo.utils import test_utils

# the module being tested
from undo.commands.secret import secret_misc

runner = CliRunner()

class SecretMiscTestCase(unittest.TestCase):
    def setUp(self):
        pass

    @patch("typer.secho")
    def test_command_secret_misc_generate_secret(self, mock_echo):
        chars = 20
        r = secret_misc.generate_secret(chars)

        echo_tests = [ "\nPassword generated!" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        self.assertEqual(len(r), chars, "Should've generated pasword of right length")