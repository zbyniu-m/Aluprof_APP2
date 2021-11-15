"""empty message

Revision ID: f15a5c3e2b65
Revises: 
Create Date: 2021-10-23 22:38:26.324125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f15a5c3e2b65'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('query_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner', sa.Integer(), nullable=False),
    sa.Column('query_name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('modification_date', sa.DateTime(), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('schedule', sa.Boolean(), nullable=False),
    sa.Column('schedule_interval', sa.String(length=1), nullable=True),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.Column('query_string', sa.Text(), nullable=False),
    sa.Column('localization', sa.String(length=255), nullable=False),
    sa.Column('restricted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['owner'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_query_table_query_name'), 'query_table', ['query_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_query_table_query_name'), table_name='query_table')
    op.drop_table('query_table')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_table('roles')
    # ### end Alembic commands ###