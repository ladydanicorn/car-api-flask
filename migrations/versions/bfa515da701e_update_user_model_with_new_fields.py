"""Update User model with new fields

Revision ID: bfa515da701e
Revises: fe8a470f8469
Create Date: 2024-08-07 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bfa515da701e'
down_revision = 'fe8a470f8469'
branch_labels = None
depends_on = None

def upgrade():
    # Add new columns as nullable
    op.add_column('user', sa.Column('first_name', sa.String(100), nullable=True))
    op.add_column('user', sa.Column('last_name', sa.String(100), nullable=True))
    op.add_column('user', sa.Column('email', sa.String(120), nullable=True))
    op.add_column('user', sa.Column('date_created', sa.DateTime(), nullable=True))

    # Update existing rows with default values
    op.execute("UPDATE \"user\" SET first_name = '', last_name = '', email = '', date_created = NOW()")

    # Now set the columns as non-nullable
    op.alter_column('user', 'first_name', nullable=False)
    op.alter_column('user', 'last_name', nullable=False)
    op.alter_column('user', 'email', nullable=False)
    op.alter_column('user', 'date_created', nullable=False)

    # Add unique constraint to email
    op.create_unique_constraint(None, 'user', ['email'])

def downgrade():
    # Remove unique constraint from email
    op.drop_constraint(None, 'user', type_='unique')

    # Drop the new columns
    op.drop_column('user', 'date_created')
    op.drop_column('user', 'email')
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')