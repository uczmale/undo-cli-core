import os, subprocess
import string, random
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


def generate_secret(chars, lowercase_only=True, include_symbols=False):
    lower = list(string.ascii_lowercase)
    upper = list(string.ascii_uppercase) if not lowercase_only else []
    numbers = list("0123456789") if not lowercase_only  else []
    symbols = list("_-,.~") if include_symbols else []
    char_set = lower + upper + numbers + numbers + symbols + symbols
    
    first_char = random.choice(lower) # guarantee letter first
    random_list = ''.join([random.choice(char_set) for i in range(chars - 1)])

    secret = first_char + random_list
    typer.secho("\nSecret generated!", fg=const.SCSS_TEXT_COLOUR)
    typer.secho("\t" + secret)

    return secret