"""Fix typo

Revision ID: 2a29fc0d064a
Revises: 0ab377d77b0d
Create Date: 2026-03-19 16:42:48.839718

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "2a29fc0d064a"
down_revision: Union[str, None] = "0ab377d77b0d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename acheived -> achieved
    op.alter_column(
        "reading_goal",
        "acheived",
        new_column_name="achieved",
        existing_type=sa.Boolean(),
        existing_nullable=False,
    )

    # Rename date_acheived -> date_achieved
    op.alter_column(
        "reading_goal",
        "date_acheived",
        new_column_name="date_achieved",
        existing_type=sa.DateTime(),
        existing_nullable=True,
    )


def downgrade() -> None:
    # Reverse: achieved -> acheived
    op.alter_column(
        "reading_goal",
        "achieved",
        new_column_name="acheived",
        existing_type=sa.Boolean(),
        existing_nullable=False,
    )

    # Reverse: date_achieved -> date_acheived
    op.alter_column(
        "reading_goal",
        "date_achieved",
        new_column_name="date_acheived",
        existing_type=sa.DateTime(),
        existing_nullable=True,
    )
