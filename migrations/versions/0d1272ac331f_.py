"""empty message

Revision ID: 0d1272ac331f
Revises: c5ac1b409ec6
Create Date: 2023-03-24 12:16:19.987672

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0d1272ac331f'
down_revision = 'c5ac1b409ec6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('download_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('referrer', sa.String(length=500), nullable=True),
    sa.Column('yt_url', sa.String(length=500), nullable=True),
    sa.Column('yt_title', sa.String(length=500), nullable=True),
    sa.Column('yt_type', sa.String(length=50), nullable=True),
    sa.Column('yt_size', sa.String(length=50), nullable=True),
    sa.Column('yt_resolution', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('visit_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ip', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('city', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('region', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('country', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('org', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('platform', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('browser', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('version', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('language', sa.String(length=100), nullable=True))
        batch_op.alter_column('url',
               existing_type=mysql.VARCHAR(length=500),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('visit_data', schema=None) as batch_op:
        batch_op.alter_column('url',
               existing_type=mysql.VARCHAR(length=500),
               nullable=False)
        batch_op.drop_column('language')
        batch_op.drop_column('version')
        batch_op.drop_column('browser')
        batch_op.drop_column('platform')
        batch_op.drop_column('org')
        batch_op.drop_column('country')
        batch_op.drop_column('region')
        batch_op.drop_column('city')
        batch_op.drop_column('ip')

    op.drop_table('download_data')
    # ### end Alembic commands ###