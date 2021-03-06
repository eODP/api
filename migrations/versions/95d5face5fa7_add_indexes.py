"""add_indexes

Revision ID: 95d5face5fa7
Revises: 5a8de34b1085
Create Date: 2020-05-21 07:31:30.569555

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "95d5face5fa7"
down_revision = "5a8de34b1085"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_index(op.f("ix_cores_type"), "cores", ["type"], unique=False)
    op.create_index(op.f("ix_samples_bottom"), "samples", ["bottom"], unique=False)
    op.create_index(
        op.f("ix_samples_principal_lithology_name"),
        "samples",
        ["principal_lithology_name"],
        unique=False,
    )
    op.create_index(op.f("ix_samples_top"), "samples", ["top"], unique=False)
    op.create_index(op.f("ix_sections_aw"), "sections", ["aw"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_sections_aw"), table_name="sections")
    op.drop_index(op.f("ix_samples_top"), table_name="samples")
    op.drop_index(op.f("ix_samples_principal_lithology_name"), table_name="samples")
    op.drop_index(op.f("ix_samples_bottom"), table_name="samples")
    op.drop_index(op.f("ix_cores_type"), table_name="cores")
    # ### end Alembic commands ###
