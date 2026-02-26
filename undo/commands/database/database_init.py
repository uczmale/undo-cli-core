import os, shutil, subprocess
import typer
from pathlib import Path

# undo specific imports
from undo.utils import const
from undo.utils import dir_utils, secret_utils
from undo.commands.database import database_misc


def init(script_path, env, host="127.0.0.1"):
    # start setting up the placeholder map
    placeholder_mapping = [("<ENV>", env)]

    # get the admin password and add it to that map
    password_path = Path(".vault/db_password")
    admin_password = secret_utils.get_secret(password_path)
    placeholder_mapping.append(("ADMIN_PASSWORD", admin_password))

    # send the placeholder map to update the placeholders in the script
    # and return the path of the tmp script created
    updated_script_path = update_script(script_path, placeholder_mapping)

    # run script with the admin password again, maybe, localhost?
    run_script(updated_script_path, host, admin_password)

    # remove the temp script
    shutil.rmtree(updated_script_path.parent)


def update_script(script_path, placeholder_mapping):
    # confirm the script exists...
    if not script_path.exists():
        script_name = script_path.name
        typer.secho("Erreur", fg=const.ERRR_TEXT_COLOUR)
        typer.secho(f"The script - {script_name} - doesn't seem to exist")
        raise typer.Exit(1)

    # create a temp dir for the changed script
    typer.secho("Copy script to a temporary directory:")
    temp_path = Path(script_path.parent / "tmp")
    typer.secho(f"\tcp {script_path} {temp_path}", fg=const.CODE_TEXT_COLOUR)
    temp_path.mkdir(parents=True, exist_ok=True)

    # get the text of the input script and swap out all the placeholders
    typer.secho("Update the temporary script to swap out the password")
    updated_script = script_path.read_text()
    updated_script_path = Path(temp_path / script_path.name)
    for p in placeholder_mapping:
        echo = "\tsed -i \"s/{p[0]}/{p[1]}/g\" {updated_script_path}"
        typer.secho(echo, ft=const.CODE_TEXT_COLOUR)
        updated_script = updated_script.replace(p[0], p[1])

    # write the new script to the temporary directory
    updated_script_path.write_text(updated_script)

    return updated_script_path

def run_script(script_path, host, password):
    # pass the tmp script
    password_mask = password[0:2] + "*****" + password[-2:]
    echo = f"\tmysql --host {host} \\" \
            "\t      --port 3306 -u root \\" \
           f"\t      -p{password_mask} \\" \
           f"\t         < {script_path}"
    typer.secho("Run the updated script into MySQL..")
    typer.secho(echo, fg=const.CODE_TEXT_COLOUR)

    command = f"mysql --host {host} --port 3306 " \
              f"-u root -p{password} < {script_path}"
    result = subprocess.run(command, shell=True)

    return result