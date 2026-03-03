import os, sys
from pathlib import Path

import typer

# undo specific imports
from undo.utils import const


def get_secret(secret_path, *, show_error=False):
    secret = False

    if secret_path.exists():
        secret = secret_path.read_text().strip()

    else:
        # secrets that start with underscores are pretty good
        secret_plain_path = Path(secret_path.parent / ("_" + secret_path.name))
        if secret_plain_path.exists():
            secret = secret_file.read_text.strip()

    if show_error and not secret:
        typer.secho("\nRuh-roh!", fg=const.ERRR_TEXT_COLOUR)
        typer.secho(f"No secret found at path: {secret_path}")
        raise typer.Exit(1)

    return secret


def upsert_secret(secret_path=None, secret=None, *,
                    hide_input=True, skip_exists=False, secret_type=None):
    
    # make sure the secret path exists, ahead of trying to create it
    secret_file = Path(secret_path)
    secret_file.parent.mkdir(parents=True, exist_ok=True)

    # you can skip prompting if the file already exists
    # and just return the existing secret
    if skip_exists and secret_file.exists():
        secret = secret_file.read_text().strip()
        secret_mask = secret[0:2] + "*****"  + secret[-2:]
        typer.secho(f"Retrieving existing secret [{secret_mask}]...")
        return secret

    # otherwise, if a secret wasn't already prompted, start by prompting
    if not secret:
        secret_type = " "+ secret_type if secret_type else ""
        secret = typer.prompt(f"Enter the{secret_type} secret",
                                    hide_input=hide_input)

    # then, if a secret does exist, double check if they wanna change it
    if secret_file.exists():
        existing_secret = secret_file.read_text().strip()

        secret_mask = existing_secret[0:2] + "*****"  + existing_secret[-2:]
        echo = f"You already have a secret ({secret_mask}), " \
                + "do you want to overwrite it?"

        typer.secho("\nCHECK", fg=const.WARN_TEXT_COLOUR)
        secret_check = typer.confirm(echo)

        # if they wanna change it, update the file
        if secret_check:
            secret_file.write_text(secret)
            typer.secho("\nSecret updated!", fg=const.SCSS_TEXT_COLOUR)
        
        # otherwise thank them for their time
        else:
            secret = existing_secret
            typer.secho("\nSecret left alone!", fg=const.INFO_TEXT_COLOUR)

    # if  there is no existing secret, save this one
    else:
        secret_file.write_text(secret)
        typer.secho("\nSecret added!", fg=const.SCSS_TEXT_COLOUR)

    # return the secret we decided was this secret
    return secret