"""query_gets_total_results_column

Revision ID: d0374bca3f84
Revises: 451fbb98855a
Create Date: 2019-06-20 12:25:27.843682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0374bca3f84'
down_revision = '451fbb98855a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('query', sa.Column('total_results', sa.BigInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('query', 'total_results')
    # ### end Alembic commands ###
