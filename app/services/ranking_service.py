from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import User, Prediction


def get_user_total_points(db: Session, user_id: int) -> int:
    """Obtiene el total de puntos de un usuario"""
    result = (
        db.query(func.sum(Prediction.points_earned))
        .filter(Prediction.user_id == user_id)
        .scalar()
    )
    return result or 0


def get_global_ranking(db: Session, limit: int = 100, offset: int = 0):
    """Obtiene el ranking global de usuarios ordenado por puntos totales"""
    query = (
        db.query(
            User.id,
            User.username,
            func.sum(Prediction.points_earned).label("total_points"),
            func.count(Prediction.id).label("total_predictions"),
        )
        .outerjoin(Prediction, User.id == Prediction.user_id)
        .group_by(User.id, User.username)
        .order_by(func.sum(Prediction.points_earned).desc(), User.username)
        .offset(offset)
        .limit(limit)
    )
    
    results = query.all()
    
    ranking = []
    for idx, (user_id, username, total_points, total_predictions) in enumerate(results, start=offset + 1):
        ranking.append({
            "position": idx,
            "user_id": user_id,
            "username": username,
            "total_points": total_points or 0,
            "total_predictions": total_predictions or 0,
        })
    
    return ranking


def get_user_ranking_position(db: Session, user_id: int) -> dict | None:
    """Obtiene la posición y estadísticas de un usuario específico en el ranking"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    
    # Obtener el total de puntos del usuario
    total_points = get_user_total_points(db, user_id)
    
    # Contar predicciones totales del usuario
    total_predictions = (
        db.query(func.count(Prediction.id))
        .filter(Prediction.user_id == user_id)
        .scalar() or 0
    )
    
    # Obtener la posición (contar cuántos usuarios tienen más puntos)
    # Primero obtener todos los usuarios con sus puntos totales
    user_points = (
        db.query(
            User.id,
            func.sum(Prediction.points_earned).label("total")
        )
        .outerjoin(Prediction, User.id == Prediction.user_id)
        .group_by(User.id)
        .all()
    )
    
    # Contar cuántos usuarios tienen más puntos que el actual
    position = sum(1 for uid, pts in user_points if (pts or 0) > total_points) + 1
    
    return {
        "position": position,
        "user_id": user_id,
        "username": user.username,
        "total_points": total_points,
        "total_predictions": total_predictions,
    }


def get_match_leaderboard(db: Session, match_id: int):
    """Obtiene el leaderboard de predicciones para un partido específico"""
    results = (
        db.query(
            User.id,
            User.username,
            Prediction.points_earned,
            Prediction.pred_a,
            Prediction.pred_b,
        )
        .join(Prediction, User.id == Prediction.user_id)
        .filter(Prediction.match_id == match_id)
        .order_by(Prediction.points_earned.desc(), Prediction.prediction_date)
        .all()
    )
    
    leaderboard = []
    for idx, (user_id, username, points, pred_a, pred_b) in enumerate(results, start=1):
        leaderboard.append({
            "position": idx,
            "user_id": user_id,
            "username": username,
            "points": points or 0,
            "prediction": f"{pred_a}-{pred_b}",
        })
    
    return leaderboard
