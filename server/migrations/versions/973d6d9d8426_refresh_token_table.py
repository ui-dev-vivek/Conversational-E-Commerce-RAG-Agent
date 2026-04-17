"""refresh token table

Revision ID: 973d6d9d8426
Revises: d1feb8909148
Create Date: 2026-04-16 23:23:05.142791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '973d6d9d8426'
down_revision: Union[str, Sequence[str], None] = 'd1feb8909148'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
