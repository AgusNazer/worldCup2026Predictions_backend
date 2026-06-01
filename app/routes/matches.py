from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Match
from app.schemas.match import MatchOut
from app.main import limiter

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("", response_model=list[MatchOut])
@limiter.limit("30/minute")
async def list_matches(request: Request, db: Session = Depends(get_db), status_filter: str | None = Query(default=None, alias="status")):
    query = db.query(Match)
    if status_filter:
        query = query.filter(Match.status == status_filter)
    return query.order_by(Match.match_date.asc()).all()


@router.get("/{match_id}", response_model=MatchOut)
@limiter.limit("20/minute")
async def get_match(request: Request, match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return match
