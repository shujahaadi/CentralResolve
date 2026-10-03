import re
from datetime import datetime

from app.schemas.message import Message


MESSAGE_PATTERN = re.compile(
    r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s+"
    r"(\d{1,2}:\d{2}(?:\s?[apAP][mM])?)\s+-\s+"
    r"([^:]+):\s+(.*)$"
)


def parse_whatsapp_chat(file_content: str) -> list[Message]:
    messages = []

    for line in file_content.splitlines():
        match = MESSAGE_PATTERN.match(line)

        if not match:
            continue

        date, time, sender, message = match.groups()

        timestamp = parse_timestamp(date, time)

        messages.append(
            Message(
                platform="whatsapp",
                sender=sender.strip(),
                timestamp=timestamp,
                message=message.strip(),
            )
        )

    return messages


def parse_timestamp(date: str, time: str) -> datetime:
    formats = [
        "%d/%m/%Y, %I:%M %p",
        "%d/%m/%y, %I:%M %p",
        "%d/%m/%Y, %H:%M",
        "%d/%m/%y, %H:%M",
    ]

    value = f"{date}, {time}"

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    raise ValueError(f"Unsupported timestamp format: {value}")