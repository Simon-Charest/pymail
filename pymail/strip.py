from re import sub


def strip(string: str) -> str:
    string = "\n".join([line for line in string.split("\n") if "BQ_BEGIN" not in line and "BQ_END" not in line])
    string = sub(r"\[.*?\|\s*(.*?)\s*\]", r"\1", string)

    return string
