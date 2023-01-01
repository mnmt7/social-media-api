"""add user table

Revision ID: 4479e0113b21
Revises: bb5031a00986
Create Date: 2023-01-01 11:27:54.498998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4479e0113b21'
down_revision = 'bb5031a00986'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
