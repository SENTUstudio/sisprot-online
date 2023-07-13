"""Agregando nueva estructura de datos geografico con tablas vacias

Revision ID: 6b7f104859f6
Revises: c3288d96e028
Create Date: 2023-06-07 14:49:42.601449

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b7f104859f6'
down_revision = 'c3288d96e028'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('estados',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('pais_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pais_id'], ['pais.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('municipios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('estados_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['estados_id'], ['estados.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parroquias',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('municipios_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['municipios_id'], ['municipios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comunidades',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('parroquias_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parroquias_id'], ['parroquias.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comunidades')
    op.drop_table('parroquias')
    op.drop_table('municipios')
    op.drop_table('estados')
    # ### end Alembic commands ###