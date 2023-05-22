import csv
import codecs
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from pydantic import ValidationError
from sisprot.db import get_db
from sisprot.auth import jwt_required
from sisprot.models import Plan, Factura
from sisprot.schemas import PaginatedResponseSchema, FacturaInSchema, FacturaOutSchema


router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])


@router.get("/facturas", response_model=PaginatedResponseSchema[FacturaOutSchema])
def index(page: int = 1, session=Depends(get_db)):
    """
    Devuelve una lista paginada de facturas
    """
    with session:
        results = session.query(Factura).paginate(page=page).as_dict()
    return results


@router.post("/importar-facturas")
def import_planes(file: UploadFile, session=Depends(get_db)):
    """Importa un CSV de facturas"""
    dialect = csv.Sniffer().sniff(file.file.readline().decode("utf-8"), delimiters=";,")
    file.file.seek(0)

    reader = csv.DictReader(
        codecs.iterdecode(file.file, "utf-8"), skipinitialspace=True, dialect=dialect
    )

    with session:
        for l in reader:
            try:
                item = FacturaInSchema(**l)
            except ValidationError as ex:
                raise HTTPException(status_code=422, detail=ex.errors())
            factura = session.query(Factura).filter_by(id_usuario=item.id_usuario).first()
            if not factura:
                n_client = Factura(**item.dict())
                session.add(n_client)
            else:
                factura.update(**item.dict())
                factura.lote = Plan.lote + 1
        session.commit()
