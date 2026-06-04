from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Match
from app.schemas.match import MatchOut
from app.limiter import limiter

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("", response_model=list[MatchOut])
@limiter.limit("30/minute")
async def list_matches(request: Request, db: Session = Depends(get_db), status_filter: str | None = Query(default=None, alias="status")):
    query = db.query(Match)
    if status_filter:
        query = query.filter(Match.status == status_filter)
    return query.order_by(Match.match_date.asc()).all()


@router.get("/search/", response_model=list[MatchOut])
@limiter.limit("20/minute")
async def search_matches(
    request: Request,
    db: Session = Depends(get_db),
    q: str | None = Query(default=None, description="Busca por id o por nombre de equipo"),
    team_a: str | None = Query(default=None),
    team_b: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
):
    query = db.query(Match)
    filters = []

    if status_filter:
        filters.append(Match.status == status_filter)

    if team_a:
        filters.append(Match.team_a.ilike(f"%{team_a.strip()}%"))

    if team_b:
        filters.append(Match.team_b.ilike(f"%{team_b.strip()}%"))

    if q:
        q_clean = q.strip()
        search_conditions = [
            Match.team_a.ilike(f"%{q_clean}%"),
            Match.team_b.ilike(f"%{q_clean}%"),
        ]
        if q_clean.isdigit():
            search_conditions.append(Match.id == int(q_clean))
        filters.append(or_(*search_conditions))

    if not filters:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes enviar al menos un filtro para buscar partidos",
        )

    return query.filter(*filters).order_by(Match.match_date.asc()).all()


@router.get("/{match_id:int}", response_model=MatchOut)
@limiter.limit("20/minute")
async def get_match(request: Request, match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return match