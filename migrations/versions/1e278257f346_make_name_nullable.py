"""empty message

Revision ID: 1e278257f346
Revises: 5c622754ebac
Create Date: 2020-05-21 06:49:06.894386

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "1e278257f346"
down_revision = "5c622754ebac"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("cores", "name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("expeditions", "name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("holes", "name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("samples", "name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("sections", "name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("sites", "name", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("sites", "name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("sections", "name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("samples", "name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("holes", "name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("expeditions", "name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("cores", "name", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###
