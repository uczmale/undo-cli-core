import os, subprocess
import typer
from pathlib import Path

# undo specific imports
from undo.utils import const
from undo.utils import dir_utils
from undo.commands.database import database_misc


def create(database_name, password, hide_input=True):

    # get the password or ask for one from the user
    password = database_misc.upsert_secret(password, hide_input)

    # get the database folder for the project (create if not)
    database_path = initialise_database_directory()


    echo = "docker run -d " \
                        f"-e MYSQL_ROOT_PASSWORD=$(cat .vault/db_password) " \
                        "-p 3306:3306 " \
                        "-v ./database/local-config/my.conf:/etc/my.conf " \
                        "--name ctrldb mysql:8.4 mysqld --mysql-native-password=ON"

    docker_command = "docker run -d " \
                        f"-e MYSQL_ROOT_PASSWORD={password} " \
                        "-p 3306:3306 " \
                        "-v ./database/local-config/my.conf:/etc/my.conf " \
                        "--name ctrldb mysql:8.4 mysqld --mysql-native-password=ON"

    return

def initialise_database_directory():
    execution_dir = dir_utils.get_execution_directory()
    database_path = Path(execution_dir / "database/db_password")
    database_path.parent.mkdir(parents=True, exist_ok=True)

    local_config = Path(database_path / "local-config")
    database_path.parent.mkdir(parents=True, exist_ok=True)

    return database_path