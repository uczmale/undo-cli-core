import os, subprocess
import typer

# undo specific imports
from undo.utils import const
from undo.utils import container_utils
from undo.commands.secret.secret_arguments import config
from undo.commands.secret import secret_misc, secret_encrypt

app = typer.Typer(no_args_is_help=True)


@app.command("encrypt", help=config["encrypt"]["help"])
def create_command(path: config["encrypt"]["path"],
                    secret: config["encrypt"]["secret"] = None,
                    autogenerate: config["encrypt"]["autogenerate"] = False,
                    overwrite: config["encrypt"]["overwrite"] = False) -> None:

    secret = secret if secret else autogenerate

    secret_encrypt.encrypt_secret(secret=secret, secret_path=path, overwrite=overwrite)
    return


@app.command("decrypt", help=config["decrypt"]["help"])
def create_command(path: config["decrypt"]["path"],
                    raw: config["decrypt"]["raw"] = False) -> None:

    secret_misc.decrypt_secret(secret_path=path, raw=raw)
    return


@app.command("generate", help=config["generate"]["help"])
def create_command(characters: config["generate"]["characters"] = 38) -> None:

    secret_misc.generate_secret(chars=characters, include_symbols=True)
    return


# callback to force single command app to still require command
@app.callback()
def callback():
    pass