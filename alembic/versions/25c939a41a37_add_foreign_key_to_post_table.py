"""add foreign key to post table

Revision ID: 25c939a41a37
Revises: 4479e0113b21
Create Date: 2023-01-01 11:39:04.180323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25c939a41a37'
down_revision = '4479e0113b21'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts",
                            referent_table="users", local_cols=['owner_id'],
                            remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
