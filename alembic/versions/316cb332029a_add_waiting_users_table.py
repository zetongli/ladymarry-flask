"""Add waiting users table

Revision ID: 316cb332029a
Revises: 25c32f74aca
Create Date: 2014-10-10 16:09:04.047795

"""

# revision identifiers, used by Alembic.
revision = '316cb332029a'
down_revision = '25c32f74aca'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('waiting_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('registered_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('waiting_users')
    ### end Alembic commands ###