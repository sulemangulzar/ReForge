"""create goals table

Revision ID: d4e8f9012abc
Revises: c3d7e8f901ab

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d4e8f9012abc"
down_revision: Union[str, Sequence[str], None] = "c3d7e8f901ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "goals",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column(
            "goal_type",
            sa.Enum(
                "LOSE_FAT",
                "GAIN_MUSCLE",
                "RECOMPOSITION",
                "MAINTAIN",
                "GAIN_STRENGTH",
                name="goaltype",
            ),
            nullable=False,
        ),
        sa.Column("target_weight_kg", sa.Float(), nullable=False),
        sa.Column("target_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_goals_user_id", "goals", ["user_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_goals_user_id", table_name="goals")
    op.drop_table("goals")
