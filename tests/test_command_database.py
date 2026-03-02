import unittest, os, sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from click import exceptions

# project specific imports
from undo.utils import test_utils

# the module being tested
from undo.commands.database import database, database_misc

runner = CliRunner()

class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        # start the session in a specific, mock project location
        self.reset_cwd = os.getcwd()
        os.chdir("tests/testproject")

    def tearDown(self):
        # reset to where we ran this test from, since we chdir a bunch
        os.chdir(self.reset_cwd)


    @patch("subprocess.run")
    @patch.dict(os.environ, { "UNDO_ROOT_CHECK_FILE": ".mock" })
    def test_command_database_command_create(self, mock_run):
        password_path = Path(".vault/db_password")
        password = password_path.read_text()
        password_path.unlink(missing_ok=True)

        r = runner.invoke(database.app,
                            ["create", "undo"],
                            input="invoke_password_input",
                            catch_exceptions=False)
        # print(r.output)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        echo_tests = [
            "Secret added", "Running the MySQL container..",
            "docker run -d", "--name undodb"
        ]
        for t in echo_tests:
            self.assertIn(t, r.output, "Should have spat out text based on input")

        args, kwargs = mock_run.call_args
        a = args[0]
        t = f"docker run -d"
        self.assertIn(t, a, "Should've tried to run a container")

        t = f"--name undodb"
        self.assertIn(t, a, "Should've given the container the correct name")
        
        # clean up
        password_path.write_text(password)


    @patch("subprocess.run")
    @patch.dict(os.environ, { "UNDO_ROOT_CHECK_FILE": ".mock" })
    def test_command_database_command_create_existing_password(self, mock_run):
        r = runner.invoke(database.app,
                            ["create", "undo"],
                            catch_exceptions=False)
        # print(r.output)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        echo_tests = [
            "Retrieving", "Running the MySQL container..",
            "docker run -d", "--name undodb"
        ]
        for t in echo_tests:
            self.assertIn(t, r.output, "Should have spat out text based on input")

        args, kwargs = mock_run.call_args
        a = args[0]
        t = f"docker run -d"
        self.assertIn(t, a, "Should've tried to run a container")

        t = f"--name undodb"
        self.assertIn(t, a, "Should've given the container the correct name")


    @patch("subprocess.run")
    @patch.dict(os.environ, { "UNDO_ROOT_CHECK_FILE": ".mock" })
    def test_command_database_command_init(self, mock_run):
        env = "local"
        host = "999.0.0.9"
        script = "database/db_initialise.sql"
        r = runner.invoke(database.app,
                            ["init", "-e", env, "-h", host, "-s", script ],
                            catch_exceptions=False)
        # print(r.output)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        echo_tests = [
            "Update the temporary script", f"s/<ENV>/{env}/g",
            "Run the updated script", f"--host {host}", "-pex*****23",
        ]
        for t in echo_tests:
            self.assertIn(t, r.output, "Should have spat out text based on input")

        args, kwargs = mock_run.call_args
        a = args[0]
        t = f"mysql --host {host}"
        self.assertIn(t, a, "Should've tried to run the MySQL command")

        t = f"< {script.replace("/", "/tmp/")}"
        self.assertIn(t, a, "Should've passed in the correct script")


    @patch("subprocess.run")
    def test_command_database_command_statement(self, mock_run):
        r = runner.invoke(database.app,
                            ["statement", "SHOW TABLES", "-d", "undo"],
                            catch_exceptions=False)
        # print(r.output)

        self.assertEqual(r.exit_code, 0, "Should have returned 0 exit code")

        echo_tests = [
            "Running database statement..",
            "\tmysql --host 127.0.0.1",
            "-D undo \\\n",
            "-e \"SHOW TABLES\""
        ]
        for t in echo_tests:
            self.assertIn(t, r.output, "Should have spat out text based on input")


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