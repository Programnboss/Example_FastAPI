"""Create posts table

Revision ID: 5a7ce1739f76
Revises: 
Create Date: 2022-04-05 23:34:52.902093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a7ce1739f76'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    #Ref Alembic documentation -> API -> DDL for commands.
    op.create_table('posts', sa.Column('id', sa.Integer, primary_key = True, nullable = False), \
        sa.Column('title', sa.String, nullable = False))
        # sa.Column('content', sa.String, nullable = False),
        # sa.Column('published', sa.Boolean, server_default = 'True', nullable = False),
        # sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text('now()')),
        # sa.Column('owner_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable= False)

    pass


def downgrade():
    op.drop_table("posts")
    pass
