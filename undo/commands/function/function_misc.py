import typer

CODE_TEXT_COLOUR = typer.colors.BRIGHT_BLACK
INFO_TEXT_COLOUR = typer.colors.BRIGHT_YELLOW


def properties(context):
    with open(context / "function.properties") as f:
        prop_text = f.read().splitlines()

    properties = {
        "name": prop_text[0].split("=")[1].strip(),
        "version": prop_text[1].split("=")[1].strip()
    }

    typer.secho("\nExtracting from function.properties:\n")

    typer.secho("\tfunction_name=" + properties["name"], fg=INFO_TEXT_COLOUR)
    typer.secho("\tfunction_version=" + properties["version"] + "\n", fg=INFO_TEXT_COLOUR)

    return properties