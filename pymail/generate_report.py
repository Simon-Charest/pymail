from pandas import DataFrame
from typing import Any


def generate_report(items: list[dict[str, Any]]) -> None:
    data_frame: DataFrame = DataFrame(items)
    print(data_frame)
