from typing import Literal
from pydantic import BaseModel


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
    evidence: list[str]


class Conflicts(BaseModel):
    conflicts: list[Conflict]