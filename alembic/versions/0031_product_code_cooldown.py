"""Add a per-product delay between Steam Guard codes.

Revision ID: 0031
Revises: 0030
"""

import sqlalchemy as sa

from alembic import op

revision = "0031"
down_revision = "0030"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "products",
        sa.Column("code_cooldown_hours", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_check_constraint(
        "ck_products_code_cooldown_hours",
        "products",
        "code_cooldown_hours BETWEEN 0 AND 1000",
    )


def downgrade():
    op.drop_constraint("ck_products_code_cooldown_hours", "products", type_="check")
    op.drop_column("products", "code_cooldown_hours")
