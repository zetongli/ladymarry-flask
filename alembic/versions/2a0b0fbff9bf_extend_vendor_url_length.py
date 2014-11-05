"""Extend vendor url length

Revision ID: 2a0b0fbff9bf
Revises: 117c1978d
Create Date: 2014-11-05 15:55:31.161179

"""

# revision identifiers, used by Alembic.
revision = '2a0b0fbff9bf'
down_revision = '117c1978d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute('alter table vendors modify profile_image varchar(512);')
    op.execute('alter table vendors modify cover_image varchar(512);')
    op.execute('alter table vendors modify website varchar(512);')

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute('alter table vendors modify profile_image varchar(255);')
    op.execute('alter table vendors modify cover_image varchar(255);')
    op.execute('alter table vendors modify website varchar(255);')
    ### end Alembic commands ###
