"""Initial migration

Revision ID: 8e5d189e06d6
Revises: 
Create Date: 2025-05-10 03:36:30.488304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone

# revision identifiers, used by Alembic.
revision: str = '8e5d189e06d6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
     # Creating the "users" table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.Column('role', sa.String(), default='customer'),
        sa.Column('created_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )

    # Creating the "categories" table
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Creating the "products" table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=True),
        sa.Column('quantity', sa.Integer(), default=0),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)),
        sa.PrimaryKeyConstraint('id')
    )

    # Creating the "stocks" table
    op.create_table(
        'stocks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id')),
        sa.Column('available_quantity', sa.Integer(), default=0),
        sa.Column('product_price', sa.Integer(), nullable=True),
        sa.Column('total_price', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)),
        sa.PrimaryKeyConstraint('id')
    )

    # Creating the "customers" table
    op.create_table(
        'customers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)),
        sa.PrimaryKeyConstraint('id')
    )

    # Creating the "suppliers" table
    op.create_table(
        'suppliers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)),
        sa.PrimaryKeyConstraint('id')
    )

    # Creating the "incoming_orders" table
    op.create_table(
        'incoming_orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('supplier_id', sa.Integer(), sa.ForeignKey('suppliers.id')),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id')),
        sa.Column('quantity', sa.Integer(), default=0),
        sa.Column('total_price', sa.Integer(), default=0),
        sa.Column('supply_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)),
        sa.PrimaryKeyConstraint('id')
    )

    # Creating the "outgoing_orders" table
    op.create_table(
        'outgoing_orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), sa.ForeignKey('customers.id')),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id')),
        sa.Column('quantity', sa.Integer(), default=0),
        sa.Column('total_price', sa.Integer(), default=0),
        sa.Column('order_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    """Downgrade schema."""
    op.drop_table('outgoing_orders')
    op.drop_table('incoming_orders')
    op.drop_table('suppliers')
    op.drop_table('customers')
    op.drop_table('stocks')
    op.drop_table('products')
    op.drop_table('categories')
    op.drop_table('users')
