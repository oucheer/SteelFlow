"""Add channel assets, custom requirements and order sync records."""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"


def upgrade():
    op.create_table(
        "channel_assets",
        sa.Column("id", sa.String(), primary_key=True), sa.Column("org_id", sa.String(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("channel", sa.String(), nullable=False), sa.Column("asset_type", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False), sa.Column("status", sa.String(), nullable=False, server_default="draft"),
        sa.Column("url", sa.String(), nullable=False, server_default=""), sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("provider_mode", sa.String(), nullable=False, server_default="MOCK"),
    )
    op.create_table(
        "order_syncs",
        sa.Column("id", sa.String(), primary_key=True), sa.Column("org_id", sa.String(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("order_id", sa.String(), nullable=False), sa.Column("target", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False, server_default="pending"), sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("provider_mode", sa.String(), nullable=False, server_default="MOCK"), sa.Column("last_error", sa.String(), nullable=False, server_default=""),
    )
    op.create_index("ix_order_syncs_order_id", "order_syncs", ["order_id"])
    op.create_table(
        "custom_requirements",
        sa.Column("id", sa.String(), primary_key=True), sa.Column("org_id", sa.String(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("customer_id", sa.String(), nullable=False), sa.Column("title", sa.String(), nullable=False),
        sa.Column("brief", sa.String(), nullable=False), sa.Column("dimensions", sa.JSON(), nullable=False),
        sa.Column("cad_mode", sa.String(), nullable=False, server_default="STUB"), sa.Column("design_result", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(), nullable=False, server_default="draft"), sa.Column("ai_analysis", sa.JSON(), nullable=False),
    )
    op.create_index("ix_custom_requirements_customer_id", "custom_requirements", ["customer_id"])


def downgrade():
    op.drop_index("ix_custom_requirements_customer_id", table_name="custom_requirements")
    op.drop_table("custom_requirements")
    op.drop_index("ix_order_syncs_order_id", table_name="order_syncs")
    op.drop_table("order_syncs")
    op.drop_table("channel_assets")
