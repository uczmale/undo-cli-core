import typer
from typing_extensions import Annotated


config = {
    "context_search": Annotated[str, typer.Argument(
        metavar="FRONTEND_NAME",
        show_default=False,
        help="The name of the frontend or the smallest unique part"
    )],
    "run": {
        "help": "Run the React app locally with the dev environment variables"
    }
}