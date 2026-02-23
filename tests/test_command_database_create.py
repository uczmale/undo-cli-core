import unittest, os, sys
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from click import exceptions

# the module being tested
from undo.commands.database import database_misc

runner = CliRunner()

class FrontendTestCase(unittest.TestCase):
    def setUp(self):
        pass


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_command_database_create_docker_command(self, mock_echo, mock_run):
        command = "start"
        container_name = "undo"
        r = database_misc.docker_command(command, container_name)

        args, kwargs = mock_run.call_args
        a = args[0]
        t = f"docker {command} {container_name}"
        self.assertEqual(a, t, "Should've started the container")