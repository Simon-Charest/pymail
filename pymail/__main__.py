from json import load
from pathlib import Path

# Pymail
from get_messages import get_messages


def main() -> None:
    config: dict = load(open(Path(__file__).parent.joinpath("data/config.json")))
    get_messages(
        config["imap_server"],
        config["imap_port"],
        config["username"],
        config["password"],
        "Succession",
        verbose = True,
        max_count = None
    )

if __name__ == "__main__":
    main()
