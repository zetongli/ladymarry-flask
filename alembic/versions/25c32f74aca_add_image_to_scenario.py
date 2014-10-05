"""Add image to scenario.

Revision ID: 25c32f74aca
Revises: d75d5f90d3
Create Date: 2014-10-05 22:18:08.880662

"""

# revision identifiers, used by Alembic.
revision = '25c32f74aca'
down_revision = 'd75d5f90d3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scenarios', sa.Column('image', sa.String(length=255), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scenarios', 'image')
    ### end Alembic commands ###
