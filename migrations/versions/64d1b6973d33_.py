"""empty message

Revision ID: 64d1b6973d33
Revises: 2da678c51b94
Create Date: 2019-05-11 16:53:03.631522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64d1b6973d33'
down_revision = '2da678c51b94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscription') as batch_op:
        batch_op.drop_column('query')   
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscription', sa.Column('query', sa.VARCHAR(length=200), nullable=True))
    op.create_index('ix_subscription_query', 'subscription', ['query'], unique=False)
    op.drop_index(op.f('ix_subscription_q'), table_name='subscription')
    op.drop_column('subscription', 'q')
    op.create_table('tasks',
    sa.Column('id', sa.VARCHAR(length=191), nullable=False),
    sa.Column('next_run_time', sa.FLOAT(), nullable=True),
    sa.Column('job_state', sa.BLOB(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tasks_next_run_time', 'tasks', ['next_run_time'], unique=False)
    # ### end Alembic commands ###
