"""empty message

Revision ID: 0e433acf5a12
Revises: 0378b8b1231f
Create Date: 2022-03-03 22:28:13.445127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e433acf5a12'
down_revision = '0378b8b1231f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type_name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('article', sa.Column('type_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'article', 'article_type', ['type_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'article', type_='foreignkey')
    op.drop_column('article', 'type_id')
    op.drop_table('article_type')
    # ### end Alembic commands ###