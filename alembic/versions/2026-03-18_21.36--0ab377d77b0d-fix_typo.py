"""Fix typo

Revision ID: 0ab377d77b0d
Revises: b9cfc9de43f1
Create Date: 2026-03-18 21:36:53.053094

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0ab377d77b0d"
down_revision: Union[str, None] = "b9cfc9de43f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "reading_goal",
        "achieved",
        new_column_name="acheived",
        existing_type=sa.Boolean(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "reading_goal",
        "acheived",
        new_column_name="achieved",
        existing_type=sa.Boolean(),
        existing_nullable=False,
    )
