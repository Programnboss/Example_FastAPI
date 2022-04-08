"""Add 'content' column to posts table.

Revision ID: 37f910a77b10
Revises: 5a7ce1739f76
Create Date: 2022-04-06 09:31:51.825005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37f910a77b10'
down_revision = '5a7ce1739f76'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable = False))
    pass


def downgrade():
    op.drop_column('posts', sa.Column('content'))
    pass
