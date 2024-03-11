from chardet import detect
from email.message import Message


def get_body(message: Message, encodings: list[str] = ["latin-1", "utf-8"]) -> str:
    part: Message
    content_type: str
    content_disposition: str
    payload_bytes: bytes
    detected_encoding: str

    for part in message.walk():
        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition"))

        # Check if the part is the body of the email
        if content_type.startswith("text/") and "attachment" not in content_disposition:
            payload_bytes = part.get_payload(decode=True)
            detected_encoding = detect(payload_bytes)["encoding"]

            # Attempt to decode using detected encoding
            if detected_encoding:
                try:
                    return payload_bytes.decode(detected_encoding)
                
                except UnicodeDecodeError:
                    pass

            # Attempt to decode using specified encodings
            for encoding in encodings:
                try:
                    return payload_bytes.decode(encoding)
                
                except UnicodeDecodeError:
                    pass

            # Return as is if decoding fails
            return payload_bytes.decode(errors="ignore")
