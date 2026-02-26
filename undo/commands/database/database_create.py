import os, subprocess
import typer
from pathlib import Path

# undo specific imports
from undo.utils import const
from undo.utils import dir_utils
from undo.commands.database import database_misc


def create(database_name, password, hide_input=True):
    # get the password or ask for one from the user
    password = database_misc.upsert_password(password, hide_input, skip_exists=True)

    # get the database folder for the project (create if not)
    database_path = initialise_database_directory()

    container_name = database_name + "db"

    echo = "\tdocker run -d \\\n" \
          f"\t             -e MYSQL_ROOT_PASSWORD=$(cat .vault/db_password) \\\n" \
           "\t             -p 3306:3306 \\\n" \
           "\t             -v ./database/local-config/my.conf:/etc/my.conf \\\n" \
          f"\t             --name {container_name} mysql:8.4 mysqld \\\n" \
           "\t             --mysql-native-password=ON \\\n"

    typer.secho("\nRunning the MySQL container..")
    typer.secho(echo, fg=const.CODE_TEXT_COLOUR)

    # the actual docker command to run
    # TODO: have a think about the f-strings and shell injection maybe?
    docker_command = "docker run -d " \
                        f"-e MYSQL_ROOT_PASSWORD={password} " \
                        "-p 3306:3306 " \
                        "-v ./database/local-config/my.conf:/etc/my.conf " \
                        f"--name {container_name} mysql:8.4 mysqld " \
                        "--mysql-native-password=ON"

    result = subprocess.run(docker_command, shell=True)

    return result


def initialise_database_directory():
    execution_dir = dir_utils.get_execution_directory()
    database_path = Path(execution_dir / "database")
    local_config = Path(database_path / "local-config")
    local_config.mkdir(parents=True, exist_ok=True)

    my_conf = Path(local_config / "my.conf")
    if not my_conf.exists():
        typer.secho("\nCreating 'database/local-config/my.conf' file")
        my_conf.write_text("[mysqld]\nmysql_native_password=ON")

    return database_path