import os, subprocess
import typer
import typer

# undo specific imports
from undo.utils import const


def docker_command(command, container_name):
    if command not in ["start", "stop", "restart", "rm"]:
        typer.secho(f"The only commands available are start, stop, restart and rm",
                fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho(f"Running docker command:")
    typer.secho(f"\tdocker {command} {container_name}", fg=const.CODE_TEXT_COLOUR)

    result = subprocess.run(f"docker {command} {container_name}", shell=True)
    return