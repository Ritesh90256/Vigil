"""store complete trace json

Revision ID: 00ac21aa0583
Revises: 90fc375f1508
Create Date: 2026-07-16 11:23:37.485458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00ac21aa0583'
down_revision: Union[str, Sequence[str], None] = '90fc375f1508'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("traces", sa.Column("trace_data", sa.JSON(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("traces", "trace_data")
