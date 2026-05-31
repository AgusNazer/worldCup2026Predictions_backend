"""Create initial schema with users, matches and predictions tables

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-05-29 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
# revision identifiers, used by Alembic.
revision: str = "001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[Sequence[str], None] = None
tag_names: Union[Sequence[str], None] = None


def upgrade() -> None:
    # Clean up any previous leftover enum type before recreating schema
    op.execute("DROP TYPE IF EXISTS match_status CASCADE")

    match_status = sa.Enum(
        "scheduled",
        "ongoing",
        "finished",
        "postponed",
        "cancelled",
        name="match_status",
    )

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=False)

    # Create matches table
    op.create_table(
        "matches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_a", sa.String(length=255), nullable=False),
        sa.Column("team_b", sa.String(length=255), nullable=False),
        sa.Column("match_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("score_a", sa.Integer(), nullable=True),
        sa.Column("score_b", sa.Integer(), nullable=True),
        sa.Column("status", match_status, nullable=False, server_default="scheduled"),
        sa.Column("result_final", sa.String(length=10), nullable=True),
        sa.CheckConstraint("score_a >= 0"),
        sa.CheckConstraint("score_b >= 0"),
        sa.CheckConstraint("result_final IN ('A','B','DRAW')"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_matches_match_date"), "matches", ["match_date"], unique=False)

    # Create predictions table
    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("match_id", sa.Integer(), nullable=False),
        sa.Column("pred_a", sa.Integer(), nullable=False),
        sa.Column("pred_b", sa.Integer(), nullable=False),
        sa.Column("points_earned", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("prediction_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("pred_a >= 0"),
        sa.CheckConstraint("pred_b >= 0"),
        sa.CheckConstraint("points_earned >= 0"),
        sa.ForeignKeyConstraint(["match_id"], ["matches.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "match_id", name="uq_predictions_user_match"),
    )
    op.create_index(op.f("ix_predictions_match_id"), "predictions", ["match_id"], unique=False)
    op.create_index(op.f("ix_predictions_prediction_date"), "predictions", ["prediction_date"], unique=False)
    op.create_index(op.f("ix_predictions_user_id"), "predictions", ["user_id"], unique=False)


def downgrade() -> None:
    # Drop predictions table
    op.drop_index(op.f("ix_predictions_user_id"), table_name="predictions")
    op.drop_index(op.f("ix_predictions_prediction_date"), table_name="predictions")
    op.drop_index(op.f("ix_predictions_match_id"), table_name="predictions")
    op.drop_table("predictions")

    # Drop matches table
    op.drop_index(op.f("ix_matches_match_date"), table_name="matches")
    op.drop_table("matches")

    # Drop users table
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_table("users")

    # Drop ENUM type
    op.execute("DROP TYPE IF EXISTS match_status")
