from fastapi import APIRouter, Depends, HTTPException, status, Body
import requests
from pydantic import ValidationError
from sqlalchemy import func
from sisprot.db import get_db
from sisprot.auth import jwt_required
from sisprot.models import AnuncioMantenimiento, Cliente
from sisprot.schemas import PaginatedResponseSchema, AnuncioMantenimientoInSchema, AnuncioMantenimientoOutSchema
from sisprot.utils import config


router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])

mantenimiento_msg = (
    "Hola, estamos en mantenimiento\n"
    "Asunto: {asunto}\n"
    "Motivo: {motivo}\n"
    "Acciones: {acciones}\n"
    "Inversiones Sisprot Taurus"
)

falla_msg = (
    "Hola, estamos presentando una falla\n"
    "Asunto: {asunto}\n"
    "Motivo: {motivo}\n"
    "Acciones: {acciones}\n"
    "Inversiones Sisprot Taurus"
)

url = "https://api.wiivo.net/v1/messages"


@router.get("/anuncios", response_model=PaginatedResponseSchema[AnuncioMantenimientoOutSchema], tags=["anuncios"])
def index(page: int = 1, session=Depends(get_db)):
    return session.query(AnuncioMantenimiento).paginate(page=page).as_dict()


@router.post("/anuncio/mantenimiento", tags=["anuncios"])
def crear_anuncio_mantenimiento(
    data: AnuncioMantenimientoInSchema, session=Depends(get_db)
):
    """
    Este endpoint se utiliza para crear los anuncios de mantenimiento
    """

    max_id = (
        session.query(func.max(AnuncioMantenimiento.anuncio_id))
        .filter(AnuncioMantenimiento.tipo == "MANTENIMIENTO")
        .scalar()
    )

    API_TOKEN = config(session, key="wiivo_api_token")

    headers = {"Content-Type": "application/json", "Token": API_TOKEN}

    item = AnuncioMantenimiento(
        **data.dict(exclude={"cliente_status"}),
        status="EN PROCESO",
        tipo="MANTENIMIENTO",
    )
    item.anuncio_id = max_id + 1 if max_id is not None else 1
    session.add(item)

    stmt = session.query(Cliente).filter(
        Cliente.id_estado_cliente == data.cliente_status
    )

    if data.comunidad:
        stmt = stmt.filter(Cliente.barrio_localidad.in_(data.comunidad))

    clientes = stmt.all()

    msg = mantenimiento_msg.format(
        asunto=data.asunto, motivo=data.motivo, acciones=data.accion
    )

    for client in clientes:
        phones = client.telefono.split(",")

        for phone in phones:

            payload = {
                "phone": f"+{client.country.codigo}{phone}",
                "message": msg,
            }

            # print(payload)

            r = requests.post(url, json=payload, headers=headers)
    session.commit()


@router.put("/anuncio/mantenimiento/{id}/cierre", tags=["anuncios"])
def cierre_anuncio_mantenimiento(id: int, session=Depends(get_db)):
    """
    Cierra el anuncio de mantenimiento
    """
    item = session.query(AnuncioMantenimiento).filter_by(id=id, tipo="MANTENIMIENTO").first()

    if not item:
        raise HTTPException(status_code=404, detail="Anuncio de falla no encontrado")


    stmt = session.query(Cliente)

    clientes = []
    if item.comunidad:
        clientes = stmt.filter(Cliente.barrio_localidad.in_(item.comunidad)).all()

    API_TOKEN = config(session, key="wiivo_api_token")

    headers = {"Content-Type": "application/json", "Token": API_TOKEN}
    
    
    for client in clientes:
        phones = client.telefono.split(",")

        for phone in phones:

            payload = {
                "phone": f"+{client.country.codigo}{phone}",
                "message": "El periodo de mantenimiento ha finalizado",
            }

            print(payload)

            r = requests.post(url, json=payload, headers=headers)
    

    item.status = "CERRADO"
    session.commit()


@router.post("/anuncio/falla", tags=["anuncios"])
def crear_anuncio_falla(
    data: AnuncioMantenimientoInSchema, session=Depends(get_db)
):
    """
    Este endpoint se utiliza para crear los anuncios de FALLA y enviar un mensaje a los clientes
    que cumpla los filtros
    """

    max_id = (
        session.query(func.max(AnuncioMantenimiento.anuncio_id))
        .filter(AnuncioMantenimiento.tipo == "FALLA")
        .scalar()
    )

    API_TOKEN = config(session, key="wiivo_api_token")

    headers = {"Content-Type": "application/json", "Token": API_TOKEN}

    item = AnuncioMantenimiento(
        **data.dict(exclude={"cliente_status"}),
        status="EN PROCESO",
        tipo="FALLA",
    )
    item.anuncio_id = max_id + 1 if max_id is not None else 1
    session.add(item)

    stmt = session.query(Cliente).filter(
        Cliente.estado_cliente.ilike(data.cliente_status)
    )

    if data.comunidad:
        stmt = stmt.filter(Cliente.barrio_localidad.in_(data.comunidad))

    clientes = stmt.all()

    msg = falla_msg.format(
        asunto=data.asunto, motivo=data.motivo, acciones=data.accion
    )

    for client in clientes:
        phones = client.telefono.split(",")

        for phone in phones:

            payload = {
                "phone": f"+{client.country.codigo}{phone}",
                "message": msg,
            }

            # print(payload)

            r = requests.post(url, json=payload, headers=headers)
    session.commit()


@router.put("/anuncio/falla/{id}/cierre", tags=["anuncios"])
def cierre_anuncio_falla(id: int, session=Depends(get_db)):
    """
    Cierra el anuncio de falla y notifica a los clientes que la falla ha sido resuelta
    """
    item = session.query(AnuncioMantenimiento).filter_by(id=id, tipo="FALLA").first()

    if not item:
        raise HTTPException(status_code=404, detail="Anuncio de falla no encontrado")

    
    stmt = session.query(Cliente)

    clientes = []
    if item.comunidad:
        clientes = stmt.filter(Cliente.barrio_localidad.in_(item.comunidad)).all()

    API_TOKEN = config(session, key="wiivo_api_token")

    headers = {"Content-Type": "application/json", "Token": API_TOKEN}
    
    
    for client in clientes:
        phones = client.telefono.split(",")

        for phone in phones:

            payload = {
                "phone": f"+{client.country.codigo}{phone}",
                "message": "La falla ha sido resuelta",
            }

            print(payload)

            # r = requests.post(url, json=payload, headers=headers)
    

    item.status = "CERRADO"
    session.commit()