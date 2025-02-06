from datetime import datetime
from email import message_from_bytes
from email.header import decode_header
from email.message import EmailMessage, Message
from email.policy import default
from imaplib import IMAP4_SSL
from io import TextIOWrapper
from pathlib import Path
from progress.bar import Bar
from typing import Any

# Pymail
from convert_to_color import convert_to_color
from get_body import get_body
from get_sublabel import get_sublabel
from output_pdf import output_pdf
from parse_date_time import parse_date_time
from strip import strip


def get_messages(
    host: str,
    port: int,
    user: str,
    password: str,
    mailbox: str,  # Also known as a label in Gmail
    sublabels: dict[str, list[str]],
    output_directory: Path,
    charset: str = None,
    criteria: str = "ALL",
    message_parts: str = "(RFC822)",
    encoding: str = "utf-8",
    datetime_filename_format: str = "%Y-%m-%d_%Hh%Mm%Ss",
    datetime_format: str = "%Y-%m-%d %H:%M:%S",
    font_file: Path = None,
    should_output_pdf: bool = True,
    max_count: int = None,
    verbose: bool = False
) -> list[dict[str, Any]]:
    if verbose: print(f"Connecting to {host}:{port} using IMAP4_SSL...")
    mail: IMAP4_SSL = IMAP4_SSL(host, port)

    if verbose: print(f"Logging as user {user}...")
    mail.login(user, password)

    if verbose: print(f"Selecting mailbox {mailbox}...")
    mail.select(mailbox)

    if verbose: print(f"Searching for emails...")
    data: list[bytes]
    _, data = mail.search(charset, criteria)

    if verbose: print(f"Splitting emails...")
    message_sets: list[bytes] = data[0].split()

    if verbose: print(f"Found {len(message_sets)} email messages.")
    
    # Iterate over the list of email IDs
    count: int
    message_set: str
    items: list[dict[str, Any]] = []

    if not max_count: max_count = len(message_sets)
    if verbose: print(f"Processing {max_count} messages...")
    bar: Bar = Bar("Processing...", max=max_count)
    
    for count, message_set in enumerate(message_sets, 1):
        _, data = mail.fetch(message_set, message_parts)  # Fetch email by ID

        # Parse email message
        string: bytes = data[0][1]  # Raw email message
        message: Message = message_from_bytes(string, policy=default)

        # Extract email information
        message_id: str = message["Message-ID"]
        date: str = message["Date"]
        from_: (str | bytes) = decode_header(message["From"])[0][0]
        to: (str | bytes) = decode_header(message["To"])[0][0]
        cc: str = decode_header(message["CC"])[0][0] if "CC" in message else None
        bcc: str = decode_header(message["BCC"])[0][0] if "BCC" in message else None
        subject: (str | bytes) = decode_header(str(message["Subject"]))[0][0]
        body: str = get_body(message)
        body = strip(body)

        # Process data
        if isinstance(from_, bytes): from_ = from_.decode(encoding, "replace")
        if isinstance(to, bytes): to = to.decode(encoding, "replace")
        if isinstance(subject, bytes): subject = subject.decode(encoding, "replace")
        subject = subject.replace('"', "'")
        
        # Get file path
        sublabel: str = get_sublabel(sublabels, [message_id, from_, to, subject])
        date_time: datetime = parse_date_time(date)
        stem: str = date_time.strftime(datetime_filename_format)
        file: str = f"{stem}.pdf"
        path: Path = output_directory.joinpath(sublabel).joinpath(file)

        # Creating attachments
        part: EmailMessage
        attachments: list[str] = []
        
        for part in message.iter_parts():
            if part.get_content_disposition() == "attachment":
                attachment_directory: Path = output_directory.joinpath(sublabel).joinpath(stem)
                attachment_directory.mkdir(parents=True, exist_ok=True)
                filename: str = part.get_filename()

                # Write attachement to file
                string: str = part.get_payload(decode=True)

                if string:
                    stream: TextIOWrapper = open(attachment_directory.joinpath(filename), "wb")                
                    stream.write(string)
                    stream.close()

                # Append attachement hyperlink to PDF
                attachments.append(f"./{stem}/{filename}")

        # Prepare text content
        text: str = f"""\
Message-ID: {message_id}
Date: {date}
From: {from_}
To: {to}
CC: {cc}
BCC: {bcc}
Subject: {subject}
Attachments:
{", ".join(attachment for attachment in attachments)}
Body: {body}
"""

        # Print to PDF
        if should_output_pdf:
            path.parent.mkdir(parents=True, exist_ok=True)
            output_pdf(text, path, fname=font_file)

        # Append data for timeline
        link: str = f"./{sublabel}/{file}"
        start: str = date_time.strftime(datetime_format)
        background_color: str = convert_to_color(sublabel)
        items.append({
            # For graph
            "id": count,
            "content": f"{sublabel}<br />{subject}<br />{start}",
            "link": link,
            "start": start, 
            "timeline": sublabel,
            "style": f"background-color: {background_color};",

            # For report
            "messageId": message_id,
            "from": from_,
            "to": to,
            "cc": cc,
            "bcc": bcc,
            "subject": subject,
            "body": f'=HYPERLINK("{link}", "{link}")'
        })

        for count, attachment in enumerate(attachments, start=1):
            items[len(items) - 1][f"attachment_{count}"] = f'=HYPERLINK("./{sublabel}/{attachment.strip("./")}", "./{sublabel}/{attachment.strip("./")}")'

        bar.next()

        if max_count and count >= max_count: break

    if verbose: print("\nLogging out...")
    mail.logout()

    return items
