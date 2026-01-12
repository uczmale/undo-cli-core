import os, subprocess, shutil
import typer
from pathlib import Path

from undo.utils import dir_utils
from undo.commands.function.function_arguments import *
from undo.commands.function import function_misc, function_wrapper

CODE_TEXT_COLOUR = typer.colors.BRIGHT_BLACK
INFO_TEXT_COLOUR = typer.colors.BRIGHT_YELLOW

# cli definition
def command(operation, context_search=None, opts={}) -> None:
    command_dir = dir_utils.get_command_directory("functions", "function")
    context = dir_utils.get_fuzzy_subdirectory(command_dir, context_search, "function")

    function_name = context.name.replace("_", "-")
    typer.secho(f"Function {function_name} selected..\n")

    # okay, so, we know what folder we're doing all this stuff in
    # let's go there (while remembering how to get back)
    typer.secho(f"Switching to directory to execute commands:")
    typer.secho(f"\tcd {context}", fg=CODE_TEXT_COLOUR)

    if operation == "wrapper":
        function_wrapper.wrapper(context,
                                    routes=opts.get("routes"),
                                    port=opts.get("port"),
                                    no_routes=opts.get("no_routes"))

    if operation == "properties":
        function_misc.properties(context)
