"""add verbatim_name to Taxon

Revision ID: e273dbddc079
Revises: f4fe705a0e6f
Create Date: 2020-06-08 21:25:22.276200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e273dbddc079"
down_revision = "f4fe705a0e6f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("taxa", sa.Column("verbatim_name", sa.String(), nullable=True))
    op.drop_column("taxa", "data_source_url")
    op.drop_column("taxa", "data_source_notes")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "taxa",
        sa.Column("data_source_notes", sa.TEXT(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "taxa",
        sa.Column("data_source_url", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("taxa", "verbatim_name")
    # ### end Alembic commands ###
