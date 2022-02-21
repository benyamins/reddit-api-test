from .db import DBConnection
from .settings import SUPPORTED_SECTIONS

import argparse
import sys


def get_args() -> argparse.Namespace:

    description = """Download DB of Saved, Updvoted, History, etc posts. 
                        through reddits API"""

    parser = argparse.ArgumentParser(description=description, prog="reddit")

    subparser: argparse._SubParsersAction = parser.add_subparsers(help="subcomand")

    subparser_list: argparse.ArgumentParser = subparser.add_parser(
        "list", help="List Help"
    )
    subparser_list.add_argument("sub", nargs="?", help="Id of sub")

    subparser_open: argparse.ArgumentParser = subparser.add_parser(
        "open", help="Open Help"
    )
    subparser_open.add_argument("id", help="Id of link to open")

    subparser_update: argparse.ArgumentParser = subparser.add_parser(
        "update", help="Update Help"
    )
    subparser_update.add_argument("db", nargs="?")

    subparser_update: argparse.ArgumentParser = subparser.add_parser(
        "select", help="Select Help"
    )
    subparser_update.add_argument("selected_db", nargs="?")

    args: argparse.Namespace = parser.parse_args()

    if args == argparse.Namespace():
        parser.print_help()
        sys.exit(1)

    return args


def proc_args(args: argparse.Namespace) -> None:

    if hasattr(args, "sub"):
        # TODO: if content is null then ask for update
        print(args)

    if hasattr(args, "id"):
        print(args)

    if hasattr(args, "db"):
        print(args)

    if hasattr(args, "selected_db"):
        # What do we support? everything in
        if args.selected_db not in SUPPORTED_SECTIONS:
            print(f"{args.selected_db} isn't a valid reddit user secction")
        else:
            connection = DBConnection(f"{args.selected_db}")
            connection.select_db()


def main() -> None:

    # Start DB if none

    # Pase args
    arguments: argparse.Namespace = get_args()
    proc_args(arguments)


if __name__ == "__main__":
    main()
