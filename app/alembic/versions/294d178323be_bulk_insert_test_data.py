"""bulk insert test data

Revision ID: 294d178323be
Revises: 947f50c56cd4
Create Date: 2023-04-26 14:42:01.669952

"""
from datetime import datetime
from alembic import op
from sqlalchemy.sql import table, column
import sqlalchemy as sa
from schemas.user import get_password_hash
from settings import ADMIN_DEFAULT_PASSWORD, USER_DEFAULT_PASSWORD


# revision identifiers, used by Alembic.
revision = "294d178323be"
down_revision = "947f50c56cd4"
branch_labels = None
depends_on = None


def upgrade() -> None:

    company_table = table("company",
                          sa.Column('name', sa.String(
                              length=50), nullable=True),
                          sa.Column('description', sa.String(
                              length=255), nullable=True),
                          sa.Column('mode', sa.Boolean(), nullable=True),
                          sa.Column('rating', sa.Float(), nullable=True),
                          sa.Column('id', sa.Uuid(), nullable=False),
                          sa.Column('created_at', sa.Time(), nullable=False),
                          sa.Column('updated_at', sa.Time(), nullable=False),
                          )
    companies = [{
        "id": "b0c58567-7e88-4355-89fb-189b09dc3d0d",
        "name": "Acme Corporation",
        "description": "A leading provider of widgets.",
        "mode": True,
        "rating": 4.5,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }, {
        "id": "70bc0ef5-0a59-46eb-84d5-a04c7966630e",
        "name": "Widget Inc.",
        "description": "A growing company that provides high-quality widgets.",
        "mode": True,
        "rating": 4.0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }]

    # Bulk insert the companies into the database
    op.bulk_insert(company_table, companies)

    user_table = table("users", sa.Column('email', sa.String(length=50), nullable=True),
                       sa.Column('username', sa.String(),
                                 nullable=True),
                       sa.Column('first_name', sa.String(),
                                 nullable=False),
                       sa.Column('last_name', sa.String(),
                                 nullable=False),
                       sa.Column('is_active', sa.Boolean(),
                                 nullable=True),
                       sa.Column('is_admin', sa.Boolean(),
                                 nullable=True),
                       sa.Column('company_id', sa.Uuid(),
                                 nullable=True),
                       sa.Column('hashed_password', sa.String(
                           length=255), nullable=True),
                       sa.Column('id', sa.Uuid(), nullable=False),
                       sa.Column('created_at', sa.Time(),
                                 nullable=False),
                       sa.Column('updated_at', sa.Time(), nullable=False))
    users = [{
        "id": "8e09820a-abc2-433a-9472-94a09e390631",
        "email": "user1@example.com",
        "username": "admin",
        "hashed_password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
        "first_name": "John",
        "last_name": "Doe",
        "is_active": True,
        "is_admin": True,
        "company_id": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }, {
        "id": "5de8a492-6735-4abe-a758-576ce3a42ac4",
        "email": "user2@example.com",
        "username": "user",
        "hashed_password": get_password_hash(USER_DEFAULT_PASSWORD),
        "first_name": "Jane",
        "last_name": "Doe",
        "is_active": True,
        "is_admin": False,
        "company_id": "b0c58567-7e88-4355-89fb-189b09dc3d0d",
        "password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }]
    op.bulk_insert(user_table, users)


def downgrade() -> None:
    op.execute('DELETE FROM users WHERE email IN ('
               '"user1@example.com", "user2@example.com"'
               ')')
    op.execute('DELETE FROM company WHERE id IN ('
               '"b0c58567-7e88-4355-89fb-189b09dc3d0d", "70bc0ef5-0a59-46eb-84d5-a04c7966630e"'
               ')')
