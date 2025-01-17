"""Make password_hash non-nullable

Revision ID: cd6d8fa2f119
Revises: 52770fed3be4
Create Date: 2025-01-04 20:09:36.315819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd6d8fa2f119'
down_revision = '52770fed3be4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=256),
               type_=sa.String(length=512),
               existing_nullable=False)
        batch_op.alter_column('username',
                existing_type=sa.String(length=64),
                type_=sa.String(length=128),  # Increase to 128
                existing_nullable=False)
        batch_op.alter_column('email',
                existing_type=sa.String(length=120),
                type_=sa.String(length=254),  # Increase to 254
                existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=512),
               type_=sa.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('username',
                existing_type=sa.String(length=128),
                type_=sa.String(length=64),  # Revert to 64
                existing_nullable=False)
        batch_op.alter_column('email',
                existing_type=sa.String(length=254),
                type_=sa.String(length=120),  # Revert to 120
                existing_nullable=False)

    # ### end Alembic commands ###
