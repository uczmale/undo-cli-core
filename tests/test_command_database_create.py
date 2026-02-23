import unittest, os, sys, shutil
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from click import exceptions

# the module being tested
from undo.commands.database import database_create

runner = CliRunner()

class FrontendTestCase(unittest.TestCase):
    def setUp(self):
        # start the session in the mock project folder
        self.reset_cwd = os.getcwd()
        os.chdir("tests/testproject")

    def tearDown(self):
        # reset to where we ran this test from, since we chdir a bunch
        os.chdir(self.reset_cwd)


    @patch("undo.commands.database.database_misc.upsert_secret")
    @patch("subprocess.run")
    @patch("typer.secho")
    def test_command_database_create_docker_command(self, mock_echo, mock_run, mock_sct):
        mock_sct.return_value = "db_password_mock"
        database_name = "undo"
        r = database_create.create(database_name, container_name)

        # args, kwargs = mock_run.call_args
        # a = args[0]
        # t = f"docker {command} {container_name}"
        # self.assertEqual(a, t, "Should've started the container")


    @patch("typer.secho")
    def test_command_database_create_initialise_database_directory(self, mock_echo):
        # rm -f local-config to see if gets created
        local_config = Path("database/local-config")
        local_config.exists() and shutil.rmtree(local_config)

        r = database_create.initialise_database_directory()

        my_conf = Path("database/local-config/my.conf")
        self.assertTrue(my_conf.exists(), "Should've created my.conf file")