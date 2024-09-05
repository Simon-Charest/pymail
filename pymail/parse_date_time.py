from datetime import datetime
from time import strptime, struct_time


def parse_date_time(
    date_string: str,
    input_formats: list[str] = [
        "%a, %d %b %Y %H:%M:%S %z (%Z)",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%a, %d %b %Y %H:%M:%S %z"
    ]
) -> datetime:
    # Remove the timezone abbreviation if present
    date_string = date_string.split("(")[0].strip()

    # Iterate over the formats and try to parse the date string
    input_format: str
    
    for input_format in input_formats:
        try:
            time: struct_time = strptime(date_string, input_format)
            return datetime(*time[:6])

            return date_time
        
        except ValueError:
            pass

    # If no format matches, raise an exception
    raise ValueError(f"Could not parse date string: {date_string}")
