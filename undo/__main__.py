from undo import cli, __app_name__

def main():
    try:
        cli.app(prog_name=__app_name__)
    finally:
        print("")

if __name__ == "__main__":
    main()