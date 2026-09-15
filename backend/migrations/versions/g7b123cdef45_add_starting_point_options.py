"""update starting point options

Revision ID: g7b123cdef45
Revises: f6a012bcde34

"""
from typing import Sequence, Union

from alembic import op


revision: str = "g7b123cdef45"
down_revision: Union[str, Sequence[str], None] = "f6a012bcde34"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE activitylevel ADD VALUE IF NOT EXISTS 'ACTIVE'")
    op.alter_column("starting_points", "average_sleep_hours", nullable=True)
    op.create_index("ix_starting_points_user_id", "starting_points", ["user_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_starting_points_user_id", table_name="starting_points")
    op.alter_column("starting_points", "average_sleep_hours", nullable=False)
