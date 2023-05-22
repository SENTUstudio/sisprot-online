from datetime import datetime, date, time
from operator import or_
from fastapi import APIRouter, Depends, HTTPException, status
from dotenv import dotenv_values
from sqlalchemy import or_, func
from sqlalchemy.orm import joinedload
from sisprot.db import get_db
from sisprot.auth import jwt_required, get_current_user
from sisprot.models import Pote
from sisprot.schemas import PaginatedResponseSchema, PoteInSchema, PoteOutSchema
from sisprot.utils import is_time_between, config


router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])


@router.get("/potes", response_model=PaginatedResponseSchema[PoteOutSchema], tags=["potes"])
def index(page: int = 1, q: str = None, session=Depends(get_db)):
    """
    Devuelve una lista paginada de Potes
    """
    with session:

        # stmt = session.query(Pote).join(Pote.metodo_de_pago)
        stmt = session.query(Pote).options(
            joinedload(Pote.metodo_de_pago),
            joinedload(Pote.agente).load_only("id_agente", "username"),
            joinedload(Pote.banco)
        )

        if q:
            stmt = stmt.filter(
                or_(
                    Pote.num_referencia.like(f"%{q}"),
                    Pote.referencia_pago_sisprot.like(f"%{q}"),
                )
            )
        results = stmt.paginate(page=page).as_query()
    return results


@router.post("/potes", tags=["potes"])
def create(
    data: PoteInSchema,
    password: str = None,
    session=Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Crea un pote

    Para editar la contrasena, editar la clave `PASSWORD_POTE` en
    el archivo .env en el directorio raiz del proyecto
    """
    now = datetime.now().time()

    pote_horario = {
        "inicio": config(session, key="pote_start"),
        "cierre": config(session, key="pote_end"),
        "password": config(session, key="pote_password"),
    }


    start = datetime.strptime(pote_horario["inicio"], "%H:%M").time()
    end = datetime.strptime(pote_horario["cierre"], "%H:%M").time()

    if not is_time_between(start, end, check_time=now):
        if not password == pote_horario["password"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El modulo de potes solo esta permitido desde {pote_horario['inicio']} a {pote_horario['cierre']}",
            )

    with session:
        pote = Pote(**data.dict())
        pote.fecha_pago_registrado_agente = datetime.today()
        pote.id_agente = current_user.id_agente

        max_id = session.query(func.max(Pote.id)).scalar()

        PREFIX = "SIS"
        session.add(pote)
        session.flush()
        pote.referencia_pago_sisprot = "{}{:010d}".format(
            PREFIX, max_id + 1 if max_id is not None else 1
        )
        session.commit()

    return "ok"
