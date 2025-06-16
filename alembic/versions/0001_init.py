"""init

Revision ID: 0001
Revises:
Create Date: 2025-06-16 23:44:41.184970

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute('CREATE SCHEMA IF NOT EXISTS challenges')
    op.create_table(
        'challenges',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('created', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=False),
        sa.Column('updated', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=False),
        sa.Column('archived', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='challenges',
    )
    op.create_table(
        'user',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('created', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=False),
        sa.Column('updated', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=False),
        sa.Column('archived', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='challenges',
    )
    op.create_table(
        'user_contacts',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('created', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=False),
        sa.Column('updated', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=False),
        sa.Column('archived', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('contact_type', sa.String(), nullable=False),
        sa.Column('contact', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['challenges.user.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        schema='challenges',
    )
    op.create_index('user_contacts_contact_idx', 'user_contacts', ['contact'], unique=False, schema='challenges')
    op.create_index(
        'user_contacts_contact_type_contact_idx',
        'user_contacts',
        ['contact_type', 'contact'],
        unique=True,
        schema='challenges',
    )
    op.create_index('user_contacts_user_id_idx', 'user_contacts', ['user_id'], unique=False, schema='challenges')


def downgrade() -> None:
    op.execute('DROP SCHEMA IF EXISTS challenges CASCADE')
