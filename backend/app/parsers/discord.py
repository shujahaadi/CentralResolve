import json
from datetime import datetime

from app.schemas.message import Message


def parse_discord_chat(file_content: str) -> list[Message]:
    data = json.loads(file_content)

    messages = []

    for item in data:
        messages.append(
            Message(
                platform="discord",
                sender=item["author"],
                timestamp=datetime.fromisoformat(item["timestamp"]),
                message=item["content"],
            )
        )

    return messages