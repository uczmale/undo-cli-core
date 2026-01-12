from typing import Optional
import typer
import time

from undo.commands.core import version
from undo.commands.frontend import frontend as fr
from undo.commands.function import function as fn

app = typer.Typer()

@app.command("fe", hidden=True)
@app.command("frontend")
def frontend_command(operation: str, context: str = typer.Argument(default="")) -> None:
    fr.command(operation, context)
    return


@app.command("fn", hidden=True)
@app.command("function")
def function_command(
        operation: str = fn.OPERATION,
        context: str = fn.CONTEXT,
        routes: Optional[str] = fn.ROUTES,
        port: Optional[str] = fn.PORT,
        no_routes: Optional[bool] = fn.NO_ROUTES
        ) -> None:
    fn.command(operation, context, opts=locals())
    return


# @app.command()
# def docs(area: str, topic: str = typer.Argument(default="[list]")) -> None:
#     docs_command(area, topic)
#     return


@app.callback()
def main(version: Optional[bool] = version.params()) -> None:
    return
