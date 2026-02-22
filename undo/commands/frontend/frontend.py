import os, subprocess
import typer

# undo specific imports
from undo.utils import dir_utils
from undo.commands.frontend.frontend_arguments import config
from undo.commands.frontend import frontend_misc

app = typer.Typer(no_args_is_help=True)

CODE_TEXT_COLOUR = typer.colors.BRIGHT_BLACK


@app.command("run", help=config["run"]["help"])
def run_command(context_search: config["context_search"] = "") -> None:
    command_dir, context = command(context_search)
    frontend_misc.run(context)
    return


def command(context_search) -> None:
    command_dir = dir_utils.get_command_directory("frontend", "frontend")
    context = dir_utils.get_fuzzy_subdirectory(command_dir, context_search, "frontend")

    typer.secho(f"Frontend {context.name} selected..\n")

    # okay, so, we know what folder we're doing all this stuff in
    # let's go there
    typer.secho(f"Switching to directory to execute commands:")
    typer.secho(f"\tcd {context}", fg=CODE_TEXT_COLOUR)

    return command_dir, context



# callback to force single command app to still require command
@app.callback()
def callback():
    pass