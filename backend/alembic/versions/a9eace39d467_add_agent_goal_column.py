"""add agent_goal column

Revision ID: a9eace39d467
Revises: 00ac21aa0583
Create Date: 2026-07-18 12:42:23.684622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9eace39d467'
down_revision: Union[str, Sequence[str], None] = '00ac21aa0583'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('traces', sa.Column('agent_goal', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('traces', 'agent_goal')
