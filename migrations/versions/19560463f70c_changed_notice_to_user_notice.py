# pylint: skip-file

"""Changed Notice to User_Notice.

Revision ID: 19560463f70c
Revises: 0a3d1a8b7316
Create Date: 2024-05-02 23:59:59.656013

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "19560463f70c"
down_revision = "0a3d1a8b7316"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_notice",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("subject", sa.String(length=100), nullable=False),
        sa.Column("content", sa.String(length=1000), nullable=True),
        sa.Column(
            "module",
            sa.Enum(
                "SYSTEM",
                "USER",
                "POST",
                "COMMENT",
                "REPLY",
                "LIKE",
                "FOLLOW",
                "SAVE",
                "COMMUNITY",
                name="usernoticemoduleenum",
            ),
            nullable=True,
        ),
        sa.Column("status", sa.Boolean(), nullable=True),
        sa.Column("create_at", sa.DateTime(), nullable=True),
        sa.Column("update_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name=op.f("fk_user_notice_user_id_user")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_notice")),
    )
    op.drop_table("notice")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notice",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("user_id", sa.VARCHAR(length=36), nullable=False),
        sa.Column("subject", sa.VARCHAR(length=100), nullable=False),
        sa.Column("content", sa.VARCHAR(length=1000), nullable=True),
        sa.Column("module", sa.VARCHAR(length=9), nullable=True),
        sa.Column("status", sa.BOOLEAN(), nullable=True),
        sa.Column("create_at", sa.DATETIME(), nullable=True),
        sa.Column("update_at", sa.DATETIME(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name="fk_notice_user_id_user"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_notice"),
    )
    op.drop_table("user_notice")
    # ### end Alembic commands ###
