"""merge logo and dados bancarios

Revision ID: 52abe1f211ea
Revises: add_logo_escritorio, 4ca297d39855
Create Date: 2025-11-23 10:20:00.491443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52abe1f211ea'
down_revision = ('add_logo_escritorio', '4ca297d39855')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
