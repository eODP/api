"""add more comments fields to taxa_crosswalk

Revision ID: 0fcf4cc40b4b
Revises: 223059b78151
Create Date: 2021-05-03 15:23:09.333356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fcf4cc40b4b'
down_revision = '223059b78151'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('taxa_crosswalk', sa.Column('initial_comments', sa.String(), nullable=True))
    op.add_column('taxa_crosswalk', sa.Column('processing_notes', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('taxa_crosswalk', 'processing_notes')
    op.drop_column('taxa_crosswalk', 'initial_comments')
    # ### end Alembic commands ###