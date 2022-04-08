"""Add user table.

Revision ID: 2919a833d169
Revises: 37f910a77b10
Create Date: 2022-04-06 10:21:05.893775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2919a833d169'
down_revision = '37f910a77b10'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable = False),
    sa.Column('email', sa.String(), nullable = False),
    sa.Column('password', sa.String(), nullable = False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), \
        nullable = False, server_default = sa.text('now()')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
