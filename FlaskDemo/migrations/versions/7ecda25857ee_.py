"""empty message

Revision ID: 7ecda25857ee
Revises: 
Create Date: 2017-11-18 20:53:47.579877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ecda25857ee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flask_user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('user', sa.String(length=50), nullable=False),
    sa.Column('password_hash', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flask_user')
    # ### end Alembic commands ###
