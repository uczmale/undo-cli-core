import unittest

def assertEcho(unit, echo_tests, mockery):
        call_args = mockery.call_args_list
        full_echo = " ".join([call[0][0] for call in call_args])

        echo_tests = echo_tests if isinstance(echo_tests, list) else [echo_tests]
        for t in echo_tests:
            unit.assertIn(t, full_echo, "Should have spat out text based on input")