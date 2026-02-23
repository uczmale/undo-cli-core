import typer
from typing_extensions import Annotated


config = {
    "context_search": Annotated[str, typer.Argument(
        metavar="CONTAINER_NAME",
        show_default=False,
        help="The name of container for the database (often just the app name + db)"
    )],

    "generate": {
        "characters": Annotated[int, typer.Option(
            "--characters", "-c",
            help="The number of characters you want to generate"
        )],
        "help": "Generate a random string"
    }
}