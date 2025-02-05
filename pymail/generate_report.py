from pathlib import Path
from pandas import DataFrame
from typing import Any


def generate_report(items: list[dict[str, Any]], excel_writer: Path) -> None:
    data_frame: DataFrame = DataFrame(items)
    data_frame.to_excel(excel_writer, index=False)
