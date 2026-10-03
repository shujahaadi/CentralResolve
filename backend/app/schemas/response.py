from pydantic import BaseModel

from app.schemas.analysis import ProjectFact
from app.schemas.conflict import Conflict


class AnalysisResponse(BaseModel):
    whatsapp_messages: int
    discord_messages: int
    total_messages: int
    facts: list[ProjectFact]
    conflicts: list[Conflict]