import os
from pathlib import Path
import unittest
from unittest.mock import patch
from click import exceptions
from ansible.parsing.vault import VaultLib

# project specific imports
from undo.utils import test_utils

# the module being tested
from undo.utils import secret_utils

class SecretUtilsTestCase(unittest.TestCase):
    def setUp(self):
        # start the session in the mock project folder
        self.reset_cwd = os.getcwd()
        os.chdir("tests/testproject")
        self.secret = Path(".vault/db_secret").read_text() # existing_secret_123

    def tearDown(self):
        # reset to where we ran this test from, since we chdir a bunch
        Path(".vault/db_secret").write_text(self.secret)
        os.chdir(self.reset_cwd)


    def test_utils_secret_utils_mask_secret(self):
        secret = "xyz_middle_middle_rpq"
        r = secret_utils.mask_secret(secret)

        self.assertEqual(r, "xy*****pq", "Should've masked all but the start and end")


    def test_utils_secret_utils_get_secret_encrypted(self):
        secret_path = Path("functions/undo_event_publisher/secrets/encrypted_secret")
        r = secret_utils.get_secret(secret_path)

        self.assertEqual(r, "encrypted_secret", "Should've returned 'encrypted' secret")


    def test_utils_secret_utils_get_secret_unencrypted(self):
        secret_path = Path("functions/undo_event_publisher/secrets/_unencrypted_secret")
        r = secret_utils.get_secret(secret_path, show_error=True)

        t = "unencrypted_secret"
        self.assertEqual(r, t, "Should've returned 'unencrypted' secret")


    def test_utils_secret_utils_get_secret_unencrypted_no_underscore(self):
        secret_path = Path("functions/undo_event_publisher/secrets/unencrypted_secret")
        r = secret_utils.get_secret(secret_path, show_error=True)

        t = "unencrypted_secret"
        self.assertEqual(r, t, "Should've returned 'unencrypted' secret")


    def test_utils_secret_utils_get_secret_not_exists(self):
        secret_path = Path("functions/undo_event_publisher/secrets/xyz")
        r = secret_utils.get_secret(secret_path)

        self.assertFalse(r, "Should've returned False as secret doesn't exist")


    @patch("typer.secho")
    def test_utils_secret_utils_get_secret_raise_error(self, mock_echo):
        secret_path = Path("functions/undo_event_publisher/secrets/xyz")
        
        with self.assertRaises(exceptions.Exit) as context:
            r = secret_utils.get_secret(secret_path, show_error=True)

        echo_tests = [ "Ruh-roh!", "No secret found", "secrets/xyz" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)


    @patch("typer.confirm")
    @patch("typer.secho")
    def test_utils_secret_utils_upsert_secret_overwrite(self, mock_echo, mock_cnf):
        mock_cnf.return_value = True

        secret_path = ".vault/db_secret"
        secret = "new_secret_789"
        hide_input = True
        secret_type = "database admin"
        r = secret_utils.upsert_secret(secret_path, secret, hide_input=hide_input,
                                            secret_type=secret_type)

        echo_tests = [ f"You already have a secret (ex*****23)" ]
        test_utils.assertEcho(self, echo_tests, mock_cnf)

        echo_tests = [ "\nSecret updated!" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        t = Path(".vault/db_secret").read_text()
        self.assertNotEqual(t, self.secret, "Secret file should've been updated")
        self.assertEqual(r, secret, "Should've returned new secret")


    @patch("typer.confirm")
    @patch("typer.secho")
    def test_utils_secret_utils_upsert_secret_no_overwrite(self, mock_echo, mock_cnf):
        mock_cnf.return_value = False

        secret_path = ".vault/db_secret"
        secret = "new_secret_789"
        hide_input = True
        secret_type = "database admin"
        r = secret_utils.upsert_secret(secret_path, secret, hide_input=hide_input,
                                            secret_type=secret_type)

        echo_tests = [ f"You already have a secret (ex*****23)" ]
        test_utils.assertEcho(self, echo_tests, mock_cnf)

        echo_tests = [ "\nSecret left alone!" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        t = Path(".vault/db_secret").read_text()
        self.assertEqual(t, self.secret, "Secret file shouldn't've been updated")


    @patch("typer.confirm")
    @patch("typer.prompt")
    @patch("typer.secho")
    def test_utils_secret_utils_upsert_secret_no_file(self,
                                                mock_echo, mock_pmt, mock_cnf):
        Path(".vault/db_secret").unlink()
        mock_pmt.return_value = new_secret = "entered_secret_555"
        mock_cnf.return_value = True

        secret_path = ".vault/db_secret"
        secret = None
        hide_input = True
        secret_type = "main database admin"
        r = secret_utils.upsert_secret(secret_path, secret, hide_input=hide_input,
                                            secret_type=secret_type)

        echo_tests = [ "Enter the main database admin secret",
                       "(use AUTO to autogenerate)" ]
        test_utils.assertEcho(self, echo_tests, mock_pmt)

        echo_tests = [ "You already have a secret", "Secret updated!" ]
        test_utils.assertNotEcho(self, echo_tests, mock_echo)

        echo_tests = [ "Secret added!" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        t = Path(".vault/db_secret")
        self.assertTrue(t.exists(), "Secret file should've been created")
        self.assertNotEqual(t.read_text(), self.secret, "File should be different")


    @patch("typer.confirm")
    @patch("typer.prompt")
    @patch("typer.secho")
    def test_utils_secret_utils_upsert_secret_skip_exists(self,
                                                mock_echo, mock_pmt, mock_cnf):
        mock_pmt.return_value = new_secret = "entered_secret_555"
        mock_cnf.return_value = True

        secret_path = ".vault/db_secret"
        secret = None
        hide_input = True
        skip_exists = True
        secret_type = "database admin"
        r = secret_utils.upsert_secret(secret_path, secret,
                                            hide_input=hide_input,
                                            skip_exists=skip_exists,
                                            secret_type=secret_type)

        echo_tests = [ "found", "ex*****23" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)
        self.assertEqual(r, "existing_secret_123", "Should've returned existing secret")

        t = Path(".vault/db_secret").read_text()
        self.assertEqual(t, self.secret, "Secret file shouldn't've been updated")


    def test_utils_secret_utils_get_vault(self):
        # assume default key of tests/testproject/.vault/vault-pass.txt
        r = secret_utils.get_vault()

        self.assertIsInstance(r, VaultLib, "Should've returnd vault library object")


    def test_utils_secret_utils_get_vault_missing(self):
        with self.assertRaises(exceptions.Exit) as context:
            key_path = ".vault/non-existent.txt"
            r = secret_utils.get_vault(key_path)



    def test_utils_secret_utils_encrypt(self):
        secret_path = "database/secrets/db_local_password_admin"
        Path(secret_path).unlink(missing_ok=True)
        secret = "vault_newly_encrypted"
        r = secret_utils.encrypt(secret, secret_path)

        self.assertTrue(r.exists(), "Should've created the password file")

        Path(secret_path).unlink(missing_ok=True)


    def test_utils_secret_utils_decrypt(self):
        # previously encrypted secret, using raw ansible
        secret_path = "database/secrets/db_local_password_user"
        r = secret_utils.decrypt(secret_path)

        t = "vault_previously_encrypted"
        self.assertEqual(r, t, "Should've decrypted and returned password")


    def test_utils_secret_utils_decrypt_bad_key(self):
        # previously encrypted secret, using raw ansible
        secret_path = "database/secrets/db_local_password_user"
        key_path = "database/secrets/db_local_password_user"

        with self.assertRaises(exceptions.Exit) as context:
            r = secret_utils.decrypt(secret_path, key_path=key_path)


    def test_utils_secret_utils_generate_secret(self):
        chars = 20
        r = secret_utils.generate_secret(chars)

        self.assertEqual(len(r), chars, "Should've generated pasword of right length")


    def test_utils_secret_utils_generate_secret_default_length(self):
        r = secret_utils.generate_secret()

        self.assertEqual(len(r), 30, "Should've generated pasword of default length")


    @patch.dict(os.environ, { "SECRET_LENGTH": "10" })
    def test_utils_secret_utils_generate_secret_env_length(self):
        r = secret_utils.generate_secret()

        self.assertEqual(len(r), 10, "Should've generated pasword of env length")