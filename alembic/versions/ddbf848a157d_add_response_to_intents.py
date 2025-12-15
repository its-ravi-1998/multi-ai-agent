"""add response to intents

Revision ID: ddbf848a157d
Revises: 88e23b00af44
Create Date: 2025-12-12 13:27:00.521249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddbf848a157d'
down_revision: Union[str, Sequence[str], None] = '88e23b00af44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("intents", sa.Column("response", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("intents", "response")
