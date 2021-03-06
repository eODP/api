"""empty add_sample_indexes

Revision ID: 95366f06d67d
Revises: 95d5face5fa7
Create Date: 2020-05-21 10:31:15.407111

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "95366f06d67d"
down_revision = "95d5face5fa7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_index(
        op.f("ix_samples_bottom_depth"), "samples", ["bottom_depth"], unique=False
    )
    op.create_index(
        op.f("ix_samples_data_source_notes"),
        "samples",
        ["data_source_notes"],
        unique=False,
    )
    op.create_index(
        op.f("ix_samples_minor_lithology_name"),
        "samples",
        ["minor_lithology_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_samples_minor_lithology_prefix"),
        "samples",
        ["minor_lithology_prefix"],
        unique=False,
    )
    op.create_index(
        op.f("ix_samples_minor_lithology_suffix"),
        "samples",
        ["minor_lithology_suffix"],
        unique=False,
    )
    op.create_index(
        op.f("ix_samples_principal_lithology_prefix"),
        "samples",
        ["principal_lithology_prefix"],
        unique=False,
    )
    op.create_index(
        op.f("ix_samples_principal_lithology_suffix"),
        "samples",
        ["principal_lithology_suffix"],
        unique=False,
    )
    op.create_index(
        op.f("ix_samples_top_depth"), "samples", ["top_depth"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_samples_top_depth"), table_name="samples")
    op.drop_index(op.f("ix_samples_principal_lithology_suffix"), table_name="samples")
    op.drop_index(op.f("ix_samples_principal_lithology_prefix"), table_name="samples")
    op.drop_index(op.f("ix_samples_minor_lithology_suffix"), table_name="samples")
    op.drop_index(op.f("ix_samples_minor_lithology_prefix"), table_name="samples")
    op.drop_index(op.f("ix_samples_minor_lithology_name"), table_name="samples")
    op.drop_index(op.f("ix_samples_data_source_notes"), table_name="samples")
    op.drop_index(op.f("ix_samples_bottom_depth"), table_name="samples")
    # ### end Alembic commands ###
