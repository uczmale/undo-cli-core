import unittest, logging, os, sys
import json, re
from unittest.mock import patch
from unittest.mock import Mock

from testutils import test_setup
logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG")))

# mock the handler that will exist in the real function but doesn't here in testland
sys.modules['handler'] = Mock()

# test specific imports
from easiutils import exceptions as er
from undo.commands.function.templates.unwrapper import wrapper


logging.disable(logging.CRITICAL)
#logging.basicConfig(level=logging.DEBUG)

token = '''
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlBjWDk4R1g0MjBUMVg2c0JEa3poUW1xZ3dNVSJ9.eyJhdWQiOiI4NmQyZDFhMi0wNTFkLTRmZmItYmM1NC0wNzMxYTQ2M2ZmZTYiLCJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vMWZhZjg4ZmUtYTk5OC00YzViLTkzYzktMjEwYTExZDlhNWMyL3YyLjAiLCJpYXQiOjE3Njc2NDQyNjksIm5iZiI6MTc2NzY0NDI2OSwiZXhwIjoxNzY3NjQ4OTU5LCJhaW8iOiJBWlFBYS84YUFBQUFua0VTMGM3WE5DbW1KSGltZDAzMklHZnZzNXRkNU5RcEp6TE1TdHhtaG1nTXRNbHYwMzUwSzlOSE53S01uZGdDWWg0NGlxRmJUd1Q2Y3BaM3QwRE05V2gvYTZPS2VKYldBR3h1aGdZRVBEK3kxb0pSUDBKYjNuRzZGMFpudDV2Vlh0Y0k3dW5yMjlTc1FTT2QxWmxNTE1QRHFSR2VxT2wrOEIvZVY2SEZxcnFJNWRvRG0yUE5TU25zRUtQUGFiMDciLCJhenAiOiIyNTA3OWFmOS02NGMwLTRkZDQtODIwNi01YThkZmM2NTdhY2UiLCJhenBhY3IiOiIwIiwibmFtZSI6Ik5lbHNvbiwgQWxleGlzIiwib2lkIjoiMDFlZTIwNGUtMDFmNi00MzBmLTk5YmEtOTE1NWJjYjY1YTFjIiwicHJlZmVycmVkX3VzZXJuYW1lIjoidWN6bWFsZUB1Y2wuYWMudWsiLCJyaCI6IjEuQVFVQV9vaXZINWlwVzB5VHlTRUtFZG1sd3FMUjBvWWRCZnRQdkZRSE1hUmpfLWFfQVI4RkFBLiIsInNjcCI6IkZpbGVzLlJlYWQiLCJzaWQiOiIwMDZiZTkxOS1jNjc4LWY4MGQtOWFkMC1jYjI2NDNhNWExMjgiLCJzdWIiOiJ3bnpzNXE3eDh4LVgtQXljVzhEWXhfbndpQjdHNWJidG9DZU1GQWphRDZFIiwidGlkIjoiMWZhZjg4ZmUtYTk5OC00YzViLTkzYzktMjEwYTExZDlhNWMyIiwidXRpIjoiUDY2b251ejVia1M3VlhZMkE5bE1BQSIsInZlciI6IjIuMCIsInhtc19mdGQiOiJVTXp4MFhPdEViOVJUSjgtYlFhMDh2Uld0OHB0cjZydUJoS2ZYR04wQUJvQlpYVnliM0JsYm05eWRHZ3RaSE50Y3cifQ.gFo_0cJrvYZN42kvp6oBrWTGEfm3hkYi7sVI_C2mBrXfR4elXHLSspdIyt2LjdmHc54_gdwwRxs200II9f4gpAgLuPPdxoGYMN40SleyqD0Om2XG49-gyum5ovfsU4aUyRYqUxb6KH0q807OJanlgWqJkM3SzgkeZ6VImmM3Eh_QhnktOMGM0Chbue8EJCrK_jW55q0LX-Mag8GQN_xHkGAxekOskD_ntxgRiPDmO2hGgtMkFeqcM4a2DPiO6bi9Z8GjFV_ZWD-5RV1UbUcZDmRII7k9JRV7Dgo5wnITi4szIFECaiVPOapNwrs4kf-sQGomyYKLGuqvqusVnypUsQ
'''.strip()

class WrapperTestCase(unittest.TestCase):
    def setup(self):
        run_tests = '''
        source .venv/bin/activate
        cp ./easiwrapper/wrapper.py ./wrapper.py
        python3 -m unittest discover -v ./wrapper
        python3 -m unittest -v easiwrapper.test_wrapper.WrapperTestCase.test_wrapper_jwt_decode
        rm ./wrapper.py
        deactivate
        '''

    def test_wrapper_define_paths(self):
        args = [
            "/dir",
            "/dir/{identifier}",
            "/dir/{dir_identifier}/subdir/{subdir_identifier}"
        ]
        r = wrapper.EASIHandler.define_paths(args)

        t = [
            {
                "key": "/dir",
                "mask": re.compile("^/dir$"),
                "params": []
            },
            {
                "key": "/dir/{identifier}",
                "mask": re.compile("^/dir/([^/]+)$"),
                "params": ["identifier"]
            },
            {
                "key": "/dir/{dir_identifier}/subdir/{subdir_identifier}",
                "mask": re.compile("^/dir/([^/]+)/subdir/([^/]+)$"),
                "params": ["dir_identifier", "subdir_identifier"]
            }
        ]
        self.assertEqual(r, t, "Should've extracted the path mask regex and params")


    def test_wrapper_extract_path_params_single(self):
        args = ["/dir/{identifier}", "/dir/{dir_identifier}/subdir/{subdir_identifier}"]
        path_set = wrapper.EASIHandler.define_paths(args)
        raw_path = "/dir/directory_identifier"

        r = wrapper.EASIHandler.extract_path_params(path_set, raw_path)

        a = r[0]
        t = "/dir/{identifier}"
        self.assertEqual(a, t, "Should've identified correct path key")

        a = r[1]
        t = { "identifier": "directory_identifier" }
        self.assertEqual(a, t, "Should've identified correct pair of path params")


    def test_wrapper_extract_path_params_multiple(self):
        args = ["/dir/{identifier}", "/dir/{dir_identifier}/subdir/{subdir_identifier}"]
        path_set = wrapper.EASIHandler.define_paths(args)
        raw_path = "/dir/directory_identifier/subdir/subdirectory_identifier"

        r = wrapper.EASIHandler.extract_path_params(path_set, raw_path)

        a = r[0]
        t = "/dir/{dir_identifier}/subdir/{subdir_identifier}"
        self.assertEqual(a, t, "Should've identified correct path key")

        a = r[1]
        t = {
            "dir_identifier": "directory_identifier",
            "subdir_identifier": "subdirectory_identifier"
        }
        self.assertEqual(a, t, "Should've identified correct set of path params")


    def test_wrapper_extract_query_params(self):
        query_string = "$filter=search eq search_term&modifier=awkward%20modifier"
        r = wrapper.EASIHandler.extract_query_params(query_string)

        t = {
            "$filter": "search eq search_term",
            "modifier": "awkward modifier"
        }
        self.assertEqual(r, t, "Should've identified correct path key")


    def test_wrapper_extract_query_params_empty(self):
        query_string = ""
        r = wrapper.EASIHandler.extract_query_params(query_string)

        t = None
        self.assertEqual(r, t, "Should've returned None for an empty query string")


    def test_wrapper_extract_authorisation_basic(self):
        auth_header = "Basic dWN6bWFsZTpuZWxzb24="
        r = wrapper.EASIHandler.extract_authorisation(auth_header)

        t = { "lambda": { "full_name": "uczmale" } }
        self.assertEqual(r, t, "Should've extracted name from basic auth hash")


    def test_wrapper_extract_authorisation_jwt(self):
        auth_header = "Bearer " + token
        r = wrapper.EASIHandler.extract_authorisation(auth_header)

        a = "https://login.microsoftonline.com/1faf88fe-a998-4c5b-93c9-210a11d9a5c2/v2.0"
        self.assertEqual(r["jwt"]["claims"]["iss"], a, "Should have captured JWT info")
        self.assertIn("name", r["jwt"]["claims"], "Should have extract all claims")


    def test_wrapper_extract_authorisation_none(self):
        auth_header = None
        r = wrapper.EASIHandler.extract_authorisation(auth_header)

        self.assertEqual(r, None, "Should've returned None like wot it got given")
