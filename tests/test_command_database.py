import unittest, os, sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from click import exceptions

# project specific imports
from undo.utils import test_utils

# the module being tested
from undo.commands.database import database

runner = CliRunner()

class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        pass

    @patch("subprocess.run")
    def test_command_database_command_start(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "ctrldb\nundodb\nozqt"
        mock_run.return_value = mock_result

        r = runner.invoke(database.app,
                            ["start", "undodb"],
                            catch_exceptions=False)
        # print(r.output)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        echo_tests = [
            "Running docker command..",
            "\tdocker start undodb"
        ]
        for t in echo_tests:
            self.assertIn(t, r.output, "Should have spat out text based on input")


    @patch("subprocess.run")
    def test_command_database_command_stop(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "ctrldb\nundodb\nozqt"
        mock_run.return_value = mock_result

        r = runner.invoke(database.app,
                            ["stop", "undodb"],
                            catch_exceptions=False)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        echo_tests = [
            "Running docker command..",
            "\tdocker stop undodb"
        ]
        for t in echo_tests:
            self.assertIn(t, r.output, "Should have spat out text based on input")


    @patch("undo.utils.container_utils.get_container_name")
    @patch("typer.secho")
    def test_command_database_command(self, mock_echo, mock_nom):
        mock_nom.return_value = "ctrldb"
        context_search = "ctrl"
        r = database.command(context_search)

        self.assertEqual(r, "ctrldb", "Should return container name")