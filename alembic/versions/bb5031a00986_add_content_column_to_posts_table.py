"""Add content column to posts table

Revision ID: bb5031a00986
Revises: 94db42c8d594
Create Date: 2023-01-01 11:11:12.726083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb5031a00986'
down_revision = '94db42c8d594'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
