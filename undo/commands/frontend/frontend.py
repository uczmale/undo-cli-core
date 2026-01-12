import os, subprocess
import typer
from pathlib import Path
from undo.utils import dir_utils

CODE_TEXT_COLOUR = typer.colors.BRIGHT_BLACK

def command(operation, context_search="") -> None:
    command_dir = dir_utils.get_command_directory("frontend", "frontend")
    context = dir_utils.get_fuzzy_subdirectory(command_dir, context_search, "frontend")

    typer.secho(f"Frontend {context.name} selected..\n")

    # okay, so, we know what folder we're doing all this stuff in
    # let's go there
    typer.secho(f"Switching to directory to execute commands:")
    typer.secho(f"\tcd {context}", fg=CODE_TEXT_COLOUR)

    if operation == "run":
        run(context)


def run(context):
    typer.secho(f"\nRunning dev React instance:")
    typer.secho(f"\tnpm run dev", fg=CODE_TEXT_COLOUR)
    
    subprocess.run("npm run dev", shell=True, cwd=context)