from pathlib import Path
from typing import Any

# Pymail
from parse_date_time import parse_date_time


def get_path(dictionary: dict, data: str, date: Any):
    key: str
    values: list[str]
    value: str
    directory: str = ""

    for key, values in dictionary.items():
        for value in values:
            if value in data:
                directory = key

                break

    return Path(__file__).parent.joinpath(f"data/email/{directory}/{parse_date_time(date)}.pdf")
