# undn CLI

The Unified Namespace for Development and Operation CLI.

## Getting started

This is all just following: https://realpython.com/python-typer-cli/

Initialise the environment:

        # get all set all up
        python3 -m venv ./.venv
        source .venv/bin/activate
        pip install -r requirements.txt

Run the CLI as a a CLI you can run from anywhere in this folder using the command undn:

        # install the package in editable mode
        source .venv/bin/activate
        python3 -m pip install -e .

        # check it worked
        undn --version

Finally, to build the package as something you can install..:

        # get up to date with the software
        python3 -m pip install --upgrade pip
        python3 -m pip install --upgrade build

        # build the package
        python3 -m build
        
        # install the package you've built, i guess, as non-editable
        python3 -m pip install .
