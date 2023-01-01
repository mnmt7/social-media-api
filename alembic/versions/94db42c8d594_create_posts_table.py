"""create posts table

Revision ID: 94db42c8d594
Revises: 
Create Date: 2023-01-01 11:01:18.755642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94db42c8d594'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
    , sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
