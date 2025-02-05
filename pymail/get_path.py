from pathlib import Path
from requests import head
from requests.exceptions import RequestException

# Pymail
from is_url import is_url


def get_path(paths: list[str], prefix: Path = None) -> str:
    path: str

    for path in paths:
        if is_url(path):
            try:
                if head(path).status_code == 200:
                    return path
                
            except RequestException:
                pass

        if Path(path).is_file():
            return path
        
        if prefix:
            path = str(prefix.joinpath(path))

            if Path(path).is_file():
                return path

    return None
