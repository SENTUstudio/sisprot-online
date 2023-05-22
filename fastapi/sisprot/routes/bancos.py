from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from pydantic import ValidationError
from sisprot.db import get_db
from sisprot.auth import jwt_required
from sisprot.models import Banco
from sisprot.schemas import PaginatedResponseSchema, BancoInSchema, BancoOutSchema


router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])

@router.get("/bancos", response_model=PaginatedResponseSchema[BancoOutSchema])
def index(page: int = 1, q: str = None, session=Depends(get_db)):
    """
    Devuelve una lista paginada de Potes
    """
    stmt = session.query(Banco)
    return stmt.paginate(page=page).as_query()


@router.post("/bancos")
def create(data: BancoInSchema, session=Depends(get_db)):
    banco = Banco(**data.dict())
    session.add(banco)
    session.commit()