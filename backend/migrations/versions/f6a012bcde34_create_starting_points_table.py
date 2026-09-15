"""create starting points table

Revision ID: f6a012bcde34
Revises: e5f9012abcde

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "f6a012bcde34"
down_revision: Union[str, Sequence[str], None] = "e5f9012abcde"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "starting_points",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("weight_kg", sa.Float(), nullable=False),
        sa.Column(
            "activity_level",
            postgresql.ENUM(name="activitylevel", create_type=False),
            nullable=False,
        ),
        sa.Column("training_days_per_week", sa.Integer(), nullable=False),
        sa.Column("average_sleep_hours", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )