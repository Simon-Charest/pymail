from pandas import DataFrame
from pathlib import Path
from typing import Any


def generate_report(items: list[dict[str, Any]], excel_writer: Path) -> None:
    data_frame: DataFrame = DataFrame(items)
    columns: list[str] = [
        "id",
        "timeline",
        "messageId",
        "start",
        "from",
        "to",
        "cc",
        "bcc",
        "subject",
        "body"
    ]
    columns += [column for column in data_frame.columns if column.startswith("attachment_")]
    data_frame = data_frame[columns]
    data_frame = data_frame.rename(columns={"timeline": "sublabel", "start": "date"})
    data_frame.to_excel(excel_writer, index=False)
