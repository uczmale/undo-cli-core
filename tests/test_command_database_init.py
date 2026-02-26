import unittest, os, sys, shutil
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from click import exceptions

# project specific imports
from undo.utils import test_utils

# the module being tested
from undo.commands.database import database_init

runner = CliRunner()

class DatabaseInitTestCase(unittest.TestCase):
    def setUp(self):
        # start the session in the mock project folder
        self.reset_cwd = os.getcwd()
        os.chdir("tests/testproject")

    def tearDown(self):
        # reset to where we ran this test from, since we chdir a bunch
        os.chdir(self.reset_cwd)


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_command_database_init_init(self, mock_echo, mock_run):
        script_path = Path("database/db_initialise.sql")
        env = "dev"

        r = database_init.init(script_path, env)

        t = Path(script_path.parent / "tmp" / script_path.name)
        self.assertFalse(t.exists(), "Should've removed temp script file")

        args, kwargs = mock_run.call_args
        t = [ "mysql --host 127.0.0.1", "-pexisting_password_123",
               "database/tmp/db_initialise.sql" ]
        for i in t:
             self.assertIn(i, args[0], "Should've passed this text into the command")


    @patch("typer.secho")
    def test_command_database_init_update_script(self, mock_echo):
        script_path = Path("database/db_initialise.sql")
        placeholder_mapping = [("<ENV>", "dev"), ("<ADMIN_PASSWORD>", "password")]
        r = database_init.update_script(script_path, placeholder_mapping)

        self.assertTrue(r.exists(), "Should've created the converted script")
        self.assertNotIn("<ENV>", r.read_text(), "Should've replaced all <ENV> markers")
        self.assertNotIn("<ADMIN", r.read_text(), "Should've replaced all <ADMIN markers")

        echo_tests = [ "Erreur", "- xyz.sql -" , "doesn't seem to exist",
                       "sed -i \"s/<ENV>/dev/g\" database/tmp/db_initialise.sql" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        # clean up temp directory
        shutil.rmtree(r.parent)


    @patch("typer.secho")
    def test_command_database_init_update_script_not_exist(self, mock_echo):
        script_path = Path("database/xyz.sql")
        env = "dev"

        with self.assertRaises(exceptions.Exit) as context:
            r = database_init.update_script(script_path, env)

        echo_tests = [ "Erreur", "- xyz.sql -" , "doesn't seem to exist" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)