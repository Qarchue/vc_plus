"""增加伺服器table

Revision ID: 5a2e6f307bc1
Revises: 6a7998d26ae6
Create Date: 2024-10-18 17:25:31.431313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a2e6f307bc1'
down_revision: Union[str, None] = '6a7998d26ae6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "servers",
        sa.Column("server_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("server_id"),
    )
    



    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("servers")

    # ### end Alembic commands ###
