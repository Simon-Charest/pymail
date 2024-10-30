from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP


def send_message(host: str, port: int, user: str, password: str, tos: list[str], subject: str, reply_to: str, body: str, verbose: bool = False):
    """Connect to the SMTP server and send the email."""

    try:
        if verbose: print("Connecting to SMTP server....")
        server: SMTP = SMTP(host, port)

        if verbose: print("Putting connection into TLS mode....")
        server.starttls()

        if verbose: print(f"Logging with user {user}...")
        server.login(user, password)

        to: str

        for to in tos:
            if verbose: print(f"Creating message for {to}...")
            msg: MIMEMultipart = MIMEMultipart()
            msg["From"] = user
            msg["To"] = to
            msg["Subject"] = subject
            msg["Reply-To"] = reply_to
            msg.attach(MIMEText(body, "plain"))

            if verbose: print("Sending message...")
            server.send_message(msg)

            if verbose: print("Message sent.")

        if verbose: print("Disconnecting...")
        server.close()

    except Exception as exception:
        if verbose: print(f"Failed to send message: {exception}")
