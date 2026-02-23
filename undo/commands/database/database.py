import os, subprocess
import typer

# undo specific imports
from undo.utils import const
from undo.utils import container_utils
from undo.commands.database.database_arguments import config
from undo.commands.database import database_misc

app = typer.Typer(no_args_is_help=True)


@app.command("create", help=config["create"]["help"])
def create_command(database_name: config["create"]["database_name"],
                    password: config["create"]["password"] = None,
                    show_password: config["create"]["show_password"] = False) -> None:

    database_misc.create_container(database_name, password=password,
                                        hide_input=(not show_password))
    return


@app.command("secret", help=config["secret"]["help"])
def secret_command(password: config["create"]["password"] = None,
                    show_password: config["create"]["show_password"] = False) -> None:

    database_misc.upsert_secret(password=password, hide_input=(not show_password))
    return


@app.command("start", help=config["start"]["help"])
def start_command(container_search: config["start"]["container_search"] = "") -> None:
    container_name = command(container_search)
    database_misc.docker_command("start", container_name)

    return


@app.command("stop", help=config["stop"]["help"])
def stop_command(container_search: config["stop"]["container_search"] = "") -> None:
    container_name = command(container_search)
    database_misc.docker_command("stop", container_name)

    return


def command(context_search) -> None:
    container_name = container_utils.get_container_name(context_search)

    return container_name



# callback to force single command app to still require command
@app.callback()
def callback():
    pass