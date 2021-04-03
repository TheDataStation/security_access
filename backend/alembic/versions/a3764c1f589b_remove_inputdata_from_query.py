"""remove inputdata from query

Revision ID: a3764c1f589b
Revises: 
Create Date: 2021-04-01 23:14:38.960491

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'a3764c1f589b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_operator', sa.Boolean(), nullable=True),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_full_name'), 'user', ['full_name'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('access',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('sharer_id', sa.Integer(), nullable=False),
    sa.Column('decision', sa.String(), nullable=False),
    sa.Column('reveal_sharer', sa.Boolean(), nullable=True),
    sa.Column('decision_reason', sa.String(), nullable=True),
    sa.Column('expiry', sa.DateTime(), nullable=True),
    sa.CheckConstraint("decision = 'maybe' OR (decision_reason IS NOT NULL AND length(decision_reason) > 0)"),
    sa.ForeignKeyConstraint(['sharer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_access_id'), 'access', ['id'], unique=False)
    op.create_table('dataset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('sharer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['sharer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dataset_description'), 'dataset', ['description'], unique=False)
    op.create_index(op.f('ix_dataset_id'), 'dataset', ['id'], unique=False)
    op.create_index(op.f('ix_dataset_title'), 'dataset', ['title'], unique=False)
    op.create_table('query',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('querier_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('payload', sqlite.JSON(), nullable=False),
    sa.Column('status_reason', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['querier_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_query_id'), 'query', ['id'], unique=False)
    op.create_table('accessgrantsdataset',
    sa.Column('access_id', sa.Integer(), nullable=False),
    sa.Column('dataset_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['access_id'], ['access.id'], ),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('access_id', 'dataset_id')
    )
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('dataset_id', sa.Integer(), nullable=True),
    sa.Column('sharer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.ForeignKeyConstraint(['sharer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_id'), 'file', ['id'], unique=False)
    op.create_index(op.f('ix_file_name'), 'file', ['name'], unique=False)
    op.create_index(op.f('ix_file_url'), 'file', ['url'], unique=True)
    op.create_table('queryrequestsaccess',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('reveal_input_data', sa.Boolean(), nullable=True),
    sa.Column('reveal_querier', sa.Boolean(), nullable=True),
    sa.Column('query_id', sa.Integer(), nullable=False),
    sa.Column('access_id', sa.Integer(), nullable=False),
    sa.Column('expiry', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['access_id'], ['access.id'], ),
    sa.ForeignKeyConstraint(['query_id'], ['query.id'], ),
    sa.PrimaryKeyConstraint('query_id', 'access_id')
    )
    op.create_table('queryusesdataset',
    sa.Column('query_id', sa.Integer(), nullable=False),
    sa.Column('dataset_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.ForeignKeyConstraint(['query_id'], ['query.id'], ),
    sa.PrimaryKeyConstraint('query_id', 'dataset_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('queryusesdataset')
    op.drop_table('queryrequestsaccess')
    op.drop_index(op.f('ix_file_url'), table_name='file')
    op.drop_index(op.f('ix_file_name'), table_name='file')
    op.drop_index(op.f('ix_file_id'), table_name='file')
    op.drop_table('file')
    op.drop_table('accessgrantsdataset')
    op.drop_index(op.f('ix_query_id'), table_name='query')
    op.drop_table('query')
    op.drop_index(op.f('ix_dataset_title'), table_name='dataset')
    op.drop_index(op.f('ix_dataset_id'), table_name='dataset')
    op.drop_index(op.f('ix_dataset_description'), table_name='dataset')
    op.drop_table('dataset')
    op.drop_index(op.f('ix_access_id'), table_name='access')
    op.drop_table('access')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_full_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
