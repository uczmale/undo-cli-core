import os, subprocess
import typer
from pathlib import Path

# undo specific imports
from undo.utils import const
from undo.utils import secret_utils


def docker_command(command, container_name):
    if command not in ["start", "stop", "restart", "rm"]:
        typer.secho(f"The command {command} is not supported; " \
                     "the only commands available are start, stop, restart and rm",
                fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho(f"Running docker command..")
    typer.secho(f"\tdocker {command} {container_name}\n", fg=const.CODE_TEXT_COLOUR)

    result = subprocess.run(f"docker {command} {container_name}", shell=True)
    return result


def upsert_password(password=None, hide_input=True, skip_exists=False):
    password_file = Path(".vault/db_password")
    password = secret_utils.upsert_secret(password_file, password,
                                                hide_input=hide_input,
                                                skip_exists=skip_exists,
                                                secret_type="database admin")

    return password