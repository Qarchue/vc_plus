"""使用者資料表

Revision ID: 211d2f15aed3
Revises: 5a2e6f307bc1
Create Date: 2024-11-14 12:14:22.485682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '211d2f15aed3'
down_revision: Union[str, None] = '5a2e6f307bc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_server_data',
        sa.Column('discord_id', sa.Integer(), sa.ForeignKey('users.discord_id'), nullable=False),
        sa.Column('servers_id', sa.Integer(), sa.ForeignKey('servers.server_id'), nullable=False),
        sa.Column('data', sa.JSON(), nullable=True),
        sa.Column('settings', sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('user_server_data')