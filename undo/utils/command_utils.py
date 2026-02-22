import os, sys, re
from pathlib import Path

import typer


# cli definition
def command(type, headline, context_search):
    command_dir = dir_utils.get_command_directory("functions", "function")
    context = dir_utils.get_fuzzy_subdirectory(command_dir, context_search, "function")

    function_name = context.name.replace("_", "-")
    typer.secho(f"Function {function_name} selected..\n")

    # okay, so, we know what folder we're doing all this stuff in
    # let's go there (while remembering how to get back)

    typer.secho(f"Switching to directory to execute commands:")
    typer.secho(f"\tcd {context}", fg=CODE_TEXT_COLOUR)

    return command_dir, context, function_name