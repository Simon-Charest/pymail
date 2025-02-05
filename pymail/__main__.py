"""
Usage: python pymail [-s] [-d] [-m #] [-g] [-e] [-r] [-n] [-v]
Examples:
python pymail -s -d -m 10 -g -e -r -v
python pymail -s -e -r -v
python pymail -n -v
"""

from io import TextIOWrapper
from json import dump, load
from pathlib import Path
from typing import Any

# Pymail
from argparse import Namespace
from delete import delete
from generate_graph import generate_graph
from generate_report import generate_report
from get_messages import get_messages
from get_path import get_path
from parse_arguments import parse_arguments
from send_message import send_message
from sort_recursively import sort_recursively

current_directory: Path = Path(__file__).parent
config_file: Path = current_directory.joinpath("config.json")
encoding: Path = "utf-8"


def main() -> None:
    arguments: Namespace = parse_arguments()

    if arguments.verbose: print(f"Loading configuration...")
    stream: TextIOWrapper = open(config_file, "r+", encoding=encoding)
    config: dict = load(stream)

    if arguments.save_configuration:
        if arguments.verbose: print(f"Sorting sublabels...")
        config["sublabels"] = sort_recursively(config["sublabels"])

        if arguments.verbose: print(f"Saving configuration...")
        stream.seek(0)
        dump(config, stream, ensure_ascii=encoding != "utf-8", indent=config["indent"])
        stream.truncate()
    
    if arguments.verbose: print(f"Closing configuration...")
    stream.close()

    if arguments.delete_messages:
        if arguments.verbose: print(f"Deleting previous result set...")
        delete(current_directory.joinpath(config["output"]))

    if arguments.get_messages:
        if arguments.verbose: print("Getting messages from server...")
        messages: list[dict[str, Any]] = get_messages(
            config["imap_server"],
            config["imap_port"],    
            config["username"],
            config["password"],
            config["mailbox"],
            config["sublabels"],
            current_directory.joinpath(config["output"]),
            config["charset"],
            config["criteria"],
            config["message_parts"],
            encoding,
            config["datetimes"]["filenameFormat"],
            config["datetimes"]["format"],
            current_directory.joinpath(config["font"]),
            config["pdf"],
            max_count=arguments.max_count,
            verbose=arguments.verbose
        )

    if arguments.send_message:
        if arguments.verbose: print("Sending message...")
        send_message(
            config["imap_server"],
            config["smtp_port"],
            config["username"],
            config["password"],
            config["tos"],
            config["subject"],
            config["reply_to"],
            config["body"],
            arguments.verbose
        )

    if arguments.verbose: print(f"Generating graph...")
    generate_graph(
        messages,
        get_path(config["timeline"]["scripts"], current_directory),
        get_path(config["timeline"]["styles"], current_directory),
        current_directory.joinpath(config["timeline"]["template"]),
        current_directory.joinpath(config["timeline"]["output"]),
        encoding
    )

    if arguments.verbose: print(f"Generating report...")
    generate_report(messages)
    
    if arguments.verbose: print(f"** DONE **")


if __name__ == "__main__":
    main()
