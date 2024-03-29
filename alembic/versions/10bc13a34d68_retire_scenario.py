"""retire scenario

Revision ID: 10bc13a34d68
Revises: 2a0b0fbff9bf
Create Date: 2014-11-05 16:25:21.056931

"""

# revision identifiers, used by Alembic.
revision = '10bc13a34d68'
down_revision = '2a0b0fbff9bf'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks_scenarios')
    op.drop_table('scenarios')
    op.alter_column('tasks', 'required',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True,
               existing_server_default='1')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'required',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True,
               existing_server_default='1')
    op.create_table('scenarios',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('when', mysql.TEXT(), nullable=True),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('image', mysql.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.create_table('tasks_scenarios',
    sa.Column('task_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('scenario_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['scenario_id'], [u'scenarios.id'], name=u'tasks_scenarios_ibfk_2', ondelete=u'CASCADE'),
    sa.ForeignKeyConstraint(['task_id'], [u'tasks.id'], name=u'tasks_scenarios_ibfk_1', ondelete=u'CASCADE'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    ### end Alembic commands ###
