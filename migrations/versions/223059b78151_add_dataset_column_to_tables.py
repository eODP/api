"""add dataset column to tables

Revision ID: 223059b78151
Revises: 62ff80715d43
Create Date: 2021-04-30 12:08:22.757961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '223059b78151'
down_revision = '62ff80715d43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cores', sa.Column('dataset', sa.String(), nullable=True))
    op.create_index(op.f('ix_cores_dataset'), 'cores', ['dataset'], unique=False)
    op.add_column('expeditions', sa.Column('dataset', sa.String(), nullable=True))
    op.create_index(op.f('ix_expeditions_dataset'), 'expeditions', ['dataset'], unique=False)
    op.add_column('holes', sa.Column('dataset', sa.String(), nullable=True))
    op.create_index(op.f('ix_holes_dataset'), 'holes', ['dataset'], unique=False)
    op.add_column('samples', sa.Column('dataset', sa.String(), nullable=True))
    op.create_index(op.f('ix_samples_dataset'), 'samples', ['dataset'], unique=False)
    op.create_foreign_key(None, 'samples', 'sections', ['section_id'], ['id'])
    op.add_column('samples_taxa', sa.Column('dataset', sa.String(), nullable=True))
    op.create_index(op.f('ix_samples_taxa_dataset'), 'samples_taxa', ['dataset'], unique=False)
    op.add_column('sections', sa.Column('dataset', sa.String(), nullable=True))
    op.create_index(op.f('ix_sections_dataset'), 'sections', ['dataset'], unique=False)
    op.add_column('sites', sa.Column('dataset', sa.String(), nullable=True))
    op.create_index(op.f('ix_sites_dataset'), 'sites', ['dataset'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sites_dataset'), table_name='sites')
    op.drop_column('sites', 'dataset')
    op.drop_index(op.f('ix_sections_dataset'), table_name='sections')
    op.drop_column('sections', 'dataset')
    op.drop_index(op.f('ix_samples_taxa_dataset'), table_name='samples_taxa')
    op.drop_column('samples_taxa', 'dataset')
    op.drop_constraint(None, 'samples', type_='foreignkey')
    op.drop_index(op.f('ix_samples_dataset'), table_name='samples')
    op.drop_column('samples', 'dataset')
    op.drop_index(op.f('ix_holes_dataset'), table_name='holes')
    op.drop_column('holes', 'dataset')
    op.drop_index(op.f('ix_expeditions_dataset'), table_name='expeditions')
    op.drop_column('expeditions', 'dataset')
    op.drop_index(op.f('ix_cores_dataset'), table_name='cores')
    op.drop_column('cores', 'dataset')
    # ### end Alembic commands ###
