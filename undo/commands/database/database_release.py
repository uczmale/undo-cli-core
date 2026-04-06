import os, shutil, subprocess, re
import typer
from pathlib import Path

# undo specific imports
from undo.utils import const
from undo.utils import dir_utils, secret_utils
from undo.commands.database import database_misc


default_database_host = "127.0.0.1"
default_script_path = "database/db_initialise.sql"
default_username = "easikit_admin"

def release(script_path, env, host=default_database_host):
    # start setting up the placeholder map
    placeholder_mapping = [("<ENV>", env)]

    # get admin password
    password_path = Path(f"database/release/secrets/{env}/db_local_password_root")
    admin_password = secret_utils.get_secret(password_path, show_error=True)

    # get script path, including filler bits
    script_path = get_script_path(script_path)

    # get placeholders, get the passwords and add to placeholder mapping
    placeholder_passwords = extract_placeholders(script_path)
    for password_type in placeholder_passwords:
        password_mapping(placeholder_mapping, password_type, env)

    # send the placeholder map to update the placeholders in the script
    # and return the path of the tmp script created
    updated_script_path = update_script(script_path, placeholder_mapping)

    # run script with the admin password again, maybe, localhost?
    run_script(updated_script_path, host, default_username, admin_password)

    # remove the temp script
    shutil.rmtree(updated_script_path.parent)


def get_script_path(script_path):
    path_test = Path(script_path)

    if not path_test.exists():
        path_test = Path(f"database/{script_path}.sql")

    if not path_test.exists():
        typer.secho("Ruh-roh!", fg=const.ERRR_TEXT_COLOUR)
        typer.secho(f"The path '{script_path}' doesn't exist in the database folder")
        raise typer.Exit(1)

    return path_test


def extract_placeholders(script_path):
    # get the sql text from the script
    sql_text = script_path.read_text()

    # get all the password references, extract the big before _PASSWORD
    # convert to lowercase, dedupe with set
    placeholders = {p.lower() for p in re.findall(r"<([\w]+)_PASSWORD>", sql_text)}

    return placeholders


def password_mapping(placeholder_mapping, password_type, env):
    # get the admin password and add it to that map
    default_path = "database/release/secrets/%s/db_%s_password_%s"
    password_path = Path(default_path % (env, env, password_type))
    password = secret_utils.upsert_secret(password_path, skip_exists=True,
                                            secret_type=f"database {password_type}")

    placeholder_mapping.append((f"<{password_type.upper()}_PASSWORD>", password))

    return password


def update_script(script_path, placeholder_mapping):
    # confirm the script exists...
    if not script_path.exists():
        script_name = script_path.name
        typer.secho("Erreur", fg=const.ERRR_TEXT_COLOUR)
        typer.secho(f"The script - {script_name} - doesn't seem to exist")
        raise typer.Exit(1)

    # create a temp dir for the changed script
    typer.secho("Copy database script to a temporary directory:")
    temp_path = Path(script_path.parent / "tmp")
    typer.secho(f"\tcp {script_path} {temp_path}", fg=const.CODE_TEXT_COLOUR)
    temp_path.mkdir(parents=True, exist_ok=True)

    # get the text of the input script and swap out all the placeholders
    typer.secho("\nUpdate the temporary script to swap out the password")
    updated_script = script_path.read_text()
    updated_script_path = Path(temp_path / script_path.name)
    for p in placeholder_mapping:
        echo_replacement = f"{p[1][0:2]}*****{p[1][-2:]}" if "PASS" in p[0] else p[1]
        echo = f"\tsed -i \"s/{p[0]}/{echo_replacement}/g\" {updated_script_path}"
        typer.secho(echo, fg=const.CODE_TEXT_COLOUR)
        updated_script = updated_script.replace(p[0], p[1])

    # write the new script to the temporary directory
    updated_script_path.write_text(updated_script)

    return updated_script_path


def run_script(script_path, host, username, password):
    # pass the tmp script
    password_mask = password[0:2] + "*****" + password[-2:]
    echo = f"\tmysql --host {host} --port --verbose \\\n" \
           f"\t      -u {username} -p{password_mask} \\\n" \
           f"\t         < {script_path}"
    typer.secho("\nRun the updated script into MySQL..")
    typer.secho(echo, fg=const.CODE_TEXT_COLOUR)

    command = f"mysql --host {host} --port 3306 --verbose " \
              f"-u {username} -p{password} < {script_path}"
    result = subprocess.run(command, shell=True)

    typer.secho("\nWhoop! Script complete!", fg=const.SCSS_TEXT_COLOUR)
    return result
