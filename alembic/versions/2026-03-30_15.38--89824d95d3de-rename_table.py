"""Rename table

Revision ID: 89824d95d3de
Revises: 01b03d761e77
Create Date: 2026-03-30 15:38:53.440429

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "89824d95d3de"
down_revision: Union[str, None] = "01b03d761e77"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("reading_goal", "reading_queue")


def downgrade() -> None:
    op.rename_table("reading_queue", "reading_goal")
