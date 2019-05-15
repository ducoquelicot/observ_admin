"""empty message

Revision ID: 4e013c60966b
Revises: 
Create Date: 2019-05-11 15:23:37.032024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e013c60966b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_tasks_next_run_time', table_name='tasks')
    op.drop_table('tasks')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.VARCHAR(length=191), nullable=False),
    sa.Column('next_run_time', sa.FLOAT(), nullable=True),
    sa.Column('job_state', sa.BLOB(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tasks_next_run_time', 'tasks', ['next_run_time'], unique=False)
    # ### end Alembic commands ###
