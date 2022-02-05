"""add last few columns to posts table

Revision ID: 4a66c03ac6de
Revises: 29123597e417
Create Date: 2022-02-04 18:04:27.740025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a66c03ac6de'
down_revision = '29123597e417'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(table_name='posts',
                column=sa.Column('published',sa.Boolean(), nullable=False, server_default='TRUE')
            )
    op.add_column(table_name='posts',
                column=sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
            )
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
