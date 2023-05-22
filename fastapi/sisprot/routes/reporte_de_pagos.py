from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sisprot.db import get_db
from sisprot.auth import jwt_required
from sisprot.models import ReportePago
from sisprot.schemas import PaginatedResponseSchema, ReportePagoOutSchema, ReportePagoInSchema


router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])

@router.get(
    "/reporte-de-pagos",
    response_model=PaginatedResponseSchema[ReportePagoOutSchema],
    dependencies=[Depends(jwt_required)],
)
def index(page: int = 1, session=Depends(get_db)):
    """
    Devuelve una lista paginada de todos los reportes de pago realizado
    """
    with session:
        results = session.query(ReportePago).paginate(page=page).as_dict()
    return results

@router.post("/reporte-de-pagos")
def create(data: ReportePagoInSchema):
    pass