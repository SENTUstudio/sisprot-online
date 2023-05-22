from datetime import datetime
from fastapi import APIRouter, Depends
from sisprot.models import TasaDigital
from sisprot.db import get_db
from sisprot.utils import get_closest
from sisprot.auth import jwt_required
from sisprot.schemas import PaginatedResponseSchema, TasaCambiariaSchema, TasaCambiariaInSchema

router = APIRouter(prefix="/api")


@router.get(
    "/tasas-digital",
    response_model=PaginatedResponseSchema[TasaCambiariaSchema],
    dependencies=[Depends(jwt_required)],
)
def index(page: int = 1, session=Depends(get_db)):
    """
    Devuelve una lista paginada de todas las tasas digitales por dia
    """
    with session:
        results = session.query(TasaDigital).paginate(page=page).as_dict()
    return results


@router.get("/tasa-actual-digital")
def tasa_actual(session=Depends(get_db)):
    """
    Retorna la tasa digital
    """
    tasa = get_closest(session, TasaDigital, TasaDigital.fecha, datetime.now())
    return tasa

@router.post("/tasas-digital")
def create(data: TasaCambiariaInSchema, session=Depends(get_db)):
    """
    Crea un objeto tasa digital
    """
    with session:
        tasa_digital = TasaDigital(**data.dict())
        session.add(tasa_digital)
        session.commit()
    return "ok"


@router.delete("/tasas-digital/{tasa_id}")
def delete(tasa_id: int, session=Depends(get_db)):
    """
    - **tasa_id**: ID de la tasa digital
    """
    with session:
        session.query(TasaDigital).filter_by(id=tasa_id).delete()
    return "ok"