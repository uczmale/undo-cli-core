import unittest, os, sys, shutil
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
        # start the session in a specific, mock project location
        self.reset_cwd = os.getcwd()
        os.chdir("tests/testproject")

    def tearDown(self):
        # reset to where we ran this test from, since we chdir a bunch
        os.chdir(self.reset_cwd)

    @patch("subprocess.run")
    def test_command_secret_command_encrypt(self, mock_run):
        secret_path = "functions/undo_api_publisher/secrets/UNDO_SECRET"
        r = runner.invoke(secret.app,
                            ["encrypt", "-s", "cli_test_password",
                             "-f", secret_path, "-o"],
                            catch_exceptions=False)
        # print(r.output)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        echo_tests = [
            "The secret 'cl*****rd' has been encrypted",
           f"the location '{secret_path}'"
        ]
        for t in echo_tests:
            self.assertIn(t, r.output, "Should have spat out text based on input")

        self.assertTrue(Path(secret_path).exists(), "Should've created the secret file")
        Path(secret_path).exists() and shutil.rmtree(Path(secret_path).parent)


    @patch("subprocess.run")
    def test_command_secret_command_encrypt_prompt(self, mock_run):
        secret_path = "functions/undo_api_publisher/secrets/UNDO_PROMPT_SECRET"
        Path(secret_path).exists() and shutil.rmtree(Path(secret_path).parent)
        r = runner.invoke(secret.app,
                            ["encrypt", "-f", secret_path],
                            input="encrypt_secret_input",
                            catch_exceptions=False)
        # print(r.output)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        echo_tests = [
            "The secret 'en*****ut' has been encrypted",
           f"the location '{secret_path}'"
        ]
        for t in echo_tests:
            self.assertIn(t, r.output, "Should have spat out text based on input")

        self.assertTrue(Path(secret_path).exists(), "Should've created the secret file")
        Path(secret_path).exists() and shutil.rmtree(Path(secret_path).parent)


    @patch("subprocess.run")
    def test_command_secret_command_decrypt(self, mock_run):
        secret_path = "database/secrets/db_local_password_user"
        r = runner.invoke(secret.app,
                            ["decrypt", "-f", secret_path, "-r"],
                            catch_exceptions=False)
        # print(r.output)

        t = "vault_previously_encrypted"
        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")
        self.assertEqual(r.output, t, "Should have returned just the actual secret")


    @patch("subprocess.run")
    def test_command_secret_command_generate(self, mock_run):
        r = runner.invoke(secret.app,
                            ["generate", "-l", "100"],
                            catch_exceptions=False)
        # print(r.output)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        echo_tests = [
            "\nSecret generated!"
        ]
        for t in echo_tests:
            self.assertIn(t, r.output, "Should have spat out text based on input")