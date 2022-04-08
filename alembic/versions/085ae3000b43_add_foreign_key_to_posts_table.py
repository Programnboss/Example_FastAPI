"""Add Foreign Key to posts table.

Revision ID: 085ae3000b43
Revises: 2919a833d169
Create Date: 2022-04-06 11:53:12.435238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '085ae3000b43'
down_revision = '2919a833d169'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts', \
        sa.Column('owner_id', 
        sa.Integer, 
        nullable= False)
        )
    op.create_foreign_key('posts_users_fk', \
        source_table="posts", 
        referent_table="users", 
        local_cols=['owner_id'], 
        remote_cols=['id'], 
        ondelete="CASCADE"
        )
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
