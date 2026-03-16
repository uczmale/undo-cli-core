import os, subprocess
import typer

# undo specific imports
from undo.utils import const
from undo.utils import container_utils
from undo.commands.secret.secret_arguments import config
from undo.commands.secret import secret_misc

app = typer.Typer(no_args_is_help=True)


@app.command("generate", help=config["generate"]["help"])
def create_command(characters: config["generate"]["characters"] = 38) -> None:

    secret_misc.generate_secret(chars=characters, include_symbols=True)
    return



# callback to force single command app to still require command
@app.callback()
def callback():
    pass