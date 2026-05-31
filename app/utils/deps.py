from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.services.auth_service import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)


def _resolve_user(credentials: HTTPAuthorizationCredentials | None, db: Session) -> User | None:
    if not credentials:
        return None

    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return None

    return db.query(User).filter(User.email == payload["sub"]).first()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    user = _resolve_user(credentials, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return user


def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User | None:
    return _resolve_user(credentials, db)
