from datetime import datetime
import logging
from pydantic import ValidationError
import requests
from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sisprot.db import get_db
from sisprot.auth import jwt_required, get_current_user
from sisprot.models import ReporteFalla, Cliente, VisitaTecnica, ReporteCerrado
from sisprot.schemas import (
    ReporteFallaInSchema,
    PaginatedResponseSchema,
    ReporteFallaEstadoInSchema,
    ReporteFallaOutSchema,
)
from sisprot.utils import config
from sisprot.messages import (
    VISITA_AGENDADA_MSG,
    VISITA_AGENDADA_GRUPO_MSG,
    VISITA_REPROGRAMADA_MSG,
    VISITA_REPROGRAMADA_GRUPO_MSG,
    REPORTE_CERRADO_MSG,
    REPORTE_CERRADO_GROUP_MSG,
)


msg_template1 = """✅ Hemos recibido tu reporte de falla con exito 🎉

👋 Hola, estimado (a) {nombre_cliente} de la comunidad {barrio_localidad}

📢 Queremos notificar que hemos recibido el reporte de falla que acabas de realizar, este es el código que entregarás a atención al cliente para poder hacerle seguimiento a tu casa {id_falla}.

En Sisprot Global Fiber, nos preocupamos porque nuestros clientes tengan un servicio estable y de calidad, pedimos disculpas de antemano por las molestias causadas y ya estamos trabajando para solucionar el problema que presentas en tu hogar/empresa.

Te pedimos un poco de paciencia, ya que dentro de poco nos pondremos en contacto contigo para realizar una asistencia remota o agendar una visita técnica de ser necesario

"""

msg_template2 = """📢 *Reporte de Falla* {id_falla}
- - - - - - - - - - - - - - - - - - - -
 👤 *Datos del cliente:*

*Nombre y Apellido*
{nombre_cliente}

*Cédula de Identidad*
{cedula_cliente}

*Barrio/Localidad]*
{barrio_localidad}

*Dirección Completa*
{direccion_cliente}

*Número de Teléfono*
{telefono}
- - - - - - - - - - - - - - - - - - - -
🧰 *Datos de la Falla:*

*Tipo de Falla*
{tipo_falla}

*Comentario*
{comentario}

*Esta falla fue reportada el día {dia_reporte}*

"""


router = APIRouter(prefix="/api")


@router.get(
    "/reporte-falla",
    tags=["reporte-fallos"],
    response_model=PaginatedResponseSchema[ReporteFallaOutSchema],
)
def index(
    page: int = 1, session=Depends(get_db), current_user=Depends(get_current_user)
):
    """
    Devuelve una lista paginada de reportes de fallas
    """
    stmt = session.query(ReporteFalla)
    results = stmt.paginate(page=page).as_dict()
    return results


@router.get("/reporte-falla/{id}", tags=["reporte-fallos"])
def index(id: int, session=Depends(get_db), current_user=Depends(get_current_user)):
    """
    Devuelve una lista paginada de reportes de fallas
    """
    result = session.query(ReporteFalla).filter_by(id=id).first()
    return result


@router.post("/reporte-falla", tags=["reporte-fallos"])
def create(data: ReporteFallaInSchema, session=Depends(get_db)):
    """
    Crea un reporte de fallo
    """

    cliente = (
        session.query(Cliente).filter(Cliente.dni_cedula == data.cedula_cliente).first()
    )

    if not cliente:
        raise HTTPException(
            status_code=400,
            detail="Usted no se encuentra registrado en nuestro sistema",
        )

    max_id = session.query(func.max(ReporteFalla.id)).scalar()
    
    obj = {
        "nombre_cliente": cliente.nombre_cliente,
        "barrio_localidad": cliente.barrio_localidad,
        "direccion_cliente": cliente.direccion,
        "cedula_cliente": cliente.dni_cedula,
        "telefono": cliente.telefono,
    }

    item = ReporteFalla(**data.dict(exclude={"cedula_cliente"}), **obj)

    item.id_falla = int(max_id) + 1 if max_id is not None else 1

    id_falla = "F{:05d}".format(item.id_falla)

    item.id_falla = id_falla

    session.add(item)


    try:
        API_TOKEN = config(session, key="wiivo_api_token")
        headers = {"Content-Type": "application/json", "Token": API_TOKEN}
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y")

        # payload = {"group": "120363049087045640@g.us", "message": msg_template.format(**data.dict())}

        # Mensaje enviado al cliente

        for tlf in cliente.telefono.split(", "):
            payload = {
                "phone": "+58" + tlf,
                "message": msg_template1.format(
                    nombre_cliente=cliente.nombre_cliente,
                    id_falla=id_falla,
                ),
            }

            # print(payload)

            requests.post(
                "https://api.wiivo.net/v1/messages", json=payload, headers=headers
            )

        # Mensaje enviado al grupo
        # payload = {"phone": f"+{data.telefono}", "message": msg_to_user.format(nombre_cliente=data.nombre_completo, barrio_localidad=data.barrio_localidad)}

        payload = {
            "group": "120363087580536000@g.us",
            "message": msg_template2.format(
                **obj,
                id_falla=id_falla,
                dia_reporte=date_time,
                tipo_falla=data.tipo_falla,
                comentario=data.comentario,
            ),
        }

        # print(payload)

        requests.post(
            "https://api.wiivo.net/v1/messages", json=payload, headers=headers
        )
    except:
        logging.exception("error send msg")
        raise HTTPException(status_code=400, detail="No se pudo enviar el mensaje")

    session.commit()


@router.put(
    "/reporte-falla/{id}/estado",
    tags=["reporte-fallos"],
)
def change_status(
    id: int,
    data: ReporteFallaEstadoInSchema,
    session=Depends(get_db),
    current_user=Depends(get_current_user),
):
    item = session.query(ReporteFalla).filter_by(id=id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Reporte de falla no encontrado")

    if item.estado_reporte == ReporteFalla.CERRADO:
        raise HTTPException(
            status_code=400, detail="El estado del reporte no se encuentra abierto"
        )

    if data.estado in [ReporteFalla.VISITA_AGENDADA, ReporteFalla.VISITA_REPROGRAMADA]:
        item.estado_reporte = (
            ReporteFalla.VISITA_AGENDADA
            if item.estado_reporte == ReporteFalla.VISITA_AGENDADA
            else ReporteFalla.VISITA_REPROGRAMADA
        )
        item.editado_por = current_user.username

        API_TOKEN = config(session, key="wiivo_api_token")
        headers = {"Content-Type": "application/json", "Token": API_TOKEN}

        visita = VisitaTecnica(
            **data.dict(
                include={
                    "hora_inicio",
                    "hora_fin",
                    "dia_visita",
                    "vlan_cliente",
                    "url_google_map",
                    "ip_cliente",
                }
            ),
            id_reporte_falla=item.id,
            agente_id=current_user.id_agente,
        )

        if data.estado == ReporteFalla.VISITA_AGENDADA:
            msg = VISITA_AGENDADA_MSG
            msg_group = VISITA_AGENDADA_GRUPO_MSG
        else:
            msg = VISITA_REPROGRAMADA_MSG
            msg_group = VISITA_REPROGRAMADA_GRUPO_MSG

        msg = msg.format(
            nombre_cliente=item.nombre_cliente,
            dia_visita=data.dia_visita,
            id_falla=item.id_falla,
        )

        try:
            for tlf in item.telefono.split(", "):
                payload = {
                    "phone": "+58" + tlf,
                    "message": msg,
                }
                # print(payload)
                requests.post(
                    "https://api.wiivo.net/v1/messages", json=payload, headers=headers
                )

            msg_group = msg_group.format(
                **data.dict(),
                id_falla=item.id_falla,
                nombre_agente=current_user.nombres,
                nombre_cliente=item.nombre_cliente,
                barrio_localidad=item.barrio_localidad,
            )
            payload = {
                "group": "120363104574594712@g.us",
                "message": msg_group,
            }

            # print(payload)

            requests.post(
                "https://api.wiivo.net/v1/messages", json=payload, headers=headers
            )
        except:
            logging.exception("error al enviar mensaje de visita agendada")
            raise HTTPException(
                status_code=400, detail="Error al enviar mensaje de visita agendada"
            )

        session.add(visita)
    elif data.estado == ReporteFalla.CERRADO and item.estado_reporte in [
        ReporteFalla.ABIERTO,
        ReporteFalla.VISITA_AGENDADA,
        ReporteFalla.VISITA_REPROGRAMADA,
    ]:
        item.estado_reporte = ReporteFalla.CERRADO
        item.cierre_ticket = datetime.now()
        item.editado_por = current_user.username

        reporte_cerrado = ReporteCerrado(
            id_reporte_falla=item.id,
            agente_id=current_user.id_agente,
            motivo_cierre=data.motivo_cierre,
            comentario=data.comentario,
        )
        session.add(reporte_cerrado)

        msg = REPORTE_CERRADO_MSG.format(
            nombre_cliente=item.nombre_cliente,
            motivo_cierre=data.motivo_cierre,
            comentario=data.comentario,
            id_falla=item.id_falla,
        )

        API_TOKEN = config(session, key="wiivo_api_token")
        headers = {"Content-Type": "application/json", "Token": API_TOKEN}

        try:
            for tlf in item.telefono.split(", "):
                payload = {
                    "phone": "+58" + tlf,
                    "message": msg,
                }
                # print(payload)
                requests.post(
                    "https://api.wiivo.net/v1/messages", json=payload, headers=headers
                )

            msg_group = REPORTE_CERRADO_GROUP_MSG.format(
                **data.dict(),
                id_falla=item.id_falla,
                nombre_agente=current_user.nombres,
                nombre_cliente=item.nombre_cliente,
                barrio_localidad=item.barrio_localidad,
            )

            payload = {
                "group": "120363086024394407@g.us",
                "message": msg_group,
            }

            # print(payload)

            requests.post(
                "https://api.wiivo.net/v1/messages", json=payload, headers=headers
            )
        except:
            logging.exception("error al enviar mensaje de visita agendada")
            raise HTTPException(
                status_code=400, detail="Error al enviar mensaje de visita agendada"
            )

    session.commit()
