"""語音創建

Revision ID: 8c6b1a9fde79
Revises: 22226be4d55d
Create Date: 2024-11-19 15:11:35.257441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c6b1a9fde79'
down_revision: Union[str, None] = '22226be4d55d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'voice_channel',
        sa.Column('discord_id', sa.Integer(), sa.ForeignKey('users.discord_id'), nullable=False),
        sa.Column('servers_id', sa.Integer(), sa.ForeignKey('servers.server_id'), nullable=False),
        sa.Column('channel_id', sa.Integer(), nullable=True),

    )


def downgrade() -> None:
    pass
