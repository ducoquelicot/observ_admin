"""empty message

Revision ID: fa51fb49f54c
Revises: 8149ce2311e0
Create Date: 2019-05-11 15:40:02.188406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa51fb49f54c'
down_revision = '8149ce2311e0'
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