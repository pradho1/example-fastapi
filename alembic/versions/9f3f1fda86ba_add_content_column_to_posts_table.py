"""add content column to posts table

Revision ID: 9f3f1fda86ba
Revises: 2bea062b0003
Create Date: 2022-02-04 17:11:06.423995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f3f1fda86ba'
down_revision = '2bea062b0003'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
