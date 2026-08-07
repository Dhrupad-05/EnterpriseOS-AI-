"""initial EnterpriseOS schema

Revision ID: 0001_initial_schema
Revises:
"""
from alembic import op
from sqlalchemy import inspect
from app.db.base import Base
from app.models import *  # noqa: F401,F403

revision="0001_initial_schema"
down_revision=None
branch_labels=None
depends_on=None
def upgrade():
    bind=op.get_bind()
    if not inspect(bind).get_table_names(): Base.metadata.create_all(bind=bind)
def downgrade():
    Base.metadata.drop_all(bind=op.get_bind())
