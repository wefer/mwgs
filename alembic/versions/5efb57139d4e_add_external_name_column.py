"""add (external) name column

Revision ID: 5efb57139d4e
Revises: 5458be78af7e
Create Date: 2017-01-16 09:56:46.390354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5efb57139d4e'
down_revision = '5458be78af7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sample', sa.Column('name', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sample', 'name')
    # ### end Alembic commands ###
