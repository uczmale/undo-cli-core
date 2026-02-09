import os, sys, re
from pathlib import Path

import typer


def get_execution_directory(cwd=None):
    execute_dir = Path(cwd if cwd else os.getcwd())
    check_dir = execute_dir
    check_file = os.environ.get("UNDO_ROOT_CHECK_FILE", ".git")
    root_check = check_dir / check_file

    # until you find a .git in the directory, keep moving up to parents
    while not root_check.exists():
        root_check = check_dir / check_file

        # if there's a .git, assume this is the root dir
        if root_check.exists():
            execute_dir = check_dir
            break

        # if you hit the root root and the parent is the current
        # and the original, actually current execute_dir will be returned
        if check_dir.resolve() == check_dir.resolve().parent:
            break

        check_dir = check_dir.resolve().parent

    return execute_dir


def get_command_directory(dir_name, dir_type):
    command_dir = get_execution_directory() / dir_name

    if not command_dir.exists():
        typer.secho(f"There's are no {dir_type}s defined.", fg=typer.colors.RED)
        raise typer.Exit(1)

    return command_dir


def get_fuzzy_subdirectory(main_directory, subdir_mask, search_type, raise_error=True):
    # expects the main directory and the subdirectory, which defaults to None
    # the main directory should already have been checked to exist
    # (everything after this expects strings though, so, cast to string)
    subdir_mask = subdir_mask if subdir_mask else ""

    # get this directory we think we're getting
    check_dir = main_directory / subdir_mask

    # if we weren't passed anything
    # or what we were passed isn't directly a directory, then..
    if not subdir_mask or not check_dir.is_dir():
        # create search string for glob
        # needs to be exactly one asterisk for wildcard
        # two asterisks start to do multi-level searches - which we don't want
        # three asterisks cause an error
        context_search = re.sub(r"\*+", "*", ("*" +  subdir_mask + "*"))
        search_rslt = list(main_directory.glob(context_search))

        if len(search_rslt) > 1:
            # if multiple found, give user the choice
            if subdir_mask:
                mssg = (f"There are multiple {search_type}s that match {subdir_mask}, "
                        + "please choose one:\n\n\t- ")
            else:
                mssg = f"There are multiple {search_type}s, please choose one:\n\n\t- "

            mssg += "\n\t- ".join([i.name for i in search_rslt]) + "\n"

            if raise_error:
                typer.secho(mssg, fg=typer.colors.RED)
                raise typer.Exit(1)
            else:
                return [i.name for i in search_rslt]

        elif len(search_rslt) == 1:
            return search_rslt[0]

        elif raise_error == False:
            return False

        else:
            # raise an error if nothing is found and we're raising
            if subdir_mask:
                typer.secho(f"No {search_type} found that matches {subdir_mask}",
                                fg=typer.colors.RED)
            else:
                typer.secho(f"No {search_type}s found, create one", fg=typer.colors.RED)
            raise typer.Exit(1)

    else:
        return check_dir
