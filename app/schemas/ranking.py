from pydantic import BaseModel


class RankingEntry(BaseModel):
    position: int
    user_id: int
    username: str
    total_points: int
    total_predictions: int

    class Config:
        from_attributes = True


class UserRankingPosition(BaseModel):
    position: int
    user_id: int
    username: str
    total_points: int
    total_predictions: int

    class Config:
        from_attributes = True


class RankingResponse(BaseModel):
    data: list[RankingEntry]
    total: int
    limit: int
    offset: int


class MatchLeaderboardEntry(BaseModel):
    position: int
    user_id: int
    username: str
    points: int
    prediction: str

    class Config:
        from_attributes = True


class MatchLeaderboardResponse(BaseModel):
    match_id: int
    data: list[MatchLeaderboardEntry]
