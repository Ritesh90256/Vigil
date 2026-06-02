"""create traces table

Revision ID: 6e642af730a9
Revises: 
Create Date: 2026-06-02 16:32:18.956851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e642af730a9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'traces',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('input', sa.Text),
        sa.Column('output', sa.Text),
        sa.Column('latency', sa.Integer),
        sa.Column('created_at', sa.TIMESTAMP)
    )


def downgrade():
    op.drop_table('traces')
