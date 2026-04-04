import os, subprocess
import typer

# undo specific imports
from undo.utils import const
from undo.utils import container_utils
from undo.commands.database.database_arguments import config
from undo.commands.database import database_create, database_release, database_misc

app = typer.Typer(no_args_is_help=True)


@app.command("create", help=config["create"]["help"])
def create_command(database_name: config["create"]["database_name"],
                    password: config["create"]["password"] = None,
                    show_password: config["create"]["show_password"] = False) -> None:

    database_create.create(database_name,
                                password=password, hide_input=(not show_password))
    return


@app.command("init", help=config["init"]["help"])
def init_command(environment: config["init"]["environment"] = ...,
                    host: config["init"]["host"] = "127.0.0.1",
                    script_path: config["init"]["script_path"]
                        = "database/db_initialise.sql") -> None:

    database_release.release(script_path=script_path, env=environment, host=host)
    return


@app.command("release", help=config["release"]["help"])
def release_command(environment: config["release"]["environment"] = ...,
                    script_path: config["release"]["script_path"] = ...,
                    host: config["release"]["host"] = "127.0.0.1") -> None:

    database_release.release(env=environment, host=host, script_path=script_path)
    return


@app.command("select", hidden=True)
@app.command("statement", help=config["statement"]["help"])
def statement_command(statement: config["statement"]["statement"] = "SHOW DATABASES",
                    env: config["statement"]["environment"] = "local",
                    database_name: config["statement"]["database_name"] = None) -> None:

    database_misc.mysql_statement(statement, env, database_name)
    return


@app.command("secret", help=config["secret"]["help"])
def secret_command(password: config["create"]["password"] = None,
                    show_password: config["create"]["show_password"] = False) -> None:

    database_misc.upsert_password(password=password, hide_input=(not show_password))
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