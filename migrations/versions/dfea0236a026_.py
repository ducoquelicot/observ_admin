"""empty message

Revision ID: dfea0236a026
Revises: 
Create Date: 2019-05-15 13:23:15.009979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfea0236a026'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.Column('doctype', sa.String(length=64), nullable=True),
    sa.Column('date', sa.String(length=64), nullable=True),
    sa.Column('body', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_records_body'), 'records', ['body'], unique=False)
    op.create_index(op.f('ix_records_city'), 'records', ['city'], unique=False)
    op.create_index(op.f('ix_records_doctype'), 'records', ['doctype'], unique=False)
    op.create_index(op.f('ix_records_name'), 'records', ['name'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('organization', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_organization'), 'user', ['organization'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('subscription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('q', sa.String(length=200), nullable=True),
    sa.Column('city', sa.Text(), nullable=True),
    sa.Column('doctype', sa.String(length=64), nullable=True),
    sa.Column('frequency', sa.String(length=30), nullable=True),
    sa.Column('output', sa.Text(), nullable=True),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscription_city'), 'subscription', ['city'], unique=False)
    op.create_index(op.f('ix_subscription_doctype'), 'subscription', ['doctype'], unique=False)
    op.create_index(op.f('ix_subscription_frequency'), 'subscription', ['frequency'], unique=False)
    op.create_index(op.f('ix_subscription_output'), 'subscription', ['output'], unique=False)
    op.create_index(op.f('ix_subscription_q'), 'subscription', ['q'], unique=False)
    op.create_index(op.f('ix_subscription_total'), 'subscription', ['total'], unique=False)

    op.create_table('scraper',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('links', sa.Text(), nullable=True),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_scraper_name'), 'scraper', ['name'], unique=False)
    op.create_index(op.f('ix_scraper_links'), 'scraper', ['links'], unique=False)
    op.create_index(op.f('ix_scraper_total'), 'scraper', ['total'], unique=False)

    op.create_table('task',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
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
    op.drop_index(op.f('ix_subscription_total'), table_name='subscription')
    op.drop_index(op.f('ix_subscription_q'), table_name='subscription')
    op.drop_index(op.f('ix_subscription_output'), table_name='subscription')
    op.drop_index(op.f('ix_subscription_frequency'), table_name='subscription')
    op.drop_index(op.f('ix_subscription_doctype'), table_name='subscription')
    op.drop_index(op.f('ix_subscription_city'), table_name='subscription')
    op.drop_table('subscription')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_organization'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_records_name'), table_name='records')
    op.drop_index(op.f('ix_records_doctype'), table_name='records')
    op.drop_index(op.f('ix_records_city'), table_name='records')
    op.drop_index(op.f('ix_records_body'), table_name='records')
    op.drop_table('records')
    # ### end Alembic commands ###
