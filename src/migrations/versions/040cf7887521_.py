"""empty message

Revision ID: 040cf7887521
Revises: 12dce0ffea7f
Create Date: 2021-07-09 13:31:34.055534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '040cf7887521'
down_revision = '12dce0ffea7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_login', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('last_request', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_request')
    op.drop_column('users', 'last_login')
    # ### end Alembic commands ###
