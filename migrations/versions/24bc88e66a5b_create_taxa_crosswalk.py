"""create_taxa_crosswalk

Revision ID: 24bc88e66a5b
Revises: 123616f16978
Create Date: 2020-10-15 20:56:28.939656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "24bc88e66a5b"
down_revision = "123616f16978"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "taxa_crosswalk",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("taxon_id", sa.Integer(), nullable=True),
        sa.Column("original_name", sa.String(), nullable=False),
        sa.Column("taxon_group", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["taxon_id"], ["taxa.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("taxa_crosswalk")
    # ### end Alembic commands ###
