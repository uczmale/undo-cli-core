import typer
from typing import Annotated


config = {
    "context_search": Annotated[str, typer.Argument(
        metavar="CONTAINER_NAME",
        show_default=False,
        help="The name of container for the database (often just the app name + db)"
    )],

    "encrypt": {
        "path": Annotated[str, typer.Option(
            "--file-path", "-f",
            help="The full path, including file name, to store the encrypted secret"
        )],
        "secret": Annotated[str, typer.Option(
            "--secret", "-s",
            help="The actual password or secret content to be encrypted"
        )],
        "overwrite": Annotated[bool, typer.Option(
            "--overwrite", "-o",
            help="If the password already exists, overwrite it "
        )],
        "help": "Encrypt a string to a file"
    },

    "decrypt": {
        "path": Annotated[str, typer.Option(
            "--file-path", "-f",
            help="The full path, including file name of the secret being decrypted"
        )],
        "raw": Annotated[bool, typer.Option(
            "--raw", "-r",
            help="Return the password as just the string with no whitespace"
        )],
        "help": "Decrypt a secret and print it to screen"
    },

    "generate": {
        "length": Annotated[int, typer.Option(
            "--length", "-l",
            help="The number of characters you want to generate"
        )],
        "help": "Generate a random string"
    }
}