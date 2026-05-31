"""Make prediction user_id nullable for anonymous predictions

Revision ID: 003_pred_user_nullable
Revises: 002_anonymous_predictions
Create Date: 2026-05-29 13:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "003_pred_user_nullable"
down_revision: Union[str, None] = "002_anonymous_predictions"
branch_labels: Union[Sequence[str], None] = None
tag_names: Union[Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "predictions",
        "user_id",
        existing_type=sa.Integer(),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "predictions",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )
