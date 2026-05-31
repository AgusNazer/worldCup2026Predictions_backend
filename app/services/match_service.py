from sqlalchemy.orm import Session

from app.models import Match, MatchStatus
from app.services.prediction_service import settle_match_points


def finalize_match(db: Session, match_id: int, score_a: int, score_b: int) -> int:
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise ValueError("Match not found")

    match.score_a = score_a
    match.score_b = score_b
    match.status = MatchStatus.finished
    total_points = settle_match_points(db, match_id)
    return total_points
