import os, subprocess
import typer
from pathlib import Path

# undo specific imports
from undo.utils import const


def docker_command(command, container_name):
    if command not in ["start", "stop", "restart", "rm"]:
        typer.secho(f"The command {command} is not supported; " \
                     "the only commands available are start, stop, restart and rm",
                fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho(f"Running docker command..")
    typer.secho(f"\tdocker {command} {container_name}", fg=const.CODE_TEXT_COLOUR)

    result = subprocess.run(f"docker {command} {container_name}", shell=True)


def upsert_secret(password=None, hide_input=True):
    password_file = Path(".vault/db_password")
    password_file.parent.mkdir(parents=True, exist_ok=True)

    if not password:
        password = typer.prompt("Enter the main admin password",
                                    hide_input=hide_input)

    if password_file.exists():
        existing_password = password_file.read_text().strip()

        password_mask = existing_password[0:2] + "*****"  + existing_password[-2:]
        echo = f"You already have a password ({password_mask}), " \
                + "do you want to overwrite it?"

        typer.secho("\nCHECK", fg=const.WARN_TEXT_COLOUR)
        password_check = typer.confirm(echo)

        if password_check:
            password_file.write_text(password)
            typer.secho("\nPassword updated!", fg=const.SCSS_TEXT_COLOUR)
        else:
            password = existing_password
            typer.secho("\nPassword left alone!", fg=const.INFO_TEXT_COLOUR)

    else:
        password_file.write_text(password)
        typer.secho("\nPassword added!", fg=const.SCSS_TEXT_COLOUR)

    return password