from urllib.parse import ParseResult, urlparse


def is_url(path: str, schemes: list[str] = ["http", "https", "ftp"]) -> bool:
    parse_result: ParseResult = urlparse(path)
    
    return parse_result.scheme in schemes
