from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas.ranking import (
    RankingResponse,
    RankingEntry,
    UserRankingPosition,
    MatchLeaderboardResponse,
)
from app.services.ranking_service import (
    get_global_ranking,
    get_user_ranking_position,
    get_match_leaderboard,
)
from app.utils.deps import get_optional_current_user

router = APIRouter(prefix="/rankings", tags=["rankings"])


@router.get("", response_model=RankingResponse)
def get_ranking(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Obtiene el ranking global de todos los usuarios"""
    ranking = get_global_ranking(db, limit=limit, offset=offset)
    
    # Obtener el total de usuarios
    total = db.query(User).count()
    
    return RankingResponse(
        data=[RankingEntry(**entry) for entry in ranking],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/users/{user_id}", response_model=UserRankingPosition)
def get_user_ranking(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Obtiene la posición y estadísticas de un usuario específico en el ranking"""
    position_data = get_user_ranking_position(db, user_id)
    
    if position_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    
    return UserRankingPosition(**position_data)


@router.get("/matches/{match_id}", response_model=MatchLeaderboardResponse)
def get_match_leaderboard_endpoint(
    match_id: int,
    db: Session = Depends(get_db),
):
    """Obtiene el leaderboard de predicciones para un partido específico"""
    leaderboard = get_match_leaderboard(db, match_id)
    
    if not leaderboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partido no encontrado o sin predicciones",
        )
    
    return MatchLeaderboardResponse(
        match_id=match_id,
        data=leaderboard,
    )


@router.get("/me", response_model=UserRankingPosition)
def get_my_ranking(
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    """Obtiene mi posición en el ranking (requiere estar autenticado)"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Debes estar autenticado para ver tu ranking",
        )
    
    position_data = get_user_ranking_position(db, current_user.id)
    
    if position_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    
    return UserRankingPosition(**position_data)
