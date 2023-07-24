"""Initial migration

Revision ID: 8776c65ff606
Revises: 
Create Date: 2023-07-23 21:40:14.192248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8776c65ff606'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('last_seen_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('operations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('operation_type', sa.Enum('income', 'expense', native_enum=False), nullable=False),
    sa.Column('amount_100x', sa.Integer(), nullable=False),
    sa.Column('currency', sa.Enum('USD', 'EUR', 'BYN', 'PLN', 'RUB', 'USDT', native_enum=False), nullable=False),
    sa.Column('note', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_operations_user_id'), 'operations', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_operations_user_id'), table_name='operations')
    op.drop_table('operations')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###