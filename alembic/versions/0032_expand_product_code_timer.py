"""Increase the product code timer limit to 1000 hours.

Revision ID: 0032
Revises: 0031
"""

from alembic import op

revision = "0032"
down_revision = "0031"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("ck_products_code_cooldown_hours", "products", type_="check")
    op.create_check_constraint(
        "ck_products_code_cooldown_hours",
        "products",
        "code_cooldown_hours BETWEEN 0 AND 1000",
    )


def downgrade():
    op.drop_constraint("ck_products_code_cooldown_hours", "products", type_="check")
    op.create_check_constraint(
        "ck_products_code_cooldown_hours",
        "products",
        "code_cooldown_hours BETWEEN 0 AND 720",
    )
