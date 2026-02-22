import typer
from typing_extensions import Annotated


config = {
    "context_search": Annotated[str, typer.Argument(
        metavar="CONTAINER_NAME",
        show_default=False,
        help="The name of container for the database (often just the app name + db)"
    )],
    "start": {
        "container_search": Annotated[str, typer.Argument(
            metavar="CONTAINER_NAME",
            show_default=False,
            help="The name of container for the database (often just the app name + db)"
        )],
        "help": "Start the container of the database"
    },
    "stop": {
        "container_search": Annotated[str, typer.Argument(
            metavar="CONTAINER_NAME",
            show_default=False,
            help="The name of container for the database (often just the app name + db)"
        )],
        "help": "Stop the container of the database"
    }
}