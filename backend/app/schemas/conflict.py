from typing import Literal
from pydantic import BaseModel


class ConflictEvidence(BaseModel):
    platform: Literal["whatsapp", "discord"]
    message: str


class Conflict(BaseModel):
    type: Literal[
        "ownership_conflict",
        "deadline_conflict",
        "status_conflict",
        "unresolved_decision",
    ]
    task: str
    description: str
    severity: Literal["low", "medium", "high"]
    evidence: list[ConflictEvidence]


class Conflicts(BaseModel):
    conflicts: list[Conflict]