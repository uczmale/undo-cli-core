import unittest, os, sys, shutil
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from click import exceptions

# project specific imports
from undo.utils import test_utils

# the module being tested
from undo.commands.database import database_release

runner = CliRunner()

class DatabaseReleaseTestCase(unittest.TestCase):
    def setUp(self):
        # start the session in the mock project folder
        self.reset_cwd = os.getcwd()
        os.chdir("tests/testproject")

    def tearDown(self):
        # reset to where we ran this test from, since we chdir a bunch
        os.chdir(self.reset_cwd)


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_command_database_release_release(self, mock_echo, mock_run):
        script_path = "database/db_initialise.sql"
        env = "dev"
        host = "127.0.0.1"

        r = database_release.release(script_path, env, host)

        t = Path(script_path.replace("/", "tmp"))
        self.assertFalse(t.exists(), "Should've removed temp script file")

        args, kwargs = mock_run.call_args
        t = [ f"mysql --host {host}",
               "database/tmp/db_initialise.sql" ]
        for i in t:
             self.assertIn(i, args[0], "Should've passed this text into the command")


    @patch("typer.secho")
    def test_command_database_release_get_script_path(self, mock_echo):
        script_path = "database/db_initialise.sql"
        r = database_release.get_script_path(script_path)

        t = Path("database/db_initialise.sql")
        self.assertEqual(r, t, "Should've returned Path version of script_path")


    @patch("typer.secho")
    def test_command_database_release_get_script_path_short(self, mock_echo):
        script_path = "db_initialise"
        r = database_release.get_script_path(script_path)

        t = Path("database/db_initialise.sql")
        self.assertEqual(r, t, "Should've returned completed version of script_path")


    @patch("typer.secho")
    def test_command_database_release_get_script_path_not_found(self, mock_echo):
        script_path = "xyz"

        with self.assertRaises(exceptions.Exit) as context:
            r = database_release.get_script_path(script_path)

        echo_tests = [ "Ruh-roh!", "path 'xyz' doesn't exist" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)


    def test_command_database_release_extract_placeholders(self):
        script_path = Path("database/db_initialise.sql")
        r = database_release.extract_placeholders(script_path)

        t = { "user", "admin" }
        self.assertEqual(r, t, "Should've returned map of user and admin")


    def test_command_database_release_password_mapping(self):
        placeholder_mapping = [("<ENV>", "dev")]
        password_type = "admin"
        r = database_release.password_mapping(placeholder_mapping, password_type)

        t = "init_admin_password_111"
        self.assertEqual(r, t, "Should've returned name/password tuple")

        a = placeholder_mapping
        t = [("<ENV>", "dev"), ("<ADMIN_PASSWORD>", "init_admin_password_111")]
        self.assertEqual(a, t, "Should've added new mapping to existing placeholders")


    @patch("typer.secho")
    def test_command_database_release_password_mapping_not_exist(self, mock_echo):
        placeholder_mapping = [("<ENV>", "dev")]
        password_type = "xyz"

        with self.assertRaises(exceptions.Exit) as context:
            r = database_release.password_mapping(placeholder_mapping, password_type)

        echo_tests = [ "Eckers", "from .vault/db_init_password_xyz" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)


    @patch("typer.secho")
    def test_command_database_release_update_script(self, mock_echo):
        script_path = Path("database/db_initialise.sql")
        placeholder_mapping = [("<ENV>", "dev"), ("<ADMIN_PASSWORD>", "password")]
        r = database_release.update_script(script_path, placeholder_mapping)

        self.assertTrue(r.exists(), "Should've created the converted script")
        self.assertNotIn("<ENV>", r.read_text(), "Should've replaced all <ENV> markers")
        self.assertNotIn("<ADMIN", r.read_text(), "Should've replaced all <ADMIN markers")

        echo_tests = [ "Copy database script",
                       "sed -i \"s/<ENV>/dev/g\" database/tmp/db_initialise.sql",
                       "s/<ADMIN_PASSWORD>/pa*****rd/g" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        # clean up temp directory
        shutil.rmtree(r.parent)


    @patch("typer.secho")
    def test_command_database_release_update_script_not_exist(self, mock_echo):
        script_path = Path("database/xyz.sql")
        placeholder_mapping = [("<ENV>", "dev"), ("<ADMIN_PASSWORD>", "password")]

        with self.assertRaises(exceptions.Exit) as context:
            r = database_release.update_script(script_path, placeholder_mapping)

        echo_tests = [ "Erreur", "- xyz.sql -" , "doesn't seem to exist" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_command_database_release_run_script(self, mock_echo, mock_run):
        script_path = Path("database/tmp/run_script.sql")
        host = "127.0.0.1"
        username = "root"
        password = "runtime_password_456"

        r = database_release.run_script(script_path, host, username, password)

        echo_tests = [ f"-u {username} -pru*****56 \\\n\t" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        args, kwargs = mock_run.call_args
        t = [ "mysql --host 127.0.0.1", f"-u {username}", "-pruntime_password_456",
               "database/tmp/run_script.sql" ]
        for i in t:
             self.assertIn(i, args[0], "Should've passed this text into the command")