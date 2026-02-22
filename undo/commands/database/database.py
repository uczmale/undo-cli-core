import os, subprocess
import typer

# undo specific imports
from undo.utils import const
from undo.utils import dir_utils
from undo.commands.database.database_arguments import config

app = typer.Typer(no_args_is_help=True)



@app.command("start", help=config["run"]["help"])
def run_command(context_search: config["context_search"] = "") -> None:
    print("hi")
    command_dir, context = command(context_search)
    run(context)
    return


def command(context_search) -> None:
    command_dir = dir_utils.get_command_directory("frontend", "frontend")
    context = dir_utils.get_fuzzy_subdirectory(command_dir, context_search, "frontend")

    typer.secho(f"Frontend {context.name} selected..\n")

    # okay, so, we know what folder we're doing all this stuff in
    # let's go there
    typer.secho(f"Switching to directory to execute commands:")
    typer.secho(f"\tcd {context}", fg=const.CODE_TEXT_COLOUR)

    return command_dir, context


def run(context):
    typer.secho(f"\nRunning dev React instance:")
    typer.secho(f"\tnpm run dev", fg=const.CODE_TEXT_COLOUR)
    
    subprocess.run("npm run dev", shell=True, cwd=context)


# callback to force single command app to still require command
@app.callback()
def callback():
    pass