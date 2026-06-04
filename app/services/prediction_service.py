from uuid import UUID
from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session

from app.models import Match, Prediction


def get_match_result_label(score_a: int, score_b: int) -> str:
    if score_a > score_b:
        return "A"
    if score_b > score_a:
        return "B"
    return "DRAW"


def calculate_points(pred_a: int, pred_b: int, score_a: int, score_b: int) -> int:
    predicted = get_match_result_label(pred_a, pred_b)
    actual = get_match_result_label(score_a, score_b)

    points = 0
    if predicted == actual:
        points += 3
    if pred_a == score_a and pred_b == score_b:
        points += 2
    return points


def create_prediction(
    db: Session,
    *,
    match_id: int,
    pred_a: int,
    pred_b: int,
    user_id: int | None = None,
    anonymous_id: UUID | None = None,
) -> Prediction:
    if (user_id is None and anonymous_id is None) or (user_id is not None and anonymous_id is not None):
        raise ValueError("Prediction owner must be either user_id or anonymous_id")

    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise ValueError("Match not found")

    if getattr(match.status, "value", match.status) not in {"scheduled", "ongoing"}:
        raise ValueError("Predictions are only allowed before the match is finished")

    if user_id is not None:
        existing = (
            db.query(Prediction)
            .filter(Prediction.match_id == match_id, Prediction.user_id == user_id)
            .first()
        )
    else:
        existing = (
            db.query(Prediction)
            .filter(Prediction.match_id == match_id, Prediction.anonymous_id == anonymous_id)
            .first()
        )

    if existing:
        raise ValueError("Prediction already exists")

    prediction = Prediction(
        match_id=match_id,
        pred_a=pred_a,
        pred_b=pred_b,
        user_id=user_id,
        anonymous_id=anonymous_id,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


def settle_match_points(db: Session, match_id: int) -> int:
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise ValueError("Match not found")
    if match.score_a is None or match.score_b is None:
        raise ValueError("Match score not set")

    predictions = db.query(Prediction).filter(Prediction.match_id == match_id).all()
    total = 0
    for prediction in predictions:
        prediction.points_earned = calculate_points(
            prediction.pred_a,
            prediction.pred_b,
            match.score_a,
            match.score_b,
        )
        total += prediction.points_earned

    match.status = "finished"
    match.result_final = get_match_result_label(match.score_a, match.score_b)
    db.commit()
    return total


def _resolve_prediction_owner(
    prediction: Prediction,
    *,
    user_id: int | None,
    anonymous_id: UUID | None,
) -> bool:
    if user_id is not None:
        return prediction.user_id == user_id
    if anonymous_id is not None:
        return prediction.anonymous_id == anonymous_id
    return False


def update_prediction(
    db: Session,
    *,
    prediction_id: int,
    pred_a: int,
    pred_b: int,
    user_id: int | None = None,
    anonymous_id: UUID | None = None,
) -> Prediction:
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise ValueError("Prediction not found")

    if not _resolve_prediction_owner(prediction, user_id=user_id, anonymous_id=anonymous_id):
        raise PermissionError("No tienes permiso para modificar esta predicción")

    match = db.query(Match).filter(Match.id == prediction.match_id).first()
    if not match:
        raise ValueError("Match not found")

    now_utc = datetime.now(timezone.utc)
    editable_until = match.match_date - timedelta(days=1)
    if now_utc >= editable_until:
        raise ValueError("Solo puedes modificar una predicción hasta 24 horas antes del partido")

    prediction.pred_a = pred_a
    prediction.pred_b = pred_b
    prediction.points_earned = 0

    db.commit()
    db.refresh(prediction)
    return prediction


def delete_prediction(
    db: Session,
    *,
    prediction_id: int,
    user_id: int | None = None,
    anonymous_id: UUID | None = None,
) -> None:
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise ValueError("Prediction not found")

    if not _resolve_prediction_owner(prediction, user_id=user_id, anonymous_id=anonymous_id):
        raise PermissionError("No tienes permiso para eliminar esta predicción")

    db.delete(prediction)
    db.commit()
