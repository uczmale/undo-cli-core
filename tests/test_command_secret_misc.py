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
        # start the session in a specific, mock project location
        self.reset_cwd = os.getcwd()
        os.chdir("tests/testproject")

    def tearDown(self):
        # reset to where we ran this test from, since we chdir a bunch
        os.chdir(self.reset_cwd)


    @patch("typer.secho")
    def test_command_secret_misc_generate_secret(self, mock_echo):
        chars = 20
        r = secret_misc.generate_secret(chars)

        echo_tests = [ "\nSecret generated!" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        self.assertEqual(len(r), chars, "Should've generated pasword of right length")


    @patch("typer.secho")
    def test_command_secret_misc_decrypt_secret(self, mock_echo):
        secret_path = "database/secrets/db_local_password_user"
        r = secret_misc.decrypt_secret(secret_path)

        t = "vault_previously_encrypted"
        echo_tests = [ "\nSecret decrypted!", f"\t{t}" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        self.assertEqual(r, t, "Should've return decrypted secret")


    @patch("typer.secho")
    def test_command_secret_misc_decrypt_secret_raw(self, mock_echo):
        secret_path = "database/secrets/db_local_password_user"
        raw = True
        r = secret_misc.decrypt_secret(secret_path, raw=raw)

        t = "vault_previously_encrypted"
        echo_tests = [ t ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        self.assertEqual(r, t, "Should've return decrypted secret")