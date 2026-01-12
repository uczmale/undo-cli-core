import os
from pathlib import Path
import unittest
from unittest.mock import patch
from click import exceptions

# the module being tested
from undo.utils import dir_utils

class DirectoryUtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_utils_dir_utils_get_execution_directory(self):
        cwd = os.path.dirname(dir_utils.__file__)
        r = dir_utils.get_execution_directory(cwd)

        self.assertEqual(r, Path(os.getcwd()), "Should've got to this directory")


    @patch.dict(os.environ, { "UNDO_ROOT_CHECK_FILE": ".mock" })
    def test_utils_dir_utils_get_execution_directory_mock(self):
        cwd = os.path.dirname(dir_utils.__file__) + "/testproject"
        r = dir_utils.get_execution_directory(cwd)

        self.assertEqual(r, Path(cwd), "Should've got to this directory")


    def test_utils_dir_utils_get_execution_directory_no_mock(self):
        cwd = os.path.dirname(dir_utils.__file__) + "/testproject"
        r = dir_utils.get_execution_directory(cwd)

        self.assertEqual(r, Path(os.getcwd()), "Should've got to this directory")


    @patch("undo.utils.dir_utils.get_execution_directory")
    def test_utils_dir_utils_get_command_directory(self, mock_dir):
        mock_dir.return_value = Path("tests/testproject")
        dir_name = "frontend"
        dir_type = "dir_type_name"

        r = dir_utils.get_command_directory(dir_name, dir_type)

        a = Path("tests/testproject/frontend")
        self.assertEqual(r, a, "Should've returned the frontend dir")


    @patch("typer.secho")
    @patch("undo.utils.dir_utils.get_execution_directory")
    def test_utils_dir_utils_get_command_directory_not_found(self, mock_dir, mock_echo):
        mock_dir.return_value = Path("tests/")
        dir_name = "frontend"
        dir_type = "dir_type_name"

        with self.assertRaises(exceptions.Exit) as context:
            r = dir_utils.get_command_directory(dir_name, dir_type)

        # get the output message
        args, kwargs = mock_echo.call_args
        a = args[0]
        self.assertIn(f"no {dir_type}s", a, "Should've printed no dir found")


    def test_utils_dir_utils_get_fuzzy_subdirectory_full_subdir(self):
        main_directory = Path("undo")
        subdir_mask = "utils"
        search_type = "frontend"
        r = dir_utils.get_fuzzy_subdirectory(
                                    main_directory, subdir_mask, search_type)

        self.assertEqual(r, main_directory / "utils", "Should returned the directory")


    def test_utils_dir_utils_get_fuzzy_subdirectory_specific_partial(self):
        main_directory = Path("undo")
        subdir_mask = "command"
        search_type = "frontend"

        r = dir_utils.get_fuzzy_subdirectory(
                                    main_directory, subdir_mask, search_type)

        self.assertEqual(r, Path("undo/commands"), "Should have returned just commands")


    @patch("typer.secho")
    def test_utils_dir_utils_get_fuzzy_subdirectory_multiple_results(self, mockery):
        main_directory = Path("undo/commands")
        subdir_mask = "c"
        search_type = "search_type"

        with self.assertRaises(exceptions.Exit) as context:
            r = dir_utils.get_fuzzy_subdirectory(
                                        main_directory, subdir_mask, search_type)

        # get the output message
        args, kwargs = mockery.call_args
        a = args[0]
        self.assertIn(search_type, a, "Should've printed search type in message")
        self.assertIn(f"match {subdir_mask},", a, "Should've included search term")
        self.assertIn("core", a, "Should've printed message including core dir")
        self.assertIn("docs", a, "Should've printed message including docs dir")


    @patch("typer.secho")
    def test_utils_dir_utils_get_fuzzy_subdirectory_no_search(self, mockery):
        main_directory = Path("undo/commands")
        subdir_mask = None
        search_type = "backend"

        with self.assertRaises(exceptions.Exit) as context:
            r = dir_utils.get_fuzzy_subdirectory(
                                        main_directory, subdir_mask, search_type)

        # get the output message
        args, kwargs = mockery.call_args
        a = args[0]
        self.assertIn("frontend", a, "Should've printed message including frontend dir")
        self.assertIn("core", a, "Should've printed message including core dir")


    @patch("typer.secho")
    def test_utils_dir_utils_get_fuzzy_subdirectory_bad_search(self, mockery):
        main_directory = Path("undo")
        subdir_mask = "xyz"
        search_type = "frontend"

        with self.assertRaises(exceptions.Exit) as context:
            r = dir_utils.get_fuzzy_subdirectory(
                                        main_directory, subdir_mask, search_type)

        # get the output message
        args, kwargs = mockery.call_args
        a = args[0]
        self.assertIn(f"No {search_type}", a, "Should've printed failure message")
        self.assertIn(subdir_mask, a, "Should've confirmed search mask")


    @patch("typer.secho")
    def test_utils_dir_utils_get_fuzzy_subdirectory_no_search_no_raise(self, mockery):
        main_directory = Path("undo/commands")
        subdir_mask = None
        search_type = "backend"
        raise_error = False

        r = dir_utils.get_fuzzy_subdirectory(
                                main_directory, subdir_mask, search_type, raise_error)

        self.assertEqual(mockery.call_count, 0, "Shouldn't've called echo")
        self.assertIsInstance(r, list, "Should've returned list of directories")
        self.assertIn("function", r, "Should've returned correct list of dictionaries")
        self.assertIn("frontend", r, "Should've returned correct list of dictionaries")


    @patch("typer.secho")
    def test_utils_dir_utils_get_fuzzy_subdirectory_bad_search_no_raise(self, mockery):
        main_directory = Path("undo")
        subdir_mask = "xyz"
        search_type = "frontend"
        raise_error = False

        r = dir_utils.get_fuzzy_subdirectory(
                                main_directory, subdir_mask, search_type, raise_error)

        self.assertEqual(mockery.call_count, 0, "Shouldn't've called echo")
        self.assertEqual(r, False, "Should've returned false")
