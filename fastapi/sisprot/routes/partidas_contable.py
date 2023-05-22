from fastapi import APIRouter, Depends, HTTPException, status
from sisprot.db import get_db
from sisprot.auth import jwt_required
from sisprot.models import PartidaContable
from sisprot.schemas import PaginatedResponseSchema, PartidaContableInSchema, PartidaContableOutSchema


router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])


@router.get("/partidas-contable", response_model=PaginatedResponseSchema[PartidaContableOutSchema])
def index(page: int = 1, session=Depends(get_db)):
    """
    Devuelve una lista paginada de Partidas Contables
    """
    with session:
        results = session.query(PartidaContable).paginate(page=page).as_dict()
    return results


@router.post("/partidas-contable")
def create(data: PartidaContableInSchema, session=Depends(get_db)):
    """
    Crea una partida contable
    """
    with session:
        partida_contable = PartidaContable(**data.dict())
        session.add(partida_contable)
        session.commit()
    
    return "ok"
