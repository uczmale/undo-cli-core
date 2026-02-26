import typer
from typing_extensions import Annotated


config = {
    "context_search": Annotated[str, typer.Argument(
        metavar="CONTAINER_NAME",
        show_default=False,
        help="The name of container for the database (often just the app name + db)"
    )],

    "create": {
        "database_name": Annotated[str, typer.Argument(
            metavar="DATABASE_NAME",
            show_default=False,
            help="The base name of the database being created"
        )],
        "password": Annotated[str, typer.Option(
            "--password", "-p",
            prompt="Enter admin password for database",
            prompt_required=False,
            help="The master admin password, injected into the container at start"
        )],
        "show_password": Annotated[bool, typer.Option(
            "--show-password", "-s",
            help="Show the password when typing it"
        )],
        "skip_password": Annotated[bool, typer.Option(
            "--skip-password", "-k",
            help="Skip password if one already exists"
        )],
        "help": "Create a container in which to house a database"
    },

    "init": {
        "environment": Annotated[str, typer.Option(
            metavar="TARGET",
            show_default=False,
            help="Genreally the environment but potentially the database's target"
        )],
        "host": Annotated[str, typer.Option(
            "--host", "-h"
            metavar="DATABASE_NAME",
            show_default=False,
            help="The host address of the database"
        )],
        "script_path": Annotated[bool, typer.Option(
            "--script-path", "-s",
            help="Skip password if one already exists"
        )],
        "help": "Run the initialisation script to create the core new database"
    },

    "secret": {
        "password": Annotated[str, typer.Option(
            "--password", "-p",
            prompt="Enter admin password for database",
            hide_input=True,
            prompt_required=False,
            help="The master admin password, injected into the container at start"
        )],
        "show_password": Annotated[bool, typer.Option(
            "--show-password", "-s",
            help="Set this if you want to show the password when typing it"
        )],
        "decrypt": Annotated[bool, typer.Option(
            "--decrypt", "-d",
            help="Print the password stored in the vault plain text to screen"
        )],
        "help": "Create or update the master admin password for the database"
    },

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