import unittest, os, sys
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from click import exceptions

# project specific imports
from undo.utils import test_utils

# the module being tested
from undo.commands.database import database_misc

class DatabaseMiscTestCase(unittest.TestCase):
    def setUp(self):
        # start the session in the mock project folder
        self.reset_cwd = os.getcwd()
        os.chdir("tests/testproject")
        self.root_password_path = "database/release/secrets/local/db_local_password_root"
        self.password = Path(self.root_password_path).read_text()

    def tearDown(self):
        # reset to where we ran this test from, since we chdir a bunch
        Path(self.root_password_path).write_text(self.password)
        os.chdir(self.reset_cwd)


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_command_database_misc_mysql_statement(self, mock_echo, mock_run):
        statement = "SELECT * FROM dual"
        env = "local"
        database_name = "undo"
        r = database_misc.mysql_statement(statement, env, database_name=database_name)

        echo_tests = [ "Running database statement..",
                       f"\n\t      -u root -p$(undo decrypt",
                       f"-e \"{statement}\"",
                       f"-D {database_name}" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        args, kwargs = mock_run.call_args
        a = args[0]
        t = "mysql --host 127.0.0.1 --port 3306 -u root -pexisting_password_123"
        self.assertIn(t, a, "Should've tried to to the right database")

        t = f"-D {database_name} -e \"{statement}\""
        self.assertIn(t, a, "Should've run the command against the databata")


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_command_database_misc_docker_command(self, mock_echo, mock_run):
        command = "start"
        container_name = "undodb"
        r = database_misc.docker_command(command, container_name)

        args, kwargs = mock_run.call_args
        a = args[0]
        t = f"docker {command} {container_name}"
        self.assertEqual(a, t, "Should've started the container")


    @patch("typer.secho")
    def test_command_database_misc_docker_command_bad_command(self, mock_echo):
        command = "xyz"
        container_name = "undo"

        with self.assertRaises(exceptions.Exit) as context:
            r = database_misc.docker_command(command, container_name)

        echo_tests = [ f"The command {command} is not supported;" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)


    @patch("typer.confirm")
    @patch("typer.secho")
    def test_command_database_misc_upsert_password_overwrite(self, mock_echo, mock_cnf):
        mock_cnf.return_value = True

        password = "new_password_789"
        hide_input = True
        r = database_misc.upsert_password(password, hide_input=hide_input)

        echo_tests = [ f"You already have a secret (ex*****23)" ]
        test_utils.assertEcho(self, echo_tests, mock_cnf)

        echo_tests = [ "\nSecret updated!" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        t = Path(self.root_password_path).read_text()
        self.assertNotEqual(t, self.password, "Password file should've been updated")
        self.assertEqual(r, password, "Should've returned new password")


    @patch("typer.confirm")
    @patch("typer.secho")
    def test_command_database_misc_upsert_password_no_overwrite(self, mock_echo, mock_cnf):
        mock_cnf.return_value = False

        password = "new_password_789"
        hide_input = True
        r = database_misc.upsert_password(password, hide_input=hide_input)

        echo_tests = [ f"You already have a secret (ex*****23)" ]
        test_utils.assertEcho(self, echo_tests, mock_cnf)

        echo_tests = [ "\nSecret left alone!" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        t = Path(self.root_password_path).read_text()
        self.assertEqual(t, self.password, "Password file shouldn't've been updated")


    @patch("typer.confirm")
    @patch("typer.prompt")
    @patch("typer.secho")
    def test_command_database_misc_upsert_password_no_file(self,
                                                mock_echo, mock_pmt, mock_cnf):
        Path(self.root_password_path).unlink()
        mock_pmt.return_value = new_password = "entered_password_555"
        mock_cnf.return_value = True

        password = None
        hide_input = True
        r = database_misc.upsert_password(password, hide_input=hide_input)

        echo_tests = [ "Enter the database admin secret" ]
        test_utils.assertEcho(self, echo_tests, mock_pmt)

        echo_tests = [ "You already have a secret", "Secret updated!" ]
        test_utils.assertNotEcho(self, echo_tests, mock_echo)

        echo_tests = [ "Secret added!" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)
        self.assertEqual(r, new_password, "Should've returned new password")


    @patch("typer.confirm")
    @patch("typer.prompt")
    @patch("typer.secho")
    def test_command_database_misc_upsert_password_skip_exists(self,
                                                mock_echo, mock_pmt, mock_cnf):
        mock_pmt.return_value = new_password = "entered_password_555"
        mock_cnf.return_value = True

        password = None
        hide_input = True
        skip_exists = True
        r = database_misc.upsert_password(password, hide_input=hide_input,
                                                        skip_exists=skip_exists)

        echo_tests = [ "found", "ex*****23" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)
        t = "existing_password_123"
        self.assertEqual(r, t, "Should've returned existing password")

        t = Path(self.root_password_path).read_text()
        self.assertEqual(t, self.password, "Password file shouldn't've been updated")


    @patch("typer.confirm")
    @patch("typer.prompt")
    @patch("typer.secho")
    def test_command_database_misc_upsert_password_env_type_skip_exists(self,
                                                mock_echo, mock_pmt, mock_cnf):
        mock_pmt.return_value = new_password = "updated_dev_user_password_333"
        mock_cnf.return_value = True


        password = None
        env = "dev"
        user_type = "user"
        hide_input = True
        skip_exists = True
        r = database_misc.upsert_password(password, env=env, user_type=user_type,
                                    hide_input=hide_input, skip_exists=skip_exists)

        echo_tests = [ "found", "de*****32" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        t = "dev_current_user_password_432"
        self.assertEqual(r, t, "Should've returned existing password")
