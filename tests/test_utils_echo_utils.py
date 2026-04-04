import os
from pathlib import Path
import unittest
from unittest.mock import patch
from click import exceptions

# the module being tested
from undo.utils import test_utils
from undo.utils import echo_utils

class EchoUtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_utils_echo_utils_echo(self):
        with test_utils.PrintBuffer() as p:
            echo_utils.echo("hello")

        self.assertEqual(p.output, "\nhello\n", "Should've caught the hello")


    def test_utils_echo_utils_echo_title(self):
        with test_utils.PrintBuffer() as p:
            echo_title = "Title"
            echo_text = "This is the text"
            echo_utils.echo(title=echo_title, text=echo_text)

        t = "\nTitle\nThis is the text\n"
        self.assertEqual(p.output, t, "Should've caught the title and text")


    def test_utils_echo_utils_echo_title_colour(self):
        with test_utils.PrintBuffer() as p:
            echo_title = "Title"
            echo_text = "This is the text"
            echo_utils.echo(title=echo_title, text=echo_text, level="success")

        t = "\nTitle\nThis is the text\n"
        self.assertEqual(p.output, t, "Should've caught the title and text")


    def test_utils_echo_utils_echo_command(self):
        lines = "docker run"
        r = echo_utils.echo_command(lines)

        t = "\tdocker run"
        self.assertEqual(r, t, "Should've printed the basic command")


    def test_utils_echo_utils_echo_command_word(self):
        lines = "docker"
        r = echo_utils.echo_command(lines)

        t = "\tdocker"
        self.assertEqual(r, t, "Should've printed the basic command")


    def test_utils_echo_utils_echo_command_multiline(self):
        lines = "docker run \ -d undo \ undodb"
        r = echo_utils.echo_command(lines)

        t = "\tdocker run \\\n\t       -d undo \\\n\t       undodb"
        self.assertEqual(r, t, "Should've printed command over multiple lines, indented")


    def test_utils_echo_utils_echo_command_multiline_list(self):
        lines = [ "docker run", "-d undo", "undodb" ]
        r = echo_utils.echo_command(lines)

        t = "\tdocker run \\\n\t       -d undo \\\n\t       undodb"
        self.assertEqual(r, t, "Should've caught the title and text")
