"""add activity and training to profiles

Revision ID: e5f9012abcde
Revises: d4e8f9012abc

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e5f9012abcde"
down_revision: Union[str, Sequence[str], None] = "d4e8f9012abc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    activity_level = sa.Enum(
        "SEDENTARY", "LIGHT", "MODERATE", "VERY_ACTIVE", name="activitylevel"
    )
    training_frequency = sa.Enum(
        "ZERO_DAYS", "ONE_TWO_DAYS", "THREE_FOUR_DAYS", "FIVE_PLUS_DAYS",
        name="trainingfrequency",
    )
    activity_level.create(op.get_bind(), checkfirst=True)
    training_frequency.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "profiles",
        sa.Column("activity_level", activity_level, nullable=False, server_default="SEDENTARY"),
    )
    op.add_column(
        "profiles",
        sa.Column("training_frequency", training_frequency, nullable=False, server_default="ZERO_DAYS"),
    )
    op.alter_column("profiles", "activity_level", server_default=None)
    op.alter_column("profiles", "training_frequency", server_default=None)


def downgrade() -> None:
    op.drop_column("profiles", "training_frequency")
    op.drop_column("profiles", "activity_level")
    sa.Enum(name="trainingfrequency").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="activitylevel").drop(op.get_bind(), checkfirst=True)
