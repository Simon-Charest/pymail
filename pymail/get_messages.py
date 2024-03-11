from email import message_from_bytes
from email.header import decode_header
from email.message import Message
from imaplib import IMAP4_SSL
from json import load
from pathlib import Path
from typing import Any

# Pymail
from get_body import get_body
from get_path import get_path
from output_pdf import output_pdf


def get_messages(
    host: str,
    port: int,
    user: str,
    password: str,
    mailbox: str,
    criteria: str = "ALL",
    message_parts: str = "(RFC822)",
    verbose: bool = False,
    max_count: int = 1
) -> None:
    mail: IMAP4_SSL = IMAP4_SSL(host, port)  # Connect
    mail.login(user, password)  # Login
    mail.select(mailbox)  # Select mailbox
    command_results: list[Any]
    _, command_results = mail.search(None, criteria)  # Search for emails
    message_sets: Any = command_results[0].split()  # Email IDs

    if verbose:
        print(f"{len(message_sets)} email message found.")
    
    dictionary: dict = load(open(Path(__file__).parent.joinpath("data/email.json")))
    path: Path
    count: int = 0
    
    # Iterate over the list of email IDs
    for message_set in message_sets:
        _, command_results = mail.fetch(message_set, message_parts)  # Fetch email by ID

        # Parse the email message
        string: bytes = command_results[0][1]  # Raw email message
        message: Message = message_from_bytes(string)

        # Extract email information
        message_id: Any = message["Message-ID"]
        date: Any = message["Date"]
        from_: Any = decode_header(message["From"])[0][0]
        to: Any = decode_header(message["To"])[0][0]
        cc: Any = decode_header(message["CC"])[0][0] if "CC" in message else None
        bcc: Any = decode_header(message["BCC"])[0][0] if "BCC" in message else None
        subject: Any = decode_header(str(message["Subject"]))[0][0]
        body: str = get_body(message)

        if isinstance(from_, bytes):
            from_ = from_.decode("utf-8", errors="replace")

        if isinstance(subject, bytes):
            subject = subject.decode("utf-8", errors="replace")

        # Prepare text content
        text: str = f"""\
Message-ID: {message_id}
Date: {date}
From: {from_}
To: {to}
CC: {cc}
BCC: {bcc}
Subject: {subject}

Body: {body}
"""
        
        # Get file path
        path = get_path(dictionary, "; ".join([str(item) for item in [message_id, from_, to, subject]]), date)

        # Create directory structure
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        
        # Print to PDF
        output_pdf(text, path)
        count += 1

        if max_count and count >= max_count:
            break

    mail.logout()  # Logout
