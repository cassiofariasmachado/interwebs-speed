from datetime import datetime

from interwebs_speed import __app_name__, __version__, cli


def main():
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
