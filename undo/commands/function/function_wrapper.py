import os, subprocess, shutil
import typer
from pathlib import Path

# project specific imports
from undo.commands.function.helpers import function_wrapper_route_parser
from undo.utils import secret_utils

CODE_TEXT_COLOUR = typer.colors.BRIGHT_BLACK

help_text = "Run a wrapper which lets you access your API locally"

def wrapper(context, routes=None, port=8000, no_routes=False):
    # say tell and what you're doing
    intro_text(routes, port)

    # copy the wrapper.py file to the function directory
    copy_wrapper(context)

    # get the env vars from environment.txt and /secrets
    env_vars = extract_env_vars(context)
    env_secrets = extract_env_secrets(context)

    # get the routes automatically from handler.py, unless explicitly overriden
    routes = extract_routes(context, routes, no_routes)

    # actually start the wrapper server
    run_process(context, routes, port, { **env_vars, **env_secrets })

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
    typer.secho(f"\nSetting the environment variables:")
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


def extract_env_secrets(context):
    # set the env vars
    typer.secho(f"\nSetting the secret environment variables:")
    env_vars = {}

    # i guess if there are no secrets..?
    if not Path(context / "secrets").exists():
        return env_vars

    # otherwise, go through all the files in the secrets folder
    # and add them to the list (skipping .none and removing lead underscores)
    for secret_path in Path(context / "secrets").iterdir():
        if secret_path.name == ".none": continue
        secret = secret_utils.get_secret(secret_path)

        if secret_path.name.startswith("_"):
            secret_name = secret_path.name[1:]
        else:
            secret_name = secret_path.name

        env_vars[secret_name] = secret

    # print final set of env vars (excluding any that were overwritten)
    env_message = "\n".join([f"\texport {k}={secret_utils.mask_secret(v)}"
                                    for k, v in env_vars.items()])
    typer.secho(env_message, fg=CODE_TEXT_COLOUR)

    return env_vars


def extract_routes(context, routes=None, no_routes=False):
    # routes come in as a string --routes '/undo /undo/{identifier}'
    routes = [ route.strip() for route in routes.split() ] if routes else []

    # if they've not set --no-auto-routes (no_routes) then try to get routes from handler
    if not no_routes:
        route_list = extract_handler_routes(context)

        if routes and route_list:
            routes = list(dict.fromkeys(routes + route_list))
            typer.secho(f"Extracted merged with param routes: " + ", ".join(route_list))
        elif route_list:
            routes = route_list
        else:
            typer.secho(f"Just using parameter routes: " + ", ".join(routes))
    else:
        typer.secho(f"Skipping auto-extract from handler.py..")

        if routes:
            typer.secho(f"Using parameter routes: " + ", ".join(routes))

    return routes


def extract_handler_routes(context):
    # i mean, this does all the heavy lifting, go look at that
    visitor = function_wrapper_route_parser.RouteVisitor()

    # assume the routes are the handler file, right? right?
    typer.secho(f"\nExtracting routes from handler/handler.py...")
    visitor.parse_handler(context / "handler/handler.py")
    
    # then, with the routes returned, just get the /path/mask
    # and then use the list(dict.fromkeys()) thing to dedupe the list
    route_list = list(dict.fromkeys([r.split()[1].strip() for r in visitor.route_list]))

    if len(route_list) > 0:
        typer.secho(f"Extracted {len(route_list)} routes: " + ", ".join(route_list))
    else:
        typer.secho(f"No routes auto-detected in handler.py. Check your standards.")

    return route_list


def run_process(context, routes=None, port=8000, env_vars={}):
    # activate the venv and run the wrapper
    typer.secho(f"\nActivate virtual environment:")
    typer.secho(f"\tsource .venv/bin/activate", fg=CODE_TEXT_COLOUR)

    # activate the venv and run the wrapper with the supplied args
    command_args = [ ".venv/bin/python", "wrapper.py", str(port) ]
    if routes:
        command_args = command_args + routes

    # TODO: make it silent, add the ampersand or pipe it to log or such...
    # something like... > wrapper.log 2>&1 &
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