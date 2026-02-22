import typer

# undo specific imports
from undo.utils import dir_utils
from undo.commands.function.function_arguments import config
from undo.commands.function import function_misc, function_wrapper

app = typer.Typer(no_args_is_help=True)

CODE_TEXT_COLOUR = typer.colors.BRIGHT_BLACK
INFO_TEXT_COLOUR = typer.colors.BRIGHT_YELLOW


@app.command("wrapper", help=function_wrapper.help_text)
def wrapper_command(context_search: config["context_search"] = "",
                    routes: config["wrapper"]["routes"] = None,
                    port: config["wrapper"]["port"] = 8000,
                    no_routes: config["wrapper"]["no_routes"] = False) -> None:

    command_dir, context, function_name = command(context_search)
    function_wrapper.wrapper(context, routes=routes, port=port, no_routes=no_routes)
    return


@app.command("properties", help=config["properties"]["help"])
def properties_command(context_search: config["context_search"] = "") -> None:
    command_dir, context, function_name = command(context_search)
    function_misc.properties(context)
    return


def command(context_search):
    command_dir = dir_utils.get_command_directory("functions", "function")
    context = dir_utils.get_fuzzy_subdirectory(command_dir, context_search, "function")

    function_name = context.name.replace("_", "-")
    typer.secho(f"Function {function_name} selected..\n")

    # okay, so, we know what folder we're doing all this stuff in
    # let's go there (while remembering how to get back)

    typer.secho(f"Switching to directory to execute commands:")
    typer.secho(f"\tcd {context}", fg=CODE_TEXT_COLOUR)

    return command_dir, context, function_name