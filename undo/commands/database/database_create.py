import os, subprocess
import typer
from pathlib import Path

# undo specific imports
from undo.utils import const


def create(database_name, password, hide_input=True):
    password_file = Path(".vault/db_password")

    if password_file.exists():
        

    if not password:
        password = typer.prompt("Enter the main admin password",
                                    hide_input=silent_password)

    return