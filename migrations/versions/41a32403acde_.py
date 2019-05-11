"""empty message

Revision ID: 41a32403acde
Revises: dcb7d41a07f7
Create Date: 2019-05-09 15:34:53.670456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41a32403acde'
down_revision = 'dcb7d41a07f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('query', sa.String(length=200), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('doctype', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscription_city'), 'subscription', ['city'], unique=False)
    op.create_index(op.f('ix_subscription_doctype'), 'subscription', ['doctype'], unique=False)
    op.create_index(op.f('ix_subscription_query'), 'subscription', ['query'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_subscription_query'), table_name='subscription')
    op.drop_index(op.f('ix_subscription_doctype'), table_name='subscription')
    op.drop_index(op.f('ix_subscription_city'), table_name='subscription')
    op.drop_table('subscription')
    # ### end Alembic commands ###