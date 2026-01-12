import os
import typer


_operation = {
    "default": ...,
    "help": "Choose from: wrapper, properties.."
}
OPERATION = typer.Argument(**_operation)

_context = {
    "default": None,
    "metavar": "FUNCTION_NAME",
    "show_default": False,
    "help": "The name of the function or the smallest unique part"
}
CONTEXT = typer.Argument(**_context)

_routes = {
    "help": "Route masks in the form '/entity /entity/{identifier}'."
}
ROUTES = typer.Option(None, "--routes", **_routes)

_port = {
    "help": "Override the default port if it is in use."
}
PORT = typer.Option(8000, "--port", **_port)
