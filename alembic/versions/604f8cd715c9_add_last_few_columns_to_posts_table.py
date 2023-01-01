"""add last few columns to posts table

Revision ID: 604f8cd715c9
Revises: 25c939a41a37
Create Date: 2023-01-01 11:49:22.695966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '604f8cd715c9'
down_revision = '25c939a41a37'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='True'))

    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
