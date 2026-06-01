import os
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.limiter import limiter
from app.models import Prediction, User
from app.schemas.prediction import PredictionCreate, PredictionOut
from app.services.prediction_service import create_prediction
from app.utils.deps import get_current_user, get_optional_current_user

router = APIRouter(prefix="/predictions", tags=["predictions"])

COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "lax")
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"


def _get_or_set_anon_id(request: Request, response: Response) -> UUID:
    existing = request.cookies.get("wc_anon_id")
    if existing:
        return UUID(existing)
    anon_id = uuid4()
    response.set_cookie(
        key="wc_anon_id",
        value=str(anon_id),
        httponly=True,
        samesite=COOKIE_SAMESITE,
        secure=COOKIE_SECURE,
        max_age=60 * 60 * 24 * 365,
    )
    return anon_id


@router.post("", response_model=PredictionOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_public_prediction(
    request: Request,
    payload: PredictionCreate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    try:
        return create_prediction(
            db,
            match_id=payload.match_id,
            pred_a=payload.pred_a,
            pred_b=payload.pred_b,
            user_id=current_user.id if current_user else None,
            anonymous_id=None if current_user else _get_or_set_anon_id(request, response),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("", response_model=list[PredictionOut])
@limiter.limit("20/minute")
async def list_public_predictions(request: Request, match_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Prediction)
    if match_id is not None:
        query = query.filter(Prediction.match_id == match_id)
    return query.order_by(Prediction.prediction_date.desc()).all()


@router.get("/mine", response_model=list[PredictionOut])
@limiter.limit("20/minute")
async def my_or_anonymous_predictions(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    query = db.query(Prediction)
    if current_user:
        anon_cookie = request.cookies.get("wc_anon_id")
        if anon_cookie:
            query = query.filter(
                or_(
                    Prediction.user_id == current_user.id,
                    Prediction.anonymous_id == UUID(anon_cookie),
                )
            )
        else:
            query = query.filter(Prediction.user_id == current_user.id)
    else:
        anon_cookie = request.cookies.get("wc_anon_id")
        if not anon_cookie:
            return []
        query = query.filter(Prediction.anonymous_id == UUID(anon_cookie))
    return query.order_by(Prediction.prediction_date.desc()).all()


@router.get("/me", response_model=list[PredictionOut])
@limiter.limit("20/minute")
async def my_predictions(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.prediction_date.desc())
        .all()
    )