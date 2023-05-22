from datetime import datetime, date
from typing import List, TypeVar, Generic, Optional, Union

from pydantic import BaseModel
from pydantic import Field, validator, create_model
from pydantic.generics import GenericModel
from sqlalchemy.orm import Query

from sisprot.models import ReporteFalla


class UserAuthScheme(BaseModel):
    username: str
    password: str


class UserScheme(BaseModel):
    id_agente: str
    username: str
    email: str | None
    rol: str | None
    nombres: str | None
    apellidos: str | None
    dni: str | None
    email: str | None
    telefono: str | None
    rol: str | None
    last_login: datetime | None

    class Config:
        orm_mode = True


class UserAuthOutScheme(BaseModel):
    accessToken: str
    user: UserScheme


GenericResultsType = TypeVar("GenericResultsType")


class PaginatedResponseSchema(GenericModel, Generic[GenericResultsType]):
    pages: int
    total: int
    has_prev: bool
    has_next: bool
    pageSize: int
    data: List[GenericResultsType]

    class Config:
        orm_mode = True


class MetodoPagoInSchema(BaseModel):
    tipo_pago: str = Field(..., min_length=1)
    metodo_pago: str = Field(..., min_length=1)
    simbolo: str = Field(..., min_length=1)
    longitud: int = Field(..., gt=0)


class MetodoPagoOutSchema(MetodoPagoInSchema):
    id: int

    class Config:
        orm_mode = True


class BancoInSchema(BaseModel):
    nombre: str
    titular_banco: str


class BancoOutSchema(BancoInSchema):
    id: int

    class Config:
        orm_mode = True


class PoteInSchema(BaseModel):
    fecha_pago_registrado_banco: datetime | date
    num_referencia: str = Field(..., min_length=1)
    # referencia_pago_sisprot: str = Field(..., min_length=1)
    monto: float = Field(..., gt=0)
    id_metodo_pago: int
    id_banco: Optional[int]


class AgenteOutSchema(BaseModel):
    id_agente: str
    username: str

    class Config:
        orm_mode = True


class PoteOutSchema(PoteInSchema):
    id: int
    metodo_de_pago: MetodoPagoOutSchema
    agente: AgenteOutSchema | None
    banco: BancoOutSchema | None
    fecha_pago_registrado_agente: datetime | date
    referencia_pago_sisprot: str = Field(..., min_length=1)

    @validator("metodo_de_pago", "agente", pre=True)
    def evaluate_lazy_columns(cls, v):
        if isinstance(v, Query):
            return v.all()
        return v

    class Config:
        orm_mode = True


class ClienteInSchema(BaseModel):
    id_cliente_wisphub: int
    usuario_cliente: str = Field(..., min_length=1)  #
    nombre_cliente: str = Field(..., min_length=1)  #
    email_cliente: str = Field(None, min_length=1)  #
    # plan_internet: str = Field(..., min_length=1)  #
    dni_cedula: str = Field(None, min_length=1)  #
    barrio_localidad: str = Field(..., min_length=1)  #
    # tipo_cliente: str = Field(..., min_length=1)  #
    comentarios: str = Field(None, min_length=1)  #
    ip_cliente: str = Field(None, min_length=1)  #
    # estado_cliente: str = Field(..., min_length=1)  #
    direccion: str = Field(..., min_length=1)  #
    telefono: str = Field(..., min_length=1)  #
    descuento: str = Field(..., min_length=1)  #
    saldo: float = Field(None)
    # precio_plan: float = Field(None, gt=0)
    fecha_instalacion: date
    fecha_cancelacion: date = Field(None)
    estado_facturacion: str = None
    pais: str = None
    router: str = None
    id_plan: int
    id_tipo_cliente: int
    id_estado_cliente: int

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }

    @validator("fecha_instalacion", "fecha_cancelacion", pre=True)
    def time_validate(cls, v):
        if isinstance(v, (datetime, date)):
            return v
        return datetime.strptime(v, "%d/%m/%Y")


class ClienteOutSchema(ClienteInSchema):
    id: int
    lote: int
    id_plan: int = None
    id_tipo_cliente: int = None
    id_estado_cliente: int = None

    class Config:
        orm_mode = True


class ClientEditSchema(BaseModel):
    telefono: Union[str, None]
    email_cliente: Union[str, None]


class TasaCambiariaSchema(BaseModel):
    id: int
    fecha: datetime
    tasa: float


class TasaCambiariaInSchema(BaseModel):
    fecha: datetime
    tasa: float


class PlanInSchema(BaseModel):
    id_plan: int
    nombre_plan: str = Field(..., min_length=1)
    precio_plan: float
    velocidad_descarga: str = Field(..., min_length=1)
    velocidad_subida: str = Field(..., min_length=1)
    descripcion: str = Field(..., min_length=1)
    recarga_por_mora: int
    id_plan_conf_avanzado: int = None


class PlanOutSchema(PlanInSchema):
    id: int
    lote: int
    descarga: str = None
    subida: str = None


class FacturaInSchema(BaseModel):
    id_factura: int
    numero_factura: str = Field(..., min_length=1)
    cajero_wisphub: str = Field(..., min_length=1)
    id_usuario: int
    nombre_cliente: str = Field(..., min_length=1)
    fecha_pago: date
    estatus: str = Field(..., min_length=1)
    sub: float
    des: float
    saldo: float
    nuevo_saldo: float
    total_cobrado: float


class FacturaOutSchema(FacturaInSchema):
    id: int
    lote: int


class PartidaContableInSchema(BaseModel):
    partida: str = Field(..., min_length=4)
    subpartida: str = Field(..., min_length=4)


class PartidaContableOutSchema(PartidaContableInSchema):
    id: int


class ReportePagoInSchema(BaseModel):
    cliente_id: int
    plan_id: int
    numero_de_factura: str = Field(..., min_length=1)
    partida_id: int
    numero_de_referencia: str = Field(..., min_length=1)
    fecha_de_pago: datetime
    metodo_de_pago: str = Field(..., min_length=1)
    monto: float = Field(..., gt=0)
    nota: str = Field(None, min_length=1)


class ReportePagoOutSchema(ReportePagoInSchema):
    id: int
    agente_id: int
    fec_hora_registro_agente: datetime


class UpdateConfigKeySchema(BaseModel):
    key: str
    value: str


class FilterMessageSchema(BaseModel):
    router: Optional[List[str]] = None
    status: Optional[List[int]] = None,
    barrio_localidad: Optional[List[str]] = None,
    router: Optional[List[str]] = None,
    plan: Optional[List[str]] = None,
    estado_facturacion: Optional[List[str]] = None,
    precio_plan: Optional[List[float]] = None,
    tipo_cliente: Optional[List[int]] = None,


class MessageSchema(BaseModel):
    message: str = Field(None, min_length=1, max_length=6000)
    media: str = Field(None)
    template_id: int = Field(None)
    deliver_at: str = Field(None)
    enable_email: bool = False
    enable_whatsapp: bool = False
    filters: FilterMessageSchema


class PlantillaMensajeInSchema(BaseModel):
    nombre: str
    mensaje: str


class PlantillaMensajeOutSchema(PlantillaMensajeInSchema):
    id: int

    class Config:
        orm_mode = True


class DeviceSchema(BaseModel):
    id: str
    phone: str
    status: str
    queue: Optional[
        create_model("Queue", status=(str, ...), total=(int, ...), size=(int, ...))
    ]
    session: Optional[create_model("Session", status=(str, ...), operative=(bool, ...))]


class AnuncioMantenimientoInSchema(BaseModel):
    cliente_status: int
    asunto: str
    motivo: str
    accion: str
    # cuerpo: str
    comunidad: Union[List[str], None]


class AnuncioMantenimientoOutSchema(AnuncioMantenimientoInSchema):
    tipo: str
    anuncio_id: int
    cliente_status: str | None

    @validator("anuncio_id")
    def validate_anuncio_id(cls, val, values, **kwargs):
        prefix = "E" if values["tipo"] == "MANTENIMIENTO" else "F"
        return "{}{:05d}".format(prefix, val)


class EstadoClienteInSchema(BaseModel):
    nombre_estado_cliente: str


class EstadoClienteOutSchema(EstadoClienteInSchema):
    id: int


class TipoClienteInSchema(BaseModel):
    nombre_tipo_cliente: str


class TipoClienteOutSchema(TipoClienteInSchema):
    id: int


class PlanConfAvanzadoInSchema(BaseModel):
    reuso: int
    limit_at_subida: str
    burst_limit_subida: float
    burst_threshold_sub: str
    burst_time_subida: str
    queue_type_subida: str
    parent: str
    address_list: str
    rules_sisprot: str
    limit_at_bajada: str
    burst_limit_bajada: str
    burst_threshold_baj: str
    burst_time_bajada: str
    queue_type_bajada: str
    prioridad: str


class PlanConfAvanzadoOutSchema(BaseModel):
    id: int


class PlanCreateSchema(BaseModel):
    plan_conf_avanzado: PlanConfAvanzadoInSchema
    plan: PlanInSchema


class ProspectoResidencialesInSchema(BaseModel):
    nombre_completo: str
    apellido_completo: str
    cedula: str
    email: str
    telefono: str
    direccion_completa: str
    barrio_localidad: str
    plan_tentativo: str
    coordenadas: Optional[str]
    municipio: Optional[str]
    otro_barrio_localidad: Optional[str]
    latitud: Optional[str]
    longitud: Optional[str]


class ProspectoPymesInSchema(BaseModel):
    nombre_completo: str
    apellido_completo: str
    cedula: str
    email: str
    telefono: str
    direccion_completa: str
    barrio_localidad: str
    plan_tentativo: str
    coordenadas: Optional[str]
    municipio: Optional[str]
    otro_barrio_localidad: Optional[str]
    latitud: Optional[str]
    longitud: Optional[str]


class ReporteFallaInSchema(BaseModel):
    # nombre_cliente: str
    # apellido_cliente: str
    cedula_cliente: str
    # barrio_localidad: str
    # direccion_cliente: str
    # telefono: str
    comentario: Union[str, None]
    tipo_falla: str


class ReporteFallaOutSchema(BaseModel):
    id: int
    id_falla: str
    estado_reporte: int
    tipo_falla: str
    nombre_cliente: str
    cedula_cliente: str
    barrio_localidad: str
    direccion_cliente: str
    telefono: str

    # @validator("id_falla")
    # def validate_anuncio_id(cls, val, values, **kwargs):
    #     return "F{:05d}".format(int(val))


class ReporteFallaEstadoInSchema(BaseModel):
    estado: int

    #
    hora_inicio: Union[str, None]
    hora_fin: Union[str, None]
    dia_visita: Union[str, None]
    vlan_cliente: Union[str, None]
    url_google_map: Union[str, None]
    ip_cliente: Union[str, None]

    motivo_cierre: Union[str, None]
    comentario: Union[str, None]

    @validator(
        "hora_inicio",
        "hora_fin",
        "dia_visita",
        "vlan_cliente",
        "url_google_map",
        "ip_cliente",
        pre=True,
        always=True,
    )
    def validate_exist(cls, v, values):
        if values["estado"] in [
            ReporteFalla.VISITA_AGENDADA,
            ReporteFalla.VISITA_REPROGRAMADA,
        ]:
            if v is None:
                raise ValueError("field required")
            else:
                return v

    @validator("motivo_cierre", "comentario", pre=True, always=True)
    def validate_reporte_cerrado(cls, v, values):
        if values["estado"] == ReporteFalla.CERRADO:
            if v is None:
                raise ValueError("field required")
            else:
                return v


class UserCreateSchema(BaseModel):
    username: str
    password_hash: str
    nombres: str
    apellidos: str
    dni: str
    email: Optional[str]
    telefono: Optional[str]
    rol_id: int


class CarteraInSchema(BaseModel):
    nombre: str
    tipo: str
    estado: str


class AnalistaUserInSchema(UserCreateSchema):
    cartera: CarteraInSchema


class RolOutSchema(BaseModel):
    nombre: str
    permisos: Optional[List[str]]

    class Config:
        orm_mode = True
