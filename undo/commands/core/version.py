import typer
from undo import __app_name__, __version__

def params():
    return typer.Option(None, "--version", "-v",
                            help="Show the application's version and exit.",
                            callback=version_callback, is_eager=True)

def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()