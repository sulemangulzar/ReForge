"""create profiles table

Revision ID: c3d7e8f901ab
Revises: a9e8f202aee9, 8b4d6e2f1a90

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c3d7e8f901ab"
down_revision: Union[str, Sequence[str], None] = ("a9e8f202aee9", "8b4d6e2f1a90")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("users", "name")
    op.create_table(
        "profiles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("gender", sa.Enum("MALE", "FEMALE", "OTHER", name="gender"), nullable=False),
        sa.Column("height_cm", sa.Float(), nullable=False),
        sa.Column("current_weight_kg", sa.Float(), nullable=False),
        sa.Column(
            "experience_level",
            sa.Enum("BEGINNER", "INTERMEDIATE", "ADVANCED", name="experiencelevel"),
            nullable=False,
        ),
        sa.Column(
            "preferred_units",
            sa.Enum("METRIC", "IMPERIAL", name="preferredunits"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_profiles_user_id", "profiles", ["user_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_profiles_user_id", table_name="profiles")
    op.drop_table("profiles")
    op.add_column("users", sa.Column("name", sa.String(), nullable=True))
