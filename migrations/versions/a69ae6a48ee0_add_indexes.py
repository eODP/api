"""add_indexes

Revision ID: a69ae6a48ee0
Revises: 772be6b089a8
Create Date: 2022-02-22 20:15:38.630465

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a69ae6a48ee0'
down_revision = '772be6b089a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_taxa_name'), 'taxa', ['name'], unique=False)
    op.create_index(op.f('ix_taxa_taxon_group'), 'taxa', ['taxon_group'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_taxa_taxon_group'), table_name='taxa')
    op.drop_index(op.f('ix_taxa_name'), table_name='taxa')
    # ### end Alembic commands ###