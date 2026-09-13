"""remove revoked from refresh tokens

Revision ID: 8b4d6e2f1a90
Revises: 7f3a2c1d9e40

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8b4d6e2f1a90"
down_revision: Union[str, Sequence[str], None] = "7f3a2c1d9e40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("refresh_tokens", "revoked")


def downgrade() -> None:
    op.add_column("refresh_tokens", sa.Column("revoked", sa.Boolean(), nullable=False, server_default=sa.false()))
