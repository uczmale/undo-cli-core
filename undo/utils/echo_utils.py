import typer

colour_level = {
    "success": typer.colors.GREEN,
    "error": typer.colors.RED,
    "warning": typer.colors.BLUE,
    "code": typer.colors.BRIGHT_BLACK,
    "info": typer.colors.BRIGHT_YELLOW,
}

def echo(text, *, title=None, level=None, nl=True, prebreak=True):
    colourway = colour_level.get(level, typer.colors.WHITE)

    pre = "\n"
    if title:
        typer.secho(pre + title, fg=colourway)
        pre = ""

    typer.secho(pre + text, nl=nl)

    return text


def echo_command(lines):
    if isinstance(lines, str):
        lines = [ l.strip() for l in lines.split("\\") ]


    # figure out the number of spaces at the start of each subsequent line
    # based on the length of the first command
    tabs = (" " * len(lines[0].split(" ")[0])) + " "

    # so if there're multiple lines
    # each subsequent line starts at the end of the first command
    # and each line will start with a tab:
    # \tdocker run \
    # \t       -p 80:80 \
    # \t       -e "ENV=dev" \
    text = "\t" + f" \\\n\t{tabs}".join(lines)

    return text
