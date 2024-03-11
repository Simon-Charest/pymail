from time import strptime, struct_time


def parse_date_time(date_string: str) -> str:
    # Remove the timezone abbreviation if present
    date_string = date_string.split("(")[0].strip()

    # Define the formats to parse
    formats: list[str] = [
        "%a, %d %b %Y %H:%M:%S %z (%Z)",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%a, %d %b %Y %H:%M:%S %z"
    ]
    
    # Iterate over the formats and try to parse the date string
    format: str
    struct_time_: struct_time
    
    for format in formats:
        try:
            struct_time_ = strptime(date_string, format)

            return f"{str(struct_time_.tm_year).zfill(2)}-{str(struct_time_.tm_mon).zfill(2)}-{str(struct_time_.tm_mday).zfill(2)}_{str(struct_time_.tm_hour).zfill(2)}h{str(struct_time_.tm_min).zfill(2)}m{str(struct_time_.tm_sec).zfill(2)}s"
        
        except ValueError:
            pass

    # If no format matches, raise an exception
    raise ValueError(f"Could not parse date string: {date_string}")
