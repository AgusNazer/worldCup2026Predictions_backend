from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PredictionCreate(BaseModel):
    match_id: int
    pred_a: int = Field(ge=0)
    pred_b: int = Field(ge=0)


class PredictionOut(BaseModel):
    id: int
    user_id: Optional[int] = None
    anonymous_id: Optional[UUID] = None
    match_id: int
    pred_a: int
    pred_b: int
    points_earned: int
    prediction_date: datetime

    class Config:
        from_attributes = True

