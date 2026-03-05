import os, subprocess
import string, random
import typer

# undo specific imports
from undo.utils import const


def generate_secret(chars, lowercase_only=True, include_symbols=False):
    lower = list(string.ascii_lowercase)
    upper = list(string.ascii_uppercase) if not lowercase_only else []
    numbers = list("0123456789") if not lowercase_only  else []
    symbols = list("_-,.~") if include_symbols else []
    char_set = lower + upper + numbers + numbers + symbols + symbols
    
    first_char = random.choice(lower) # guarantee letter first
    random_list = ''.join([random.choice(char_set) for i in range(chars - 1)])

    password = first_char + random_list
    typer.secho("\nPassword generated!", fg=const.SCSS_TEXT_COLOUR)
    typer.secho("\t" + password)

    return password