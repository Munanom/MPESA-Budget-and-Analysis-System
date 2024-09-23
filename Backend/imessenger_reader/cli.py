#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line tool for fetching and processing messages from the chat.db file on macOS.
This script provides functionalities to extract messages from the macOS Messages database (`chat.db`) and export the data in various formats or display specific information.

Modules:
    argparse -- For parsing command-line arguments.
    os -- For interacting with the operating system.
    sys -- For system-specific parameters and functions.
    imessage_reader -- Custom module for fetching and processing iMessage data.

Constants:
    MACOS_DB_PATH (str): Default path to the chat.db file on macOS.

Functions:
    get_parser() -- Creates and returns an argument parser for the CLI.
    check_database_path(args) -- Validates the database path and invokes the evaluation function.
    evaluate(path: str, output: str, recipients: bool, version: bool) -- Processes the database according to the provided options.
    main() -- Entry point for the CLI.
"""

import argparse
import os
import sys

from os.path import expanduser

from imessage_reader import fetch_data
from imessage_reader import info


# Path to the chat.db file on macOS
# Note: This path is used if the user does not specify a path.
MACOS_DB_PATH = expanduser("~") + "/Library/Messages/chat.db"


def get_parser() -> argparse.ArgumentParser:
    """Create the argument parser

    :rtype: object
    :return: Configured ArgumentParser object.
    """
    parser = argparse.ArgumentParser(
        description="A tool to fetch messages from the chat.db file."
    )

    parser.add_argument(
        "-p",
        "--path",
        type=str,
        nargs="?",
        const=MACOS_DB_PATH,
        default=MACOS_DB_PATH,
        help="Path to the database file"
    )

    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        default="nothing",
        help="Specify the output: e => Excel, s => SQLite"
    )

    parser.add_argument(
        "-r",
        "--recipients",
        help="Show the recipients",
        action="store_true"
    )

    parser.add_argument(
        "-v",
        "--version",
        help="Show the current version.",
        action="store_true"
    )

    return parser


def check_database_path(args):
    """ Parse arguments from sys.argv and invoke the evaluate method.

    :param args: the user's input
    """
    if args.path == MACOS_DB_PATH:
        evaluate(MACOS_DB_PATH, args.output, args.recipients, args.version)
    elif os.path.isdir(args.path):
        db_path = args.path + "/chat.db"
        evaluate(db_path, args.output, args.recipients, args.version)
    else:
        sys.exit("Path doesn't exist! Exit program.")


def evaluate(path: str, output: str, recipients: bool, version: bool):
    """
    Processes the database based on user options.
    
    :param path: Path to the chat.db file.
    :param output: Output format.
    :param recipients: Flag to show recipients.
    :param version: Flag to show version.
    """
    data = fetch_data.FetchData(path)

    if version:
        info.app_info()
        sys.exit()

    if recipients:
        data.show_user_txt("recipients")
        sys.exit()

    if output == "e" or output == "excel":
        data.show_user_txt("excel")
    elif output == "s" or output == "sqlite" or output == "sqlite3":
        data.show_user_txt("sqlite")
    else:
        data.show_user_txt("nothing")


def main():
    """Entrypoint to the command-line interface (CLI).
    """
    parser = get_parser()
    args = parser.parse_args()
    check_database_path(args)

if __name__ == "__main__":
    main()