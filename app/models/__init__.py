from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from uuid import uuid4

from app.database import Base
from sqlalchemy.dialects.postgresql import UUID


class MatchStatus(str, enum.Enum):
    scheduled = "scheduled"
    ongoing = "ongoing"
    finished = "finished"
    postponed = "postponed"
    cancelled = "cancelled"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    predictions = relationship("Prediction", back_populates="user", cascade="all, delete-orphan")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    team_a = Column(String(255), nullable=False)
    team_b = Column(String(255), nullable=False)
    match_date = Column(DateTime(timezone=True), nullable=False, index=True)
    score_a = Column(Integer, CheckConstraint("score_a >= 0"), nullable=True)
    score_b = Column(Integer, CheckConstraint("score_b >= 0"), nullable=True)
    status = Column(Enum(MatchStatus, name="match_status"), nullable=False, default=MatchStatus.scheduled)
    result_final = Column(String(10), CheckConstraint("result_final IN ('A','B','DRAW')"), nullable=True)

    predictions = relationship("Prediction", back_populates="match", cascade="all, delete-orphan")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    anonymous_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    pred_a = Column(Integer, CheckConstraint("pred_a >= 0"), nullable=False)
    pred_b = Column(Integer, CheckConstraint("pred_b >= 0"), nullable=False)
    points_earned = Column(Integer, CheckConstraint("points_earned >= 0"), nullable=False, default=0)
    prediction_date = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="predictions")
    match = relationship("Match", back_populates="predictions")

    __table_args__ = (
        UniqueConstraint("user_id", "match_id", name="uq_predictions_user_match"),
        UniqueConstraint("match_id", "anonymous_id", name="uq_predictions_anonymous_match"),
        CheckConstraint("(user_id IS NOT NULL AND anonymous_id IS NULL) OR (user_id IS NULL AND anonymous_id IS NOT NULL)", name="ck_prediction_owner"),
    )
