"""
Usage: python pymail
"""

from io import TextIOWrapper
from json import dump, load
from pathlib import Path
from typing import Any

# Pymail
from generate_timeline import generate_timeline
from get_messages import get_messages
from send_message import send_message
from sort_recursively import sort_recursively

ROOT_DIRECTORY: Path = Path(__file__).parent
DATA_DIRECTORY: Path = ROOT_DIRECTORY.joinpath("data")
CONFIG_FILE: Path = DATA_DIRECTORY.joinpath("config.json")
FONT_FILE: Path = DATA_DIRECTORY.joinpath("DejaVuSans.ttf")
TIMELINE_SCRIPT_FILE: str = "https://cdnjs.cloudflare.com/ajax/libs/vis-timeline/7.7.3/vis-timeline-graph2d.min.js"
#TIMELINE_SCRIPT_FILE: str = f"file:///{DATA_DIRECTORY.joinpath('vis-timeline-graph2d.min.js')}"
TIMELINE_STYLE_FILE: str = "https://cdnjs.cloudflare.com/ajax/libs/vis-timeline/7.7.3/vis-timeline-graph2d.css"
#TIMELINE_STYLE_FILE: str = f"file:///{DATA_DIRECTORY.joinpath('vis-timeline-graph2d.css')}"
TIMELINE_TEMPLATE_FILE: Path = DATA_DIRECTORY.joinpath("timeline_template.html")
OUTPUT_DIRECTORY: Path = DATA_DIRECTORY.joinpath("email")
TIMELINE_FILE: Path = OUTPUT_DIRECTORY.joinpath("timeline.html")
ENCODING: str = "utf-8"
INDENT: int = 2
DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
DATETIME_FILENAME_FORMAT: str = "%Y-%m-%d_%Hh%Mm%Ss"
SHOULD_OUTPUT_PDF: bool = True
MAX_COUNT: int = None
VERBOSE: bool = True
DELETE: bool = True


def main(
    config_file: Path = CONFIG_FILE,
    output_directory: Path = OUTPUT_DIRECTORY,
    encoding: str = ENCODING,
    indent: int = INDENT,
    font_file: Path = FONT_FILE,
    should_output_pdf: bool = SHOULD_OUTPUT_PDF,
    max_count: int = MAX_COUNT,
    verbose: bool = VERBOSE,
    timeline_script_file: str = TIMELINE_SCRIPT_FILE,
    timeline_style_file: str = TIMELINE_STYLE_FILE,
    timeline_template_file: str = TIMELINE_TEMPLATE_FILE,
    timeline_file: str = TIMELINE_FILE,
    *,
    delete: bool = DELETE
) -> None:
    """
    configuration: dict = load(open(config_file, encoding=encoding))
    send_message(
        configuration["host"],
        configuration["port"],
        configuration["user"],
        configuration["password.vk"],
        configuration["tos"],
        configuration["subject"],
        configuration["reply_to"],
        configuration["body"],
        configuration["verbose"]
    )
    exit()
    """

    if verbose:
        print(f"Loading configuration...")

    stream: TextIOWrapper = open(config_file, "r+", encoding=encoding)
    config: dict = load(stream)

    if verbose:
        print(f"Sorting sublabels...")

    config["sublabels"] = sort_recursively(config["sublabels"])

    if verbose:
        print(f"Saving configuration...")

    stream.seek(0)
    dump(config, stream, ensure_ascii=encoding != "utf-8", indent=indent)
    stream.truncate()
    stream.close()

    messages: list[dict[str, Any]] = get_messages(
        config["imap_server"],
        config["imap_port"],    
        config["username"],
        config["password"],
        config["mailbox"],
        config["sublabels"],
        output_directory,
        font_file=font_file,
        should_output_pdf=should_output_pdf,
        max_count=max_count,
        verbose=verbose,
        delete=delete
    )

    if verbose:
        print(f"Generating timeline...")

    generate_timeline(messages, timeline_script_file, timeline_style_file, timeline_template_file, timeline_file)

    if verbose:
        print(f"** DONE **")





if __name__ == "__main__":
    main()
