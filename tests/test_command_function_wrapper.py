import unittest, os
from pathlib import Path
from unittest.mock import patch
import tempfile
from click import exceptions

# project specific imports
from undo.utils import test_utils

# the module being tested
from undo.commands.function import function_wrapper


class FunctionWrapperTestCase(unittest.TestCase):
    def setUp(self):
        # start the session in the mock project folder
        self.reset_cwd = os.getcwd()
        os.chdir("tests/testproject")
        
    def tearDown(self):
        # reset to where we ran this test from, since we chdir a bunch
        os.chdir(self.reset_cwd)

    @patch("subprocess.run")
    @patch("typer.secho")
    def test_command_function_wrapper_wrapper(self, mock_echo, mock_run):
        context = Path("functions/undo_api_publisher")
        r = function_wrapper.wrapper(context)

        echo_tests = [ "port 8000", "Copy wrapper code", "export LOG_LEVEL",
                        "handler/handler.py", "/undo/{identifier}",
                        "wrapper.py 8000", "Clean up" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_command_function_wrapper_wrapper_args(self, mock_echo, mock_run):
        context = Path("functions/undo_api_publisher")
        routes = "/xndn/{identifier}"
        port = 8080
        no_routes=True
        r = function_wrapper.wrapper(context, routes=routes,
                                        port=port, no_routes=no_routes)

        echo_tests = [ "port 8080", "Copy wrapper code", "export LOG_LEVEL",
                        "wrapper.py 8080", "/xndn/{identifier}", "Clean up" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)
        test_utils.assertNotEcho(self, ["/undo/{identifier}"], mock_echo)


    @patch("typer.secho")
    def test_command_function_wrapper_intro_text(self, mock_echo):
        routes = "/undo /undo/{identity}"
        port = "8080"
        r = function_wrapper.intro_text(routes, port)

        t = "/undo, /undo/{identity}"
        args, kwargs = mock_echo.call_args
        self.assertIn(port, args[0], "Should've printed correct port")
        self.assertIn(t, args[0], "Should've printed correct routes")


    @patch("typer.secho")
    def test_command_function_wrapper_copy_wrapper(self, mockery):
        context = Path("functions/undo_api_publisher")
        r = function_wrapper.copy_wrapper(context)

        t = Path(context / "wrapper.py").exists()
        self.assertTrue(t, "Wrapper should've been copied to function directory")
        return

        args, kwargs = mockery.call_args_list[1]
        self.assertIn("templates/unwrapper", args[0], "Should've given wrapper location")
        self.assertIn("undo_api_publisher", args[0], "Should've given target location")

        Path(context / "wrapper.py").unlink()


    @patch("typer.secho")
    @patch.dict(os.environ, { "PATH": "current_env" }, clear=True)
    def test_command_function_wrapper_extract_env_vars(self, mockery):
        context = Path("functions/undo_api_publisher")
        r = function_wrapper.extract_env_vars(context)

        t = {
            "PATH": "current_env",
            "USERNAME": "undo_user",
            "LOG_LEVEL": "DEBUG"
        }
        self.assertEqual(r, t, "Should've captured vars, inc. overwrite and ignore")

        # there are actually three cuz the first is some generic user feedback
        args, kwargs = mockery.call_args_list[1]
        self.assertIn("undo_user", args[0], "Should've printed the latest USERNAME")
        self.assertIn("DEBUG", args[0], "Should've printed the non-commented LOG_LEVEL")

        self.assertNotIn("old_user", args[0], "Shouldn't've printed the first USERNAME")
        self.assertNotIn("TRACE", args[0], "Shouldn't've printed the commented LOG_LEVEL")


    @patch("typer.secho")
    @patch.dict(os.environ, { "PATH": "current_env" }, clear=True)
    def test_command_function_wrapper_extract_env_vars_empty(self, mockery):
        context = Path("functions/undo_api_publisher")
        r = function_wrapper.extract_env_vars(context, "environment-dev.txt")

        t = { "PATH": "current_env" }
        self.assertEqual(r, t, "Should've captured empty env list")


    @patch("typer.secho")
    def test_command_function_wrapper_extract_env_secrets(self, mock_echo):
        context = Path("functions/undo_event_publisher")
        r = function_wrapper.extract_env_secrets(context)

        t = {
            "unencrypted_secret": "unencrypted_secret",
            "encrypted_secret": "encrypted_secret"
        }
        self.assertEqual(r, t, "Should've captured secrets, inc unencrypred, encrypted")

        echo_tests = [ "secret env", "export unencrypted_secret=un*****et" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

    @patch("typer.secho")
    def test_command_function_wrapper_extract_routes(self, mock_echo):
        context = Path("functions/undo_api_publisher")
        routes = "/undo /undo/{identifier}/xndo"
        no_routes = False
        r = function_wrapper.extract_routes(context, routes, no_routes)

        t = [ "/undo", "/undo/{identifier}/xndo", "/undo/{identifier}" ]
        self.assertEqual(r, t, "Should've combined paths to unique list")

        echo_tests = [ "handler/handler.py", "/undo, /undo/{identifier}", "merged" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)


    @patch("typer.secho")
    def test_command_function_wrapper_extract_routes_no_routes(self, mock_echo):
        context = Path("functions/undo_api_publisher")
        routes = "/undo /undo/{identifier}/xndo"
        no_routes = True
        r = function_wrapper.extract_routes(context, routes, no_routes)

        t = [ "/undo", "/undo/{identifier}/xndo" ]
        self.assertEqual(r, t, "Should've combined paths to unique list")

        echo_tests = [ "Skipping", "/undo, /undo/{identifier}" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        echo_tests = [ "handler/handler.py", "merged" ]
        test_utils.assertNotEcho(self, echo_tests, mock_echo)


    @patch("typer.secho")
    def test_command_function_wrapper_extract_routes_no_handler(self, mock_echo):
        context = Path("functions/undo_event_publisher")
        routes = "/undo /undo/{identifier}/xndo"
        no_routes = False
        r = function_wrapper.extract_routes(context, routes, no_routes)

        t = [ "/undo", "/undo/{identifier}/xndo" ]
        self.assertEqual(r, t, "Should've combined paths to unique list")

        echo_tests = [
            "handler/handler.py", "No routes",
            "Just using", "/undo, /undo/{identifier}"
        ]
        test_utils.assertEcho(self, echo_tests, mock_echo)

        echo_tests = [ "Skipping.." ]
        test_utils.assertNotEcho(self, echo_tests, mock_echo)


    @patch("typer.secho")
    def test_command_function_wrapper_extract_handler_routes(self, mock_echo):
        context = Path("functions/undo_api_publisher")
        r = function_wrapper.extract_handler_routes(context)

        t = [ "/undo", "/undo/{identifier}" ]
        self.assertEqual(r, t, "Should've extracted just the two unique path masks")

        echo_tests = [ "handler/handler.py", "/undo, /undo/{identifier}" ]
        test_utils.assertEcho(self, echo_tests, mock_echo)


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_command_function_wrapper_run_process(self, mock_echo, mock_run):
        context = Path("functions/undo_api_publisher")
        routes = [ "/note", "/note/{identifier}" ]
        port = 8080
        env_vars = { "LOG_LEVEL": "DEBUG" }
        r = function_wrapper.run_process(context, routes, port, env_vars)

        args, kwargs = mock_echo.call_args_list[3]
        self.assertIn(" ".join(routes), args[0], "Should've printed routes")
        self.assertIn(str(port), args[0], "Should've printed port")

        args, kwargs = mock_run.call_args
        t = [ ".venv/bin/python", "wrapper.py", "8080", "/note", "/note/{identifier}" ]
        self.assertEqual(args[0], t, "Should've created the list of cmd args")
        self.assertEqual(kwargs["env"], env_vars, "Should've passed in env vars")
        self.assertEqual(kwargs["cwd"], context, "Should've passed in context as cwd")


    @patch("subprocess.run")
    @patch("typer.secho")
    def test_command_function_wrapper_run_process_no_routes(self, mock_echo, mock_run):
        context = Path("functions/undo_api_publisher")
        routes = None
        port = 8000
        env_vars = { "LOG_LEVEL": "DEBUG" }
        r = function_wrapper.run_process(context, routes, port, env_vars)

        args, kwargs = mock_echo.call_args_list[3]
        self.assertIn(str(port), args[0], "Should've printed port")

        args, kwargs = mock_run.call_args
        t = [ ".venv/bin/python", "wrapper.py", "8000" ]
        self.assertEqual(args[0], t, "Should've created the list of cmd args")
        self.assertEqual(kwargs["env"], env_vars, "Should've passed in env vars")
        self.assertEqual(kwargs["cwd"], context, "Should've passed in context as cwd")


    @patch("pathlib.Path.unlink")
    @patch("typer.secho")
    def test_command_function_wrapper_delete_wrapper_mocK(self, mock_echo, mock_unlink):
        context = Path("functions/undo_api_publisher")
        r = function_wrapper.delete_wrapper(context)

        args, kwargs = mock_echo.call_args
        t = "undo-cli/tests/testproject/functions/undo_api_publisher/wrapper.py"
        self.assertIn(t, args[0], "Should've printed deletion path")

        a = mock_unlink.assert_called_once
        self.assertTrue(a, "Should've attempted to delete the file")


    @patch("typer.secho")
    def test_command_function_wrapper_delete_wrapper_delete(self, mock_echo):
        with tempfile.TemporaryDirectory() as tmpdir:
                context = Path(tmpdir)
                wrapper_file = context / "wrapper.py"
                wrapper_file.write_text("test_wrapper_code")

                a = wrapper_file.exists()
                self.assertTrue(a, "Should've created the file")

                r = function_wrapper.delete_wrapper(context)

                a = wrapper_file.exists()
                self.assertFalse(a, "Should've attempted to delete the file")