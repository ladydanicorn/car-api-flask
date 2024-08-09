"""Alter User and Car tables to use UUID

Revision ID: fe8a470f8469
Revises: 29c3d3503714
Create Date: 2024-08-07 14:08:15.424967

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fe8a470f8469'
down_revision = '29c3d3503714'
branch_labels = None
depends_on = None

def upgrade():
    # Add new UUID columns
    op.add_column('user', sa.Column('new_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('car', sa.Column('new_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('car', sa.Column('new_user_id', postgresql.UUID(as_uuid=True), nullable=True))

    # Generate UUIDs for existing rows
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
    op.execute("UPDATE \"user\" SET new_id = uuid_generate_v4()")
    op.execute("UPDATE car SET new_id = uuid_generate_v4(), new_user_id = (SELECT new_id FROM \"user\" WHERE \"user\".id = car.user_id)")

    # Set new columns as not nullable
    op.alter_column('user', 'new_id', nullable=False)
    op.alter_column('car', 'new_id', nullable=False)
    op.alter_column('car', 'new_user_id', nullable=False)

    # Drop foreign key first
    op.drop_constraint('car_user_id_fkey', 'car', type_='foreignkey')

    # Now drop primary keys
    op.drop_constraint('user_pkey', 'user', type_='primary')
    op.drop_constraint('car_pkey', 'car', type_='primary')

    # Set new primary keys
    op.create_primary_key('user_pkey', 'user', ['new_id'])
    op.create_primary_key('car_pkey', 'car', ['new_id'])

    # Drop old columns
    op.drop_column('user', 'id')
    op.drop_column('car', 'id')
    op.drop_column('car', 'user_id')

    # Rename new columns
    op.alter_column('user', 'new_id', new_column_name='id')
    op.alter_column('car', 'new_id', new_column_name='id')
    op.alter_column('car', 'new_user_id', new_column_name='user_id')

    # Create new foreign key
    op.create_foreign_key('car_user_id_fkey', 'car', 'user', ['user_id'], ['id'])

    # Alter password column length
    op.alter_column('user', 'password', type_=sa.String(255))

def downgrade():
    # This is a one-way migration, downgrade is not supported
    pass