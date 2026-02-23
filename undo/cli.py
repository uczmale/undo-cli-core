from typing import Optional
import typer
import time, sys

from undo.commands.core import version
from undo.commands.database import database as db
from undo.commands.function import function as fn
from undo.commands.frontend import frontend as fr
from undo.commands.secret import secret as sc

app = typer.Typer(no_args_is_help=True, rich_markup_mode=None)

# z function wrapper...
app.add_typer(fn.app, name="function")
app.add_typer(fn.app, name="fn", hidden=True)

# z frontend run...
app.add_typer(fr.app, name="frontend")
app.add_typer(fr.app, name="fr", hidden=True)

# z database start...
app.add_typer(db.app, name="database")
app.add_typer(db.app, name="db", hidden=True)

# z database start...
app.add_typer(sc.app, name="secret")
app.add_typer(sc.app, name="sc", hidden=True)

# @app.command()
# def docs(area: str, topic: str = typer.Argument(default="[list]")) -> None:
#     docs_command(area, topic)
#     return


@app.callback()
def main_command(version: Optional[bool] = version.params()) -> None:
    return


def main():
    # ensures there's always a line break after every command..
    try:
        app()
    finally:
        print("")