"""Primer registro

Revision ID: 53ca25326202
Revises: 
Create Date: 2023-06-03 19:49:33.302087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53ca25326202'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'agentes', 'cartera_clientes', ['id_cartera'], ['id'])
    op.drop_constraint('tipo_cliente_fk', 'clientes', type_='foreignkey')
    op.create_foreign_key(None, 'clientes', 'planes', ['id_plan'], ['id'])
    op.create_foreign_key(None, 'clientes', 'tipo_cliente', ['id_tipo_cliente'], ['id'])
    op.drop_column('clientes', 'estado_cliente')
    op.drop_column('clientes', 'tipo_cliente')
    op.add_column('prospectos_pymes', sa.Column('sms', sa.String(length=50), nullable=True))
    op.add_column('prospectos_pymes', sa.Column('whatsapp', sa.String(length=50), nullable=True))
    op.add_column('prospectos_pymes', sa.Column('twitter', sa.String(length=50), nullable=True))
    op.add_column('prospectos_pymes', sa.Column('facebook', sa.String(length=50), nullable=True))
    op.add_column('prospectos_pymes', sa.Column('instagram', sa.String(length=50), nullable=True))
    op.add_column('prospectos_residenciales', sa.Column('sms', sa.String(length=50), nullable=True))
    op.add_column('prospectos_residenciales', sa.Column('whatsapp', sa.String(length=50), nullable=True))
    op.add_column('prospectos_residenciales', sa.Column('twitter', sa.String(length=50), nullable=True))
    op.add_column('prospectos_residenciales', sa.Column('facebook', sa.String(length=50), nullable=True))
    op.add_column('prospectos_residenciales', sa.Column('instagram', sa.String(length=50), nullable=True))
    op.create_foreign_key(None, 'reporte_de_pagos', 'planes', ['plan_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reporte_de_pagos', type_='foreignkey')
    op.drop_column('prospectos_residenciales', 'instagram')
    op.drop_column('prospectos_residenciales', 'facebook')
    op.drop_column('prospectos_residenciales', 'twitter')
    op.drop_column('prospectos_residenciales', 'whatsapp')
    op.drop_column('prospectos_residenciales', 'sms')
    op.drop_column('prospectos_pymes', 'instagram')
    op.drop_column('prospectos_pymes', 'facebook')
    op.drop_column('prospectos_pymes', 'twitter')
    op.drop_column('prospectos_pymes', 'whatsapp')
    op.drop_column('prospectos_pymes', 'sms')
    op.add_column('clientes', sa.Column('tipo_cliente', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('clientes', sa.Column('estado_cliente', sa.VARCHAR(length=200), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'clientes', type_='foreignkey')
    op.drop_constraint(None, 'clientes', type_='foreignkey')
    op.create_foreign_key('tipo_cliente_fk', 'clientes', 'tipo_cliente', ['id_tipo_cliente'], ['id'], ondelete='SET NULL')
    op.drop_constraint(None, 'agentes', type_='foreignkey')
    # ### end Alembic commands ###