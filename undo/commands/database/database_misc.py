import os, subprocess
import typer
from pathlib import Path

# undo specific imports
from undo.utils import const
from undo.utils import secret_utils


default_database_host = "127.0.0.1"
default_script_path = ".database/db_initialise.sql"
default_username = "root"

def mysql_statement(statement, database_name=None):
    # get admin password
    password_path = Path(".vault/db_password")
    admin_password = secret_utils.get_secret(password_path)

    # echo command
    database_command = f"-D {database_name} " if database_name else ""
    database_command_echo = f"\t      {database_command}\\\n" if database_name else ""
    echo = f"\tmysql --host {default_database_host} --port 3306 \\\n" \
           f"\t      -u {default_username} -p$(cat .vault/db_password) \\\n" \
           f"{database_command_echo}" \
           f"\t      -e \"{statement}\"\n"
    typer.secho(f"Running database statement..")
    typer.secho(echo, fg=const.CODE_TEXT_COLOUR)

    command = f"mysql --host {default_database_host} --port 3306 " \
              f"-u {default_username} -p{admin_password} {database_command}" \
              f"-e \"{statement}\""
    result = subprocess.run(command, shell=True)
    return result


def docker_command(command, container_name):
    if command not in ["start", "stop", "restart", "rm"]:
        typer.secho(f"The command {command} is not supported; " \
                     "the only commands available are start, stop, restart and rm",
                fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho(f"Running docker command..")
    typer.secho(f"\tdocker {command} {container_name}\n", fg=const.CODE_TEXT_COLOUR)

    result = subprocess.run(f"docker {command} {container_name}", shell=True)
    return result


def upsert_password(password=None, *, env="local", user_type="root",
                            hide_input=True, skip_exists=False):
    
    # set up the database specific password path and create it if it doesn't exist
    # this is probably happening during database create command after all
    password_path = Path(f"database/release/{env}/")
    password_path.mkdir(parents=True, exist_ok=True)

    # put it all together and what have you got
    password_file = Path(password_path / f"db_password_{user_type}")

    # ding dong, password
    password = secret_utils.upsert_secret(password_file, password,
                                                hide_input=hide_input,
                                                skip_exists=skip_exists,
                                                secret_type="database admin")

    return password