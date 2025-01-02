"""Initial migration

Revision ID: dd590f9f839b
Revises: 
Create Date: 2025-01-02 17:22:08.195461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd590f9f839b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_application',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_submitted', sa.Date(), nullable=False),
    sa.Column('due_date', sa.Date(), nullable=True),
    sa.Column('follow_up_date', sa.Date(), nullable=True),
    sa.Column('company', sa.String(length=120), nullable=False),
    sa.Column('contact', sa.String(length=120), nullable=True),
    sa.Column('position_title', sa.String(length=120), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('cv_submitted', sa.String(length=10), nullable=False),
    sa.Column('cover_letter_submitted', sa.String(length=10), nullable=False),
    sa.Column('follow_up_sent', sa.String(length=10), nullable=False),
    sa.Column('follow_up_message', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('job_application')
    # ### end Alembic commands ###