import os
from pathlib import Path
import unittest
from unittest.mock import patch

# the module being tested
from undo.commands.function.helpers import function_wrapper_route_parser

class RouteParserTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_helper_function_wrapper_route_parser_simple(self):
        file_path = Path("tests/testdata/python-simple-code.py")
        visitor = function_wrapper_route_parser.RouteVisitor()
        visitor.parse_handler(file_path)

        r = visitor.route_list

        t = [ "GET /undo/{identifier}", "PUT /undo/{identifier}" ]
        self.assertEqual(r, t, "Should've extracted just the two valid routes")


    def test_helper_function_wrapper_route_parser_standard(self):
        file_path = Path("tests/testdata/python-handler-sample.py")
        visitor = function_wrapper_route_parser.RouteVisitor()
        visitor.parse_handler(file_path)

        r = visitor.route_list

        t = [ "GET /undo", "GET /undo/{identifier}", 
              "POST /undo", "PUT /undo/{identifier}" ]
        self.assertEqual(r, t, "Should've extracted just the two valid routes")


    def test_helper_function_wrapper_route_parser_no_handler(self):
        file_path = Path("non-existent-file")
        visitor = function_wrapper_route_parser.RouteVisitor()
        visitor.parse_handler(file_path)

        r = visitor.route_list

        t = [ ]
        self.assertEqual(r, t, "Should've returned no routes and given no exception?")
