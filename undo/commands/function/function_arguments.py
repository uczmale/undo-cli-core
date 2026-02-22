import typer
from typing_extensions import Annotated


config = {
    "context_search": Annotated[str, typer.Argument(
        metavar="FUNCTION_NAME",
        show_default=False,
        help="The name of the function or the smallest unique part"
    )],
    "wrapper": {
        "routes": Annotated[str, typer.Option(
            "--routes", "-r",
            help="Route masks in the form '/entity /entity/{identifier}'."
        )],
        "port": Annotated[int, typer.Option(
            "--port", "-p",
            show_default=False,
            help="Override the default port if it is in use [default: 8000]."
        )],
        "no_routes": Annotated[bool,  typer.Option(
            "--no-auto-routes", "-n",
            help="Prevents routes being inferred from handler/handler.py."
        )]
    },
    "properties": {
        "help": "Show the name and version details for the function"
    }
}