"""empty message

Revision ID: 2eda2e568ba7
Revises: 4b0c374e4f58
Create Date: 2019-04-08 17:50:20.444861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2eda2e568ba7'
down_revision = '4b0c374e4f58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_organization', table_name='user')
    op.create_index(op.f('ix_user_organization'), 'user', ['organization'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_organization'), table_name='user')
    op.create_index('ix_user_organization', 'user', ['organization'], unique=1)
    # ### end Alembic commands ###