import typer
from undn import __app_name__, __version__

def params():
    return typer.Option(None, "--type", "-t",
                            help="Show guide to undn and development in general.",
                            callback=docs_callback)


def command(area, topic) -> None:
    if area == "undn":
        undn_help(topic)
    else:
        snippets(topic)


def undn_help(topic):
    print("undn is a cli, it's not that deep")


def snippets(topic):
    typer.secho(f"Learn some stuff", fg=typer.colors.GREEN)

