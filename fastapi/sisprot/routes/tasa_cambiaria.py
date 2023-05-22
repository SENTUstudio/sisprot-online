from datetime import datetime
from fastapi import APIRouter, Depends
from sisprot.models import TasaCambiaria
from sisprot.db import get_db
from sisprot.utils import get_closest
from sisprot.auth import jwt_required
from sisprot.schemas import PaginatedResponseSchema, TasaCambiariaSchema

router = APIRouter(prefix="/api")


@router.get(
    "/tasas-cambiaria",
    response_model=PaginatedResponseSchema[TasaCambiariaSchema],
    dependencies=[Depends(jwt_required)],
)
def index(page: int = 1, session=Depends(get_db)):
    """
    Devuelve una lista paginada de todas las tasas cambiarias por dia
    """
    with session:
        results = session.query(TasaCambiaria).paginate(page=page).as_dict()
    return results


@router.get("/tasa-actual")
def tasa_actual(session=Depends(get_db)):
    """
    Retorna la tasa actual del BCV
    """
    tasa = get_closest(session, TasaCambiaria, TasaCambiaria.fecha, datetime.now())
    return tasa

