"""add classifier columns

Revision ID: 90fc375f1508
Revises: 6e642af730a9
Create Date: 2026-07-12 13:25:38.030966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90fc375f1508'
down_revision: Union[str, Sequence[str], None] = '6e642af730a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("traces", sa.Column("failure_mode", sa.Text(), nullable=True))
    op.add_column("traces",sa.Column("confidence", sa.Text(), nullable=True))
    op.add_column("traces",sa.Column("reasoning", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("traces","reasoning")
    op.drop_column("traces","confidence")
    op.drop_column("traces","failure_mode")
