import unittest, os, sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from click import exceptions

# project specific imports
from undo.utils import test_utils

# the module being tested
from undo.utils import container_utils

runner = CliRunner()

class ContainerUtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    @patch("subprocess.run")
    @patch("typer.secho")
    def test_utils_container_utils_get_container_name(self, mock_echo, mock_sub):
        mock_result = MagicMock()
        mock_result.stdout = "ctrldb\nundodb\nozqt"
        mock_sub.return_value = mock_result

        name_search = "ctrldb"
        r = container_utils.get_container_name(name_search)

        self.assertEqual(r, "ctrldb", "Should return the single container")


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_utils_container_utils_get_container_name_subset(self, mock_echo, mock_sub):
        mock_result = MagicMock()
        mock_result.stdout = "ctrldb\nundodb\nozqt"
        mock_sub.return_value = mock_result

        name_search = "ctrl"
        r = container_utils.get_container_name(name_search)

        self.assertEqual(r, "ctrldb", "Should return the single container")


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_utils_container_utils_get_container_name_sub_list(self, mock_echo, mock_sub):
        mock_result = MagicMock()
        mock_result.stdout = "ctrldb\nundodb\nozqt"
        mock_sub.return_value = mock_result

        name_search = "db"
        with self.assertRaises(exceptions.Exit) as context:
            r = container_utils.get_container_name(name_search)

        echo_tests = [ "Multiple containers match 'db'",
                       "\t- ctrldb" ,
                       "\t- undodb" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_utils_container_utils_get_container_name_no_filter(self, mock_echo, mock_sub):
        mock_result = MagicMock()
        mock_result.stdout = "ctrldb\nundodb\nozqt"
        mock_sub.return_value = mock_result

        name_search = ""
        with self.assertRaises(exceptions.Exit) as context:
            r = container_utils.get_container_name(name_search)

        echo_tests = [ "There are multiple containers, select one",
                       "\t- ctrldb",
                       "\t- undodb",
                       "\t- ozqt" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_utils_container_utils_get_container_name_no_match(self, mock_echo, mock_sub):
        mock_result = MagicMock()
        mock_result.stdout = "ctrldb\nundodb\nozqt"
        mock_sub.return_value = mock_result

        name_search = "xyz"

        with self.assertRaises(exceptions.Exit) as context:
            r = container_utils.get_container_name(name_search)