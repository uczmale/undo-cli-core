from io import StringIO
import sys


def assertEcho(unit, echo_tests, mockery):
    call_args = mockery.call_args_list
    full_echo = " ".join([call[0][0] for call in call_args])

    echo_tests = echo_tests if isinstance(echo_tests, list) else [echo_tests]
    for t in echo_tests:
        unit.assertIn(t, full_echo, "Should have spat out that text based as an echo")

def assertNotEcho(unit, echo_tests, mockery):
    call_args = mockery.call_args_list
    full_echo = " ".join([call[0][0] for call in call_args])

    echo_tests = echo_tests if isinstance(echo_tests, list) else [echo_tests]
    for t in echo_tests:
        unit.assertNotIn(t, full_echo, "Should NOT have spat out that text as an echo")


class PrintBuffer:
    # stdout logic stolen from
    # https://blog.finxter.com/7-easy-steps-to-redirect-your-standard-output-to-a-variable-python/

    def __init__(self):
        # during the with line and receives te with content
        # e.g. with PrintBuffer(...) the ... is passed to __init__
        # could be a file name later down the line, for example
        pass

    def __enter__(self):
        # happens before the first line of code inside with
        # capture the original stdout router thingy
        self.original_stdout = sys.stdout
        
        # initalise a new file stream thingy to send print() etc statements to
        self.output_buffer = StringIO()
        
        # assign the buffer to the current stdout router
        sys.stdout = self.output_buffer

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # happens at the end of the context block
        # route stdout back to its original destination
        sys.stdout = self.original_stdout

        # capture anything that was buffered by it in the meantime
        self.output = self.output_buffer.getvalue()
