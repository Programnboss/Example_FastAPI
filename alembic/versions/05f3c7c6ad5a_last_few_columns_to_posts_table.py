"""last few columns to posts table.

Revision ID: 05f3c7c6ad5a
Revises: 085ae3000b43
Create Date: 2022-04-06 12:03:45.058769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05f3c7c6ad5a'
down_revision = '085ae3000b43'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', \
        sa.Column('published', 
            sa.Boolean, 
            server_default = 'True', 
            nullable = False))
    op.add_column('posts', \
        sa.Column('created_at', 
        sa.TIMESTAMP(timezone=True), 
        nullable = False, 
        server_default = sa.text('now()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
