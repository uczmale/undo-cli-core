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
    def test_command_database_misc_start(self, mock_echo, mock_run):
        container_name = "undodb"
        r = database_misc.start(container_name)

        # there are actually three cuz the first is some generic user feedback
        args, kwargs = mock_run.call_args
        a = args[0]
        t = f"docker start {container_name}"
        self.assertEqual(a, t, "Should've started the container")