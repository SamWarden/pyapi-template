"""Add the "uuid-ossp" extension

Revision ID: 0001
Revises:
Create Date: 2025-10-29 10:00:39.737781

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION "uuid-ossp"')


def downgrade() -> None:
    op.execute('DROP EXTENSION "uuid-ossp"')
