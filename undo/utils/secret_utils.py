import os, sys
from pathlib import Path

from ansible.parsing.vault import VaultSecret, VaultLib, AnsibleVaultError
import typer

# undo specific imports
from undo.utils import const


def mask_secret(secret):
    secret_mask = secret[0:2] + "*****" + secret[-2:]

    return secret_mask


def get_secret(secret_path, *, show_error=False):
    secret = False
    secret_path = Path(secret_path)

    # if it file exists as passed in..
    if secret_path.exists():
        # if the file name starts with underscore, it isn't encrypted
        if secret_path.name.startswith("_"):
            secret = secret_path.read_text().strip()
        # otherwise, decrypt it
        else:
            secret = decrypt(secret_path)

    # otherwse maybe the file exists with an underscore but was passed in without?
    else:
        secret_plain_path = Path(secret_path.parent / ("_" + secret_path.name))
        if secret_plain_path.exists():
            secret = secret_plain_path.read_text().strip()

    # if neither of those resulted in a string being returned
    if show_error and not secret:
        typer.secho("\nRuh-roh!", fg=const.ERRR_TEXT_COLOUR)
        typer.secho(f"No secret found at path: {secret_path}")
        raise typer.Exit(1)

    return secret


def upsert_secret(secret_path=None, secret=None, *,
                    hide_input=True, skip_exists=False, secret_type=None):
    # quick aside, it's possible to force showing the passsword, if you need that
    if os.environ.get("SHOW_PASSWORD"): hide_input = False

    # make sure the secret path exists, ahead of trying to create it
    secret_file = Path(secret_path)
    secret_file.parent.mkdir(parents=True, exist_ok=True)
    Path(secret_file.parent / ".none").touch()

    # you can skip prompting if the file already exists
    # and just return the existing secret
    if skip_exists and secret_file.exists():
        secret = get_secret(secret_file)
        secret_mask = secret[0:2] + "*****"  + secret[-2:]
        typer.secho(f"\nSecret found at '{secret_file}':")
        typer.secho(f"\t{secret_mask}...")
        return secret

    # otherwise, if a secret wasn't already prompted, start by prompting
    if not secret:
        secret_type = " "+ secret_type if secret_type else ""
        secret = typer.prompt(f"Enter the{secret_type} secret",
                                    hide_input=hide_input)

    # then, if a secret does exist, double check if they wanna change it
    if secret_file.exists():
        # get (and decrypt) the secret
        existing_secret = decrypt(secret_file)

        # prompt a y/n to overwrite it
        echo = f"You already have a secret ({mask_secret(existing_secret)}), " \
                + "do you want to overwrite it?"
        typer.secho("\nCHECK", fg=const.WARN_TEXT_COLOUR)
        secret_check = typer.confirm(echo)

        # if they wanna change it, encrypt the new secret into the file
        if secret_check:
            encrypt(secret, secret_file)
            typer.secho("\nSecret updated!", fg=const.SCSS_TEXT_COLOUR)
        
        # otherwise thank them for their time
        else:
            secret = existing_secret
            typer.secho("\nSecret left alone!", fg=const.INFO_TEXT_COLOUR)

    # if there is no existing secret, save this one
    else:
        encrypt(secret, secret_file)
        typer.secho("\nSecret added!", fg=const.SCSS_TEXT_COLOUR)

    # return the secret we decided was this secret
    return secret


def get_vault(key_path=".vault/vault-pass.txt"):
    # double check the key path exists, otherwise raise an error
    key_path = Path(key_path)
    if not key_path.exists():
        raise typer.Exit(1)

    # extract the vault key from its path, and  convert it to a VaultSecret
    vault_key_text = Path(key_path).read_text().strip()
    vault_key = VaultSecret(vault_key_text.encode("utf-8"))

    # insantiate a vault library with the default vault_id
    vault = VaultLib([("default", vault_key)])

    return vault


def encrypt(secret, secret_path, *, key_path=".vault/vault-pass.txt"):
    # double check the folder in which we'll store the secret exits, otherwise...
    secret_path = Path(secret_path)
    if not secret_path.parent.exists():
        raise typer.Exit(1)

    # get the vault object and use it to encrypt the secret
    vault = get_vault(key_path)
    encrypted_secret = vault.encrypt(secret.encode("utf-8"))

    # then save the secret to the secret path
    Path(secret_path).write_text(encrypted_secret.decode("utf-8"))

    return secret_path


def decrypt(secret_path, *, key_path=".vault/vault-pass.txt"):
    # double check secret exits...
    secret_path = Path(secret_path)
    if not secret_path.exists():
        raise typer.Exit(1)
    
    # then get said secret
    secret = secret_path.read_text()

    # get the vault object and use it to decrypt the secret
    vault = get_vault(key_path)
    try:
        decrypted_secret = vault.decrypt(secret.encode("utf-8"))
    except AnsibleVaultError as ex:
        raise typer.Exit(1)

    return decrypted_secret.decode("utf-8").strip()