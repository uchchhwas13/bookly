"""init

Revision ID: e84893af927a
Revises: 
Create Date: 2025-09-22 14:05:06.651190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e84893af927a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create users table
    op.create_table(
        'users',
        sa.Column('uid', sa.UUID(), nullable=False),
        sa.Column('username', sqlmodel.sql.sqltypes.AutoString(),
                  nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(),
                  nullable=False),
        sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(),
                  nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(),
                  server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(),
                  server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('uid')
    )

    # Alter books.published_date from VARCHAR → DATE safely
    op.alter_column(
        'books',
        'published_date',
        existing_type=sa.VARCHAR(),
        type_=sa.Date(),
        existing_nullable=False,
        postgresql_using="published_date::date"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')

    # Reverse the type change
    op.alter_column(
        'books',
        'published_date',
        existing_type=sa.Date(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using="published_date::varchar"
    )
