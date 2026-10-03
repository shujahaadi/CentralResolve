from typing import Literal

from pydantic import BaseModel


class ProjectFact(BaseModel):
    type: Literal[
        "task_assignment",
        "deadline",
        "status",
        "decision",
        "unresolved",
    ]

    platform: Literal["whatsapp", "discord"]
    person: str
    task: str
    value: str
    source_message: str


class ProjectFacts(BaseModel):
    facts: list[ProjectFact]