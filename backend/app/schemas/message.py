from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    platform: str
    sender: str
    timestamp: datetime
    message: str