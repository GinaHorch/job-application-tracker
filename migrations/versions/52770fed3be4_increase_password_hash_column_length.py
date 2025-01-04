"""Increase password_hash column length

Revision ID: 52770fed3be4
Revises: d2001dca8ae8
Create Date: 2025-01-04 19:46:39.709958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52770fed3be4'
down_revision = 'd2001dca8ae8'
branch_labels = None
depends_on = None


def upgrade():
    # Increase the length of password_hash column to 512 characters
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=256),
               type_=sa.String(length=512),
               existing_nullable=False)  # Ensure nullable state matches your model


def downgrade():
    # Revert the length of password_hash column back to 256 characters
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=512),
               type_=sa.VARCHAR(length=256),
               existing_nullable=False)  # Ensure nullable state matches your model
