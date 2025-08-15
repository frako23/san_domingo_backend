"""Primera migración con enum

Revision ID: fd5e64842429
Revises: 
Create Date: 2025-08-15 08:52:07.850521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd5e64842429'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Crear el tipo ENUM en PostgreSQL
    op.execute("CREATE TYPE coffeeflavor AS ENUM ('vainilla', 'chocolate', 'galleta', 'avellana')")

    # Alterar la columna para usar el nuevo tipo ENUM
    op.execute("""
        ALTER TABLE coffeetype
        ALTER COLUMN nombre TYPE coffeeflavor
        USING nombre::coffeeflavor
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Revertir la columna al tipo VARCHAR antes de eliminar el ENUM
    op.execute("""
        ALTER TABLE coffeetype
        ALTER COLUMN nombre TYPE VARCHAR
    """)

    # Eliminar el tipo ENUM
    op.execute("DROP TYPE coffeeflavor")
