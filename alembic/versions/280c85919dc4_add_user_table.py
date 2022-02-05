"""add user table

Revision ID: 280c85919dc4
Revises: 9f3f1fda86ba
Create Date: 2022-02-04 17:18:39.614325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '280c85919dc4'
down_revision = '9f3f1fda86ba'
branch_labels = None
depends_on = None


def upgrade():
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


def downgrade():
    op.drop_table('users')
    pass
