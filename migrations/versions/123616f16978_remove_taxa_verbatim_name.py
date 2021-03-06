"""remove taxa verbatim_name

Revision ID: 123616f16978
Revises: a9c88584741a
Create Date: 2020-10-15 17:42:34.492767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "123616f16978"
down_revision = "a9c88584741a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("taxa", "verbatim_name")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "taxa",
        sa.Column("verbatim_name", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
