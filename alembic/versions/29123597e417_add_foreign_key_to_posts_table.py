"""add foreign key to posts table

Revision ID: 29123597e417
Revises: 280c85919dc4
Create Date: 2022-02-04 17:29:47.483825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29123597e417'
down_revision = '280c85919dc4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fkey',
                            source_table='posts',
                            referent_table='users',
                            local_cols = ['owner_id'],
                            remote_cols=['id'],
                            ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column(table_name='posts', column_name='owner_id')
    pass
