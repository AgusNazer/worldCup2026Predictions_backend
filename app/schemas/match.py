from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MatchOut(BaseModel):
    id: int
    team_a: str
    team_b: str
    match_date: datetime
    score_a: Optional[int] = None
    score_b: Optional[int] = None
    status: str
    result_final: Optional[str] = None

    class Config:
        from_attributes = True

