import os, subprocess
import typer

# undo specific imports
from undo.utils import const, secret_utils


def decrypt_secret(secret_path, *, raw=False):
    # get the secret with all the attendent decryption
    secret = secret_utils.get_secret(secret_path, show_error=True)

    # if raw, just return the string, with no whitespace, to use in a $(subcommand)?
    if raw:
        typer.secho(secret, nl=False)

    # otherwise, a big flashy colourfull print
    else:
        typer.secho("\nSecret decrypted!", fg=const.SCSS_TEXT_COLOUR)
        typer.secho(f"\t{secret}")

    return secret


def generate_secret(secret_length, lowercase_only=True, include_symbols=False):
    secret = secret_utils.generate_secret(secret_length, lowercase_only, include_symbols)
    typer.secho("\nSecret generated!", fg=const.SCSS_TEXT_COLOUR)
    typer.secho("\t" + secret)

    return secret