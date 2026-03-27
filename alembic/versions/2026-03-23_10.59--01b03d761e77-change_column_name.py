"""Change column name

Revision ID: 01b03d761e77
Revises: 2a29fc0d064a
Create Date: 2026-03-23 10:59:51.734888

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "01b03d761e77"
down_revision: Union[str, None] = "2a29fc0d064a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "reading_progress",
        "date",
        new_column_name="progress_date",
        existing_type=sa.Date(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "reading_progress",
        "progress_date",
        new_column_name="date",
        existing_type=sa.Date(),
        existing_nullable=False,
    )
