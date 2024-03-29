"""Added account table

Revision ID: 64dbbbc564a9
Revises: e88bd3b19334
Create Date: 2023-07-18 14:23:40.858433

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '64dbbbc564a9'
down_revision = 'e88bd3b19334'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('anuncios_mantenimiento',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('anuncio_id', sa.String(length=100), nullable=True),
    sa.Column('fecha_creado', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.Column('asunto', sa.Text(), nullable=True),
    sa.Column('motivo', sa.Text(), nullable=True),
    sa.Column('accion', sa.Text(), nullable=True),
    sa.Column('cuerpo', sa.Text(), nullable=True),
    sa.Column('comunidad', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('tipo', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bancos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.Text(), nullable=True),
    sa.Column('titular_banco', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cartera_clientes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('tipo', sa.String(length=100), nullable=True),
    sa.Column('estado', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('clientes_wisphub',
    sa.Column('id_servicio', sa.Integer(), nullable=False),
    sa.Column('usuario', sa.Text(), nullable=True),
    sa.Column('nombre', sa.Text(), nullable=True),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('cedula', sa.Text(), nullable=True),
    sa.Column('direccion', sa.Text(), nullable=True),
    sa.Column('localidad', sa.Text(), nullable=True),
    sa.Column('ciudad', sa.Text(), nullable=True),
    sa.Column('telefono', sa.Text(), nullable=True),
    sa.Column('descuento', sa.Text(), nullable=True),
    sa.Column('saldo', sa.Text(), nullable=True),
    sa.Column('rfc', sa.Text(), nullable=True),
    sa.Column('informacion_adicional', sa.Text(), nullable=True),
    sa.Column('notificacion_sms', sa.Boolean(), nullable=True),
    sa.Column('aviso_pantalla', sa.Boolean(), nullable=True),
    sa.Column('notificaciones_push', sa.Boolean(), nullable=True),
    sa.Column('auto_activar_servicio', sa.Boolean(), nullable=True),
    sa.Column('firewall', sa.Boolean(), nullable=True),
    sa.Column('servicio', sa.Text(), nullable=True),
    sa.Column('password_servicio', sa.Text(), nullable=True),
    sa.Column('server_hotspot', sa.Text(), nullable=True),
    sa.Column('ip', sa.Text(), nullable=True),
    sa.Column('ip_local', sa.Text(), nullable=True),
    sa.Column('estado', sa.Text(), nullable=True),
    sa.Column('modelo_antena', sa.Text(), nullable=True),
    sa.Column('password_cpe', sa.Text(), nullable=True),
    sa.Column('mac_cpe', sa.Text(), nullable=True),
    sa.Column('interfaz_lan', sa.Text(), nullable=True),
    sa.Column('modelo_router_wifi', sa.Text(), nullable=True),
    sa.Column('ip_router_wifi', sa.Text(), nullable=True),
    sa.Column('mac_router_wifi', sa.Text(), nullable=True),
    sa.Column('usuario_router_wifi', sa.Text(), nullable=True),
    sa.Column('password_router_wifi', sa.Text(), nullable=True),
    sa.Column('ssid_router_wifi', sa.Text(), nullable=True),
    sa.Column('password_ssid_router_wifi', sa.Text(), nullable=True),
    sa.Column('comentarios', sa.Text(), nullable=True),
    sa.Column('coordenadas', sa.Text(), nullable=True),
    sa.Column('costo_instalacion', sa.Text(), nullable=True),
    sa.Column('precio_plan', sa.Text(), nullable=True),
    sa.Column('forma_contratacion', sa.Text(), nullable=True),
    sa.Column('sn_onu', sa.Text(), nullable=True),
    sa.Column('estado_facturas', sa.Text(), nullable=True),
    sa.Column('fecha_instalacion', sa.Text(), nullable=True),
    sa.Column('fecha_cancelacion', sa.Text(), nullable=True),
    sa.Column('fecha_corte', sa.Text(), nullable=True),
    sa.Column('ultimo_cambio', sa.Text(), nullable=True),
    sa.Column('sectorial', sa.Text(), nullable=True),
    sa.Column('plan_internet_id', sa.Integer(), nullable=True),
    sa.Column('plan_internet_nombre', sa.Text(), nullable=True),
    sa.Column('zona_id', sa.Integer(), nullable=True),
    sa.Column('zona_nombre', sa.Text(), nullable=True),
    sa.Column('router_id', sa.Integer(), nullable=True),
    sa.Column('router_nombre', sa.Text(), nullable=True),
    sa.Column('tecnico_id', sa.Float(), nullable=True),
    sa.Column('tecnico_nombre', sa.Text(), nullable=True),
    sa.Column('tecnico', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id_servicio')
    )
    op.create_table('configuraciones',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('key', sa.String(length=200), nullable=True),
    sa.Column('value', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('estado_cliente',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre_estado_cliente', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre_estado_cliente')
    )
    op.create_table('facturas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_factura', sa.Integer(), nullable=True),
    sa.Column('numero_factura', sa.String(length=150), nullable=True),
    sa.Column('cajero_wisphub', sa.String(length=150), nullable=True),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.Column('nombre_cliente', sa.String(length=200), nullable=True),
    sa.Column('fecha_pago', sa.Date(), nullable=True),
    sa.Column('estatus', sa.String(length=100), nullable=True),
    sa.Column('sub', sa.Float(), nullable=True),
    sa.Column('des', sa.Float(), nullable=True),
    sa.Column('saldo', sa.Float(), nullable=True),
    sa.Column('nuevo_saldo', sa.Float(), nullable=True),
    sa.Column('total_cobrado', sa.Float(), nullable=True),
    sa.Column('lote', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_factura')
    )
    op.create_table('metodos_de_pago',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tipo_pago', sa.Text(), nullable=True),
    sa.Column('metodo_pago', sa.Text(), nullable=True),
    sa.Column('simbolo', sa.Text(), nullable=True),
    sa.Column('longitud', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pais',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('paises',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('codigo', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('codigo'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('partidas_contables',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('partida', sa.String(length=200), nullable=True),
    sa.Column('subpartida', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permissions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('descripcion', sa.String(length=300), nullable=True),
    sa.Column('modulo', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('plan_conf_avanzado',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('reuso', sa.Integer(), nullable=True),
    sa.Column('limit_at_subida', sa.String(length=200), nullable=True),
    sa.Column('burst_limit_subida', sa.Float(), nullable=True),
    sa.Column('burst_threshold_sub', sa.String(length=200), nullable=True),
    sa.Column('burst_time_subida', sa.String(length=200), nullable=True),
    sa.Column('queue_type_subida', sa.String(length=200), nullable=True),
    sa.Column('parent', sa.String(length=200), nullable=True),
    sa.Column('address_list', sa.String(length=200), nullable=True),
    sa.Column('rules_sisprot', sa.String(length=200), nullable=True),
    sa.Column('limit_at_bajada', sa.String(length=200), nullable=True),
    sa.Column('burst_limit_bajada', sa.String(length=200), nullable=True),
    sa.Column('burst_threshold_baj', sa.String(length=200), nullable=True),
    sa.Column('burst_time_bajada', sa.String(length=200), nullable=True),
    sa.Column('queue_type_bajada', sa.String(length=200), nullable=True),
    sa.Column('prioridad', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plantillas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('mensaje', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('prospectos_pymes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre_completo', sa.String(length=300), nullable=True),
    sa.Column('apellido_completo', sa.String(length=300), nullable=True),
    sa.Column('cedula', sa.String(length=300), nullable=True),
    sa.Column('nombre_o_razon_social', sa.String(length=300), nullable=True),
    sa.Column('rif', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=300), nullable=True),
    sa.Column('telefono', sa.String(length=300), nullable=True),
    sa.Column('direccion_completa', sa.String(length=300), nullable=True),
    sa.Column('barrio_localidad', sa.String(length=300), nullable=True),
    sa.Column('plan_tentativo', sa.String(length=300), nullable=True),
    sa.Column('municipio', sa.String(length=300), nullable=True),
    sa.Column('otro_barrio_localidad', sa.String(length=300), nullable=True),
    sa.Column('latitud', sa.String(length=300), nullable=True),
    sa.Column('longitud', sa.String(length=300), nullable=True),
    sa.Column('fecha_nacimiento', sa.Date(), nullable=True),
    sa.Column('sexo', sa.String(length=50), nullable=True),
    sa.Column('foto_cedula', sa.String(length=200), nullable=True),
    sa.Column('foto_rif', sa.String(length=200), nullable=True),
    sa.Column('estado_vivienda', sa.String(length=300), nullable=True),
    sa.Column('parroquia', sa.String(length=300), nullable=True),
    sa.Column('sms', sa.String(length=50), nullable=True),
    sa.Column('whatsapp', sa.String(length=50), nullable=True),
    sa.Column('twitter', sa.String(length=50), nullable=True),
    sa.Column('facebook', sa.String(length=50), nullable=True),
    sa.Column('instagram', sa.String(length=50), nullable=True),
    sa.Column('fecha_hora_registro_sistema', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prospectos_residenciales',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre_completo', sa.String(length=300), nullable=True),
    sa.Column('apellido_completo', sa.String(length=300), nullable=True),
    sa.Column('cedula', sa.String(length=300), nullable=True),
    sa.Column('email', sa.String(length=300), nullable=True),
    sa.Column('telefono', sa.String(length=300), nullable=True),
    sa.Column('direccion_completa', sa.String(length=300), nullable=True),
    sa.Column('barrio_localidad', sa.String(length=300), nullable=True),
    sa.Column('plan_tentativo', sa.String(length=300), nullable=True),
    sa.Column('municipio', sa.String(length=300), nullable=True),
    sa.Column('otro_barrio_localidad', sa.String(length=300), nullable=True),
    sa.Column('latitud', sa.String(length=300), nullable=True),
    sa.Column('longitud', sa.String(length=300), nullable=True),
    sa.Column('fecha_nacimiento', sa.Date(), nullable=True),
    sa.Column('sexo', sa.String(length=50), nullable=True),
    sa.Column('foto_cedula', sa.String(length=200), nullable=True),
    sa.Column('foto_rif', sa.String(length=200), nullable=True),
    sa.Column('estado_vivienda', sa.String(length=300), nullable=True),
    sa.Column('parroquia', sa.String(length=300), nullable=True),
    sa.Column('sms', sa.String(length=50), nullable=True),
    sa.Column('whatsapp', sa.String(length=50), nullable=True),
    sa.Column('twitter', sa.String(length=50), nullable=True),
    sa.Column('facebook', sa.String(length=50), nullable=True),
    sa.Column('instagram', sa.String(length=50), nullable=True),
    sa.Column('fecha_hora_registro_sistema', sa.Date(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reportes_falla',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_falla', sa.Text(), nullable=True),
    sa.Column('nombre_cliente', sa.String(length=300), nullable=True),
    sa.Column('apellido_cliente', sa.String(length=300), nullable=True),
    sa.Column('cedula_cliente', sa.String(length=300), nullable=True),
    sa.Column('barrio_localidad', sa.String(length=300), nullable=True),
    sa.Column('direccion_cliente', sa.String(length=300), nullable=True),
    sa.Column('telefono', sa.String(length=300), nullable=True),
    sa.Column('tipo_falla', sa.String(length=300), nullable=True),
    sa.Column('estado_reporte', sa.Integer(), nullable=True),
    sa.Column('comentario', sa.Text(), nullable=True),
    sa.Column('creacion_ticket', sa.DateTime(), nullable=True),
    sa.Column('cierre_ticket', sa.DateTime(), nullable=True),
    sa.Column('editado_por', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=200), nullable=True),
    sa.Column('permisos', postgresql.ARRAY(sa.String(length=200)), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('tasas_cambiaria',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tasa', sa.Float(), nullable=True),
    sa.Column('fecha', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasas_digital',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tasa', sa.Float(), nullable=True),
    sa.Column('fecha', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.Column('errors', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tipo_cliente',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre_tipo_cliente', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre_tipo_cliente')
    )
    op.create_table('agentes',
    sa.Column('id_agente', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.Column('nombres', sa.String(length=100), nullable=True),
    sa.Column('apellidos', sa.String(length=100), nullable=True),
    sa.Column('dni', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('telefono', sa.String(length=100), nullable=True),
    sa.Column('rol', sa.Text(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('rol_id', sa.Integer(), nullable=True),
    sa.Column('id_cartera', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_cartera'], ['cartera_clientes.id'], ),
    sa.PrimaryKeyConstraint('id_agente'),
    sa.UniqueConstraint('username')
    )
    op.create_table('estados',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('pais_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pais_id'], ['pais.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_plan', sa.Integer(), nullable=True),
    sa.Column('nombre_plan', sa.Text(), nullable=True),
    sa.Column('precio_plan', sa.Float(), nullable=True),
    sa.Column('velocidad_descarga', sa.String(length=100), nullable=True),
    sa.Column('velocidad_subida', sa.String(length=100), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('lote', sa.Integer(), nullable=True),
    sa.Column('recarga_por_mora', sa.Integer(), nullable=True),
    sa.Column('id_plan_conf_avanzado', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_plan_conf_avanzado'], ['plan_conf_avanzado.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_plan')
    )
    op.create_table('clientes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_cliente_wisphub', sa.Integer(), nullable=True),
    sa.Column('usuario_cliente', sa.Text(), nullable=True),
    sa.Column('nombre_cliente', sa.Text(), nullable=True),
    sa.Column('email_cliente', sa.String(length=100), nullable=True),
    sa.Column('plan_internet', sa.String(length=200), nullable=True),
    sa.Column('dni_cedula', sa.String(length=100), nullable=True),
    sa.Column('barrio_localidad', sa.Text(), nullable=True),
    sa.Column('comentarios', sa.Text(), nullable=True),
    sa.Column('ip_cliente', sa.String(length=100), nullable=True),
    sa.Column('direccion', sa.Text(), nullable=True),
    sa.Column('telefono', sa.String(length=100), nullable=True),
    sa.Column('descuento', sa.String(length=50), nullable=True),
    sa.Column('saldo', sa.Float(), nullable=True),
    sa.Column('fecha_instalacion', sa.Date(), nullable=True),
    sa.Column('fecha_cancelacion', sa.Date(), nullable=True),
    sa.Column('precio_plan', sa.Float(), nullable=True),
    sa.Column('lote', sa.Integer(), nullable=True),
    sa.Column('pais', sa.String(length=100), nullable=True),
    sa.Column('router', sa.String(length=100), nullable=True),
    sa.Column('estado_facturacion', sa.String(length=200), nullable=True),
    sa.Column('clave_6d', sa.String(length=300), nullable=True),
    sa.Column('fue_migrado', sa.Boolean(), nullable=True),
    sa.Column('wisphub_update', sa.Boolean(), nullable=True),
    sa.Column('id_plan', sa.Integer(), nullable=True),
    sa.Column('id_tipo_cliente', sa.Integer(), nullable=True),
    sa.Column('id_estado_cliente', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_estado_cliente'], ['estado_cliente.id'], ),
    sa.ForeignKeyConstraint(['id_plan'], ['planes.id'], ),
    sa.ForeignKeyConstraint(['id_tipo_cliente'], ['tipo_cliente.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_cliente_wisphub')
    )
    op.create_table('municipios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('estados_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['estados_id'], ['estados.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('potes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('num_referencia', sa.Text(), nullable=True),
    sa.Column('monto', sa.Float(), nullable=True),
    sa.Column('referencia_pago_sisprot', sa.String(length=100), nullable=True),
    sa.Column('fecha_pago_registrado_banco', sa.Date(), nullable=True),
    sa.Column('fecha_pago_registrado_agente', sa.Date(), nullable=True),
    sa.Column('id_metodo_pago', sa.Integer(), nullable=True),
    sa.Column('id_agente', sa.Integer(), nullable=True),
    sa.Column('id_banco', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_agente'], ['agentes.id_agente'], ),
    sa.ForeignKeyConstraint(['id_banco'], ['bancos.id'], ),
    sa.ForeignKeyConstraint(['id_metodo_pago'], ['metodos_de_pago.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rf_reportes_cerrados',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_reporte_falla', sa.Integer(), nullable=True),
    sa.Column('motivo_cierre', sa.String(length=300), nullable=True),
    sa.Column('comentario', sa.Text(), nullable=True),
    sa.Column('agente_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['agente_id'], ['agentes.id_agente'], ),
    sa.ForeignKeyConstraint(['id_reporte_falla'], ['reportes_falla.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rf_visitas_tecnicas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_reporte_falla', sa.Integer(), nullable=True),
    sa.Column('hora_inicio', sa.String(length=300), nullable=True),
    sa.Column('hora_fin', sa.String(length=300), nullable=True),
    sa.Column('dia_visita', sa.String(length=300), nullable=True),
    sa.Column('vlan_cliente', sa.String(length=300), nullable=True),
    sa.Column('url_google_map', sa.String(length=300), nullable=True),
    sa.Column('ip_cliente', sa.String(length=300), nullable=True),
    sa.Column('agente_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['agente_id'], ['agentes.id_agente'], ),
    sa.ForeignKeyConstraint(['id_reporte_falla'], ['reportes_falla.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parroquias',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('municipios_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['municipios_id'], ['municipios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reporte_de_pagos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('agente_id', sa.Integer(), nullable=True),
    sa.Column('fec_hor_registro_agente', sa.DateTime(), nullable=True),
    sa.Column('cliente_id', sa.Integer(), nullable=True),
    sa.Column('plan_id', sa.Integer(), nullable=True),
    sa.Column('numero_de_factura', sa.Text(), nullable=True),
    sa.Column('partida_id', sa.Integer(), nullable=True),
    sa.Column('numero_de_referencia', sa.Text(), nullable=True),
    sa.Column('fecha_de_pago', sa.DateTime(), nullable=True),
    sa.Column('metodo_de_pago', sa.String(length=200), nullable=True),
    sa.Column('monto', sa.Float(), nullable=True),
    sa.Column('nota', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['agente_id'], ['agentes.id_agente'], ),
    sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ),
    sa.ForeignKeyConstraint(['partida_id'], ['partidas_contables.id'], ),
    sa.ForeignKeyConstraint(['plan_id'], ['planes.id'], ),
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
    op.drop_table('reporte_de_pagos')
    op.drop_table('parroquias')
    op.drop_table('rf_visitas_tecnicas')
    op.drop_table('rf_reportes_cerrados')
    op.drop_table('potes')
    op.drop_table('municipios')
    op.drop_table('clientes')
    op.drop_table('planes')
    op.drop_table('estados')
    op.drop_table('agentes')
    op.drop_table('tipo_cliente')
    op.drop_table('tasks')
    op.drop_table('tasas_digital')
    op.drop_table('tasas_cambiaria')
    op.drop_table('roles')
    op.drop_table('reportes_falla')
    op.drop_table('prospectos_residenciales')
    op.drop_table('prospectos_pymes')
    op.drop_table('plantillas')
    op.drop_table('plan_conf_avanzado')
    op.drop_table('permissions')
    op.drop_table('partidas_contables')
    op.drop_table('paises')
    op.drop_table('pais')
    op.drop_table('metodos_de_pago')
    op.drop_table('facturas')
    op.drop_table('estado_cliente')
    op.drop_table('configuraciones')
    op.drop_table('clientes_wisphub')
    op.drop_table('cartera_clientes')
    op.drop_table('bancos')
    op.drop_table('anuncios_mantenimiento')
    # ### end Alembic commands ###
