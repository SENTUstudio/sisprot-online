import csv
import codecs
from operator import or_
from sqlalchemy import or_
from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy import String
from sisprot.db import get_db
from sisprot.auth import jwt_required
from sisprot.models import ClienteWisphub
from sisprot.schemas import ClienteWisphubInSchema


router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])


@router.get("/clientes-wisphub", tags=["clientes-wisphub"])
def index(page: int = 1, q: str = None, session=Depends(get_db)):
    """
    Devuelve una lista paginada de Clientes importados
    Parametros:

    - **q**: Palabras a buscar
    """
    with session:
        stmt = session.query(ClienteWisphub)

        if q:
            stmt = stmt.filter(
                or_(
                    ClienteWisphub.cedula.ilike("%" + q + "%"),
                    ClienteWisphub.id_servicio.ilike("%" + q + "%"),
                )
            )
        results = stmt.paginate(page=page).as_dict()
    return results
