from typing import Optional
import typer
import time

from undo.commands.core import version
from undo.commands.frontend import frontend as fr
from undo.commands.function import function as fn

app = typer.Typer(rich_markup_mode=None)

# z function wrapper|...
app.add_typer(fn.app, name="function")
app.add_typer(fn.app, name="fn", hidden=True)

# z function wrapper|...
app.add_typer(fr.app, name="frontend")
app.add_typer(fr.app, name="fr", hidden=True)

# @app.command()
# def docs(area: str, topic: str = typer.Argument(default="[list]")) -> None:
#     docs_command(area, topic)
#     return


@app.callback()
def main(version: Optional[bool] = version.params()) -> None:
    return
