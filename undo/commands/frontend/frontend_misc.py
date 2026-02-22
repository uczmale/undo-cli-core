import os, subprocess
import typer

# undo specific imports
from undo.utils import const


def run(context):
    typer.secho(f"\nRunning dev React instance:")
    typer.secho(f"\tnpm run dev", fg=const.CODE_TEXT_COLOUR)
    
    subprocess.run("npm run dev", shell=True, cwd=context)