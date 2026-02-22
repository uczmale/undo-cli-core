import os, subprocess
import typer

# undo specific imports
from undo.utils import const


def get_container_name(name_search):
    result = subprocess.run("docker ps -a --format '{{.Names}}'", shell=True,
                                capture_output=True, text=True, check=True)
    names = [name for name in result.stdout.splitlines() if name_search in name]

    if len(names) == 1:
        return names[0]

    if len(names) == 0:
        typer.secho(f"No container found that matches {name_search}",
                        fg=typer.colors.RED)
        raise typer.Exit(1)

    else:
        if name_search:
            echo_warn = f"Multiple containers match '{name_search}', select one:"
        else:
            echo_warn = f"There are multiple containers, select one:"
        echo = "\t- " + "\n\t- ".join(names)

        typer.secho(echo_warn, fg=const.WARN_TEXT_COLOUR)
        typer.secho(echo)

        raise typer.Exit(1)