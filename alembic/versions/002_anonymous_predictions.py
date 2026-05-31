"""Add anonymous predictions support

Revision ID: 002_anonymous_predictions
Revises: 001_initial_schema
Create Date: 2026-05-29 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "002_anonymous_predictions"
down_revision: Union[str, None] = "001_initial_schema"
branch_labels: Union[Sequence[str], None] = None
tag_names: Union[Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("predictions", sa.Column("anonymous_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.create_index("ix_predictions_anonymous_id", "predictions", ["anonymous_id"], unique=False)
    op.create_check_constraint(
        "ck_prediction_owner",
        "predictions",
        "(user_id IS NOT NULL AND anonymous_id IS NULL) OR (user_id IS NULL AND anonymous_id IS NOT NULL)",
    )
    op.create_unique_constraint("uq_predictions_anonymous_match", "predictions", ["match_id", "anonymous_id"])


def downgrade() -> None:
    op.drop_constraint("uq_predictions_anonymous_match", "predictions", type_="unique")
    op.drop_constraint("ck_prediction_owner", "predictions", type_="check")
    op.drop_index("ix_predictions_anonymous_id", table_name="predictions")
    op.drop_column("predictions", "anonymous_id")
