from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Column,
    Integer,
    Text,
    String,
    Date,
    Float,
    ForeignKey,
)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from sisprot.db import BaseModel
from .auth import UserAuth


class Pote(BaseModel):
    __tablename__ = "potes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    num_referencia = Column(Text)
    monto = Column(Float)
    referencia_pago_sisprot = Column(String(100))

    fecha_pago_registrado_banco = Column(Date)
    fecha_pago_registrado_agente = Column(Date)

    id_metodo_pago = Column(Integer, ForeignKey("metodos_de_pago.id"), nullable=True)
    id_agente = Column(Integer, ForeignKey("agentes.id_agente"), nullable=True)
    id_banco = Column(Integer, ForeignKey("bancos.id"), nullable=True)
    agente = relationship(UserAuth)
    metodo_de_pago = relationship("MetodoPago", back_populates="potes", lazy="subquery")
    banco = relationship("Banco", back_populates="potes", lazy="subquery")


class MetodoPago(BaseModel):
    __tablename__ = "metodos_de_pago"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_pago = Column(Text)
    metodo_pago = Column(Text)
    simbolo = Column(Text)
    longitud = Column(Integer)
    potes = relationship("Pote", back_populates="metodo_de_pago")


class TipoCliente(BaseModel):
    __tablename__ = "tipo_cliente"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo_cliente = Column(Text, unique=True)


class EstadoCliente(BaseModel):
    __tablename__ = "estado_cliente"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_estado_cliente = Column(Text, unique=True)


class Cliente(BaseModel):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente_wisphub = Column(Integer, unique=True)  # id_usuario
    usuario_cliente = Column(Text)  # usuario
    nombre_cliente = Column(Text)  # nombre
    email_cliente = Column(String(100))  # email
    plan_internet = Column(String(200))  #
    dni_cedula = Column(String(100))  # dni
    barrio_localidad = Column(Text)  #
    # tipo_cliente = Column(String(100))  #
    comentarios = Column(Text)  #
    ip_cliente = Column(String(100))  # ip_cliente
    # estado_cliente = Column(String(200))  #
    direccion = Column(Text)  #
    telefono = Column(String(100))  #
    descuento = Column(String(50))  #
    saldo = Column(Float)  #
    fecha_instalacion = Column(Date)  #
    fecha_cancelacion = Column(Date)  #
    precio_plan = Column(Float)
    lote = Column(Integer, default=1)
    pais = Column(String(100))
    router = Column(String(100))
    estado_facturacion = Column(String(200))
    clave_6d = Column(String(300))
    fue_migrado = Column(Boolean, default=False, nullable=True)
    wisphub_update = Column(Boolean, default=False, nullable=True)
    country = relationship("Pais", primaryjoin="foreign(Cliente.pais) == Pais.nombre")

    id_plan = Column(Integer, ForeignKey("planes.id"))
    plan = relationship("Plan")

    id_tipo_cliente = Column(Integer, ForeignKey("tipo_cliente.id"))
    tipo_cliente = relationship("TipoCliente")

    id_estado_cliente = Column(Integer, ForeignKey("estado_cliente.id"))
    estado_cliente = relationship("EstadoCliente")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class TasaCambiaria(BaseModel):
    __tablename__ = "tasas_cambiaria"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tasa = Column(Float)
    fecha = Column(DateTime)


class PlanConfAvanzado(BaseModel):
    __tablename__ = "plan_conf_avanzado"
    id = Column(Integer, primary_key=True, autoincrement=True)
    reuso = Column(Integer)
    limit_at_subida = Column(String(200))
    burst_limit_subida = Column(Float)
    burst_threshold_sub = Column(String(200))
    burst_time_subida = Column(String(200))
    queue_type_subida = Column(String(200))
    parent = Column(String(200))
    address_list = Column(String(200))
    rules_sisprot = Column(String(200))
    limit_at_bajada = Column(String(200))
    burst_limit_bajada = Column(String(200))
    burst_threshold_baj = Column(String(200))
    burst_time_bajada = Column(String(200))
    queue_type_bajada = Column(String(200))
    prioridad = Column(String(200))


class Plan(BaseModel):
    __tablename__ = "planes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_plan = Column(Integer, unique=True)
    nombre_plan = Column(Text)
    precio_plan = Column(Float)
    velocidad_descarga = Column(String(100))
    velocidad_subida = Column(String(100))
    descripcion = Column(Text)
    lote = Column(Integer, default=1)
    recarga_por_mora = Column(Integer)
    id_plan_conf_avanzado = Column(Integer, ForeignKey("plan_conf_avanzado.id"))
    plan_conf_avanzado = relationship("PlanConfAvanzado")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Factura(BaseModel):
    __tablename__ = "facturas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_factura = Column(Integer, unique=True)
    numero_factura = Column(String(150))
    cajero_wisphub = Column(String(150))
    id_usuario = Column(Integer)
    nombre_cliente = Column(String(200))
    fecha_pago = Column(Date)
    estatus = Column(String(100))
    sub = Column(Float)
    des = Column(Float)
    saldo = Column(Float)
    nuevo_saldo = Column(Float)
    total_cobrado = Column(Float)
    lote = Column(Integer, default=1)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class TasaDigital(BaseModel):
    __tablename__ = "tasas_digital"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tasa = Column(Float)
    fecha = Column(Date)


class PartidaContable(BaseModel):
    __tablename__ = "partidas_contables"
    id = Column(Integer, primary_key=True, autoincrement=True)
    partida = Column(String(200))
    subpartida = Column(String(200))


class ReportePago(BaseModel):
    __tablename__ = "reporte_de_pagos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    agente_id = Column(Integer, ForeignKey("agentes.id_agente"), nullable=True)
    fec_hor_registro_agente = Column(DateTime)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    plan_id = Column(Integer, ForeignKey("planes.id"), nullable=True)
    numero_de_factura = Column(Text)
    partida_id = Column(Integer, ForeignKey("partidas_contables.id"), nullable=True)
    numero_de_referencia = Column(Text)
    fecha_de_pago = Column(DateTime)
    metodo_de_pago = Column(String(200))
    monto = Column(Float)
    nota = Column(Text)

    plan = relationship("Plan")
    partida_contable = relationship("PartidaContable")
    agente = relationship(UserAuth)


class Configuracion(BaseModel):
    __tablename__ = "configuraciones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(200))
    value = Column(String(300))


class Banco(BaseModel):
    __tablename__ = "bancos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Text)
    titular_banco = Column(Text)
    potes = relationship("Pote", back_populates="banco")


class PlantillaMensaje(BaseModel):
    __tablename__ = "plantillas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True)
    mensaje = Column(Text)


class Pais(BaseModel):
    __tablename__ = "paises"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True)
    codigo = Column(String(100), unique=True)


class AnuncioMantenimiento(BaseModel):
    __tablename__ = "anuncios_mantenimiento"
    id = Column(Integer, primary_key=True, autoincrement=True)
    anuncio_id = Column(String(100))
    fecha_creado = Column(DateTime, default=datetime.now)
    status = Column(String(100))
    asunto = Column(Text)
    motivo = Column(Text)
    accion = Column(Text)
    cuerpo = Column(Text)
    comunidad = Column(ARRAY(String))
    tipo = Column(String(100))


class Task(BaseModel):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(100))
    errors = Column(Text)
    created_at = Column(DateTime, default=datetime.now)


class ProspectosResidenciales(BaseModel):
    __tablename__ = "prospectos_residenciales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_completo = Column(String(300))
    apellido_completo = Column(String(300))
    cedula = Column(String(300))
    email = Column(String(300))
    telefono = Column(String(300))
    direccion_completa = Column(String(300))
    barrio_localidad = Column(String(300))
    plan_tentativo = Column(String(300))
    municipio = Column(String(300))
    otro_barrio_localidad = Column(String(300))
    latitud = Column(String(300))
    longitud = Column(String(300))
    fecha_nacimiento = Column(Date)
    sexo = Column(String(50))
    foto_cedula = Column(String(200))
    foto_rif = Column(String(200))
    estado_vivienda = Column(String(300))
    parroquia = Column(String(300))
    sms = Column(String(50))
    whatsapp = Column(String(50))
    twitter = Column(String(50))
    facebook = Column(String(50))
    instagram = Column(String(50))
    fecha_hora_registro_sistema = Column(Date, nullable=True, server_default=func.now())


class ProspectosPymes(BaseModel):
    __tablename__ = "prospectos_pymes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_completo = Column(String(300))
    apellido_completo = Column(String(300))
    cedula = Column(String(300))
    nombre_o_razon_social = Column(String(300))
    rif = Column(String(50))
    email = Column(String(300))
    telefono = Column(String(300))
    direccion_completa = Column(String(300))
    barrio_localidad = Column(String(300))
    plan_tentativo = Column(String(300))
    municipio = Column(String(300))
    otro_barrio_localidad = Column(String(300))
    latitud = Column(String(300))
    longitud = Column(String(300))
    fecha_nacimiento = Column(Date)
    sexo = Column(String(50))
    foto_cedula = Column(String(200))
    foto_rif = Column(String(200))
    estado_vivienda = Column(String(300))
    parroquia = Column(String(300))
    sms = Column(String(50))
    whatsapp = Column(String(50))
    twitter = Column(String(50))
    facebook = Column(String(50))
    instagram = Column(String(50))
    fecha_hora_registro_sistema = Column(
        DateTime, nullable=True, server_default=func.now()
    )


class ReporteFalla(BaseModel):
    __tablename__ = "reportes_falla"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_falla = Column(Text)
    nombre_cliente = Column(String(300))
    apellido_cliente = Column(String(300))
    cedula_cliente = Column(String(300))
    barrio_localidad = Column(String(300))
    direccion_cliente = Column(String(300))
    telefono = Column(String(300))
    tipo_falla = Column(String(300))
    estado_reporte = Column(Integer, default=1)
    comentario = Column(Text)

    creacion_ticket = Column(DateTime, default=datetime.now)
    cierre_ticket = Column(DateTime)
    editado_por = Column(String(300))

    ABIERTO = 1
    VISITA_AGENDADA = 2
    VISITA_REPROGRAMADA = 3
    CERRADO = 4


class VisitaTecnica(BaseModel):
    __tablename__ = "rf_visitas_tecnicas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_reporte_falla = Column(Integer, ForeignKey("reportes_falla.id"), nullable=True)
    hora_inicio = Column(String(300))
    hora_fin = Column(String(300))
    dia_visita = Column(String(300))
    vlan_cliente = Column(String(300), default="Desconocida/Renovar", nullable=True)
    url_google_map = Column(String(300), nullable=True)
    ip_cliente = Column(String(300))
    agente_id = Column(Integer, ForeignKey("agentes.id_agente"), nullable=True)


class ReporteCerrado(BaseModel):
    __tablename__ = "rf_reportes_cerrados"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_reporte_falla = Column(Integer, ForeignKey("reportes_falla.id"), nullable=True)
    motivo_cierre = Column(String(300))
    comentario = Column(Text)
    agente_id = Column(Integer, ForeignKey("agentes.id_agente"), nullable=True)


class CarteraCliente(BaseModel):
    __tablename__ = "cartera_clientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    tipo = Column(String(100))
    estado = Column(String(100))


class Paises(BaseModel):
    __tablename__ = "pais"
    id = Column(Integer, primary_key=True)
    name = Column(Text)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Estados(BaseModel):
    __tablename__ = "estados"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    pais_id = Column(Integer, ForeignKey("pais.id"))

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Municipios(BaseModel):
    __tablename__ = "municipios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)  # nombre
    estados_id = Column(Integer, ForeignKey("estados.id"))


class Parroquias(BaseModel):
    __tablename__ = "parroquias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    municipios_id = Column(Integer, ForeignKey("municipios.id"))


class Comunidades(BaseModel):
    __tablename__ = "comunidades"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)  # nombre
    parroquias_id = Column(Integer, ForeignKey("parroquias.id"))


"""
Modelos de base de datos raw para wishphub
"""


class ClienteWisphub(BaseModel):
    __tablename__ = "clientes_wisphub"
    id_servicio = Column(Integer, primary_key=True)
    usuario = Column(Text)
    nombre = Column(Text)
    email = Column(Text)
    cedula = Column(Text)
    direccion = Column(Text)
    localidad = Column(Text)
    ciudad = Column(Text)
    telefono = Column(Text)
    descuento = Column(Text)
    saldo = Column(Text)
    rfc = Column(Text)
    informacion_adicional = Column(Text)
    notificacion_sms = Column(Boolean, default=False, nullable=True)
    aviso_pantalla = Column(Boolean, default=False, nullable=True)
    notificaciones_push = Column(Boolean, default=False, nullable=True)
    auto_activar_servicio = Column(Boolean, default=False, nullable=True)
    firewall = Column(Boolean, default=False, nullable=True)
    servicio = Column(Text)
    password_servicio = Column(Text)
    server_hotspot = Column(Text)
    ip = Column(Text)
    ip_local = Column(Text)
    estado = Column(Text)
    modelo_antena = Column(Text)
    password_cpe = Column(Text)
    mac_cpe = Column(Text)
    interfaz_lan = Column(Text)
    modelo_router_wifi = Column(Text)
    ip_router_wifi = Column(Text)
    mac_router_wifi = Column(Text)
    usuario_router_wifi = Column(Text)
    password_router_wifi = Column(Text)
    ssid_router_wifi = Column(Text)
    password_ssid_router_wifi = Column(Text)
    comentarios = Column(Text)
    coordenadas = Column(Text)
    costo_instalacion = Column(Text)
    precio_plan = Column(Text)
    forma_contratacion = Column(Text)
    sn_onu = Column(Text)
    estado_facturas = Column(Text)
    fecha_instalacion = Column(Text)
    fecha_cancelacion = Column(Text)
    fecha_corte = Column(Text)
    ultimo_cambio = Column(Text)
    sectorial = Column(Text)
    plan_internet_id = Column(Integer, unique=False)
    plan_internet_nombre = Column(Text)
    zona_id = Column(Integer, unique=False)
    zona_nombre = Column(Text)
    router_id = Column(Integer, unique=False)
    router_nombre = Column(Text)
    tecnico_id = Column(Float)
    tecnico_nombre = Column(Text)
    tecnico = Column(Float)
