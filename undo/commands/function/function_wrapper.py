import os, subprocess, shutil
import typer
from pathlib import Path

CODE_TEXT_COLOUR = typer.colors.BRIGHT_BLACK

def wrapper(context, routes=None, port=8000):
    # say tell and what you're doing
    intro_text(routes, port)

    # copy the wrapper.py file to the function directory
    copy_wrapper(context)

    # get the env vars from environment.txt
    env_vars = extract_env_vars(context)

    # actually start the wrapper server
    run_process(context, routes, port, env_vars)

    # when everything is done, remove the wrapper
    delete_wrapper(context)


def intro_text(routes, port):
    echo = "\nStarting HTTP wrapper for function.\n" \
           + f"- Running on port {port}.\n"
    if routes:
        echo += "- With routes: " \
                + typer.style(", ".join(routes.split()), bold=True) + "\n"
    else:
        echo += "- No routes selected.\n"

    typer.secho(echo)
    return echo


def copy_wrapper(context):
    # find the wrapper in this module
    unwrapper = Path(__file__).resolve().parent / "templates/unwrapper/wrapper.py"

    # tell people about it
    typer.secho(f"\nCopy wrapper code to working directory:")
    typer.secho(f"\tcp {unwrapper} {context}", fg=CODE_TEXT_COLOUR)

    # copy the wrapper file
    shutil.copyfile(unwrapper, context / "wrapper.py")


def extract_env_vars(context, env_file="environment.txt"):
    # set the env vars
    typer.secho(f"\nSet the environment variables:")
    env_vars = os.environ.copy()
    env_pairs = {}
    with open(context / env_file) as f:
        envs = f.read().splitlines()
        for env_var in envs:
            if env_var.startswith("#") or len(env_var) == 0: continue

            try:
                env_pair = env_var.strip().split("=")
                env_pairs[env_pair[0]] = env_pair[1]
            except Exception as ex:
                typer.secho(f"\tError parsing {env_var}", fg=CODE_TEXT_COLOUR)

    # print final set of env vars (excluding any that were overwritten)
    env_message = "\n".join([f"\texport {k}={v}" for k, v in env_pairs.items()])
    typer.secho(env_message, fg=CODE_TEXT_COLOUR)

    env_vars = { **env_vars, **env_pairs }
    return env_vars


def run_process(context, routes=None, port=8000, env_vars={}):
    # activate the venv and run the wrapper
    typer.secho(f"\nActivate virtual environment:")
    typer.secho(f"\tsource .venv/bin/activate", fg=CODE_TEXT_COLOUR)

    # activate the venv and run the wrapper with the supplied args
    command_args = [ ".venv/bin/python", "wrapper.py", str(port) ]
    if routes:
        command_args = command_args + [ route.strip() for route in routes.split() ]

    typer.secho(f"\nRun the wrapper script:")
    typer.secho(f"\tpython3 {' '.join(command_args)}", fg=CODE_TEXT_COLOUR)
    try:
        subprocess.run(command_args, env=env_vars, cwd=context)
    except KeyboardInterrupt:
        # prevent Ctrl+C (which ends the http server)
        # from immediately aborting the command
        pass


def delete_wrapper(context):
    echo = "\nClean up wrapper code:" \
           + typer.style(f"\trm {context.resolve()}/wrapper.py\n", fg=CODE_TEXT_COLOUR)

    typer.secho(echo)
    wrapper_path = context.resolve() / "wrapper.py"
    wrapper_path.unlink()
    return echo