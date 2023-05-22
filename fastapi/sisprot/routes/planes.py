import csv
import codecs
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from pydantic import ValidationError
from sisprot.db import get_db
from sisprot.auth import jwt_required
from sisprot.models import Plan, PlanConfAvanzado
from sisprot.schemas import (
    PaginatedResponseSchema,
    PlanInSchema,
    PlanOutSchema,
    PlanConfAvanzadoInSchema,
    PlanCreateSchema,
)


router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])


@router.get(
    "/planes", response_model=PaginatedResponseSchema[PlanOutSchema], tags=["planes"]
)
def index(page: int = 1, id_plan: int = None, session=Depends(get_db)):
    """
    Devuelve una lista paginada de planes
    """
    with session:
        stmt = session.query(Plan)
        if id_plan:
            stmt = stmt.filter(Plan.id_plan == id_plan)
        results = stmt.paginate(page=page).as_dict()
    return results


@router.post("/importar-planes", tags=["planes"])
def import_planes(file: UploadFile, session=Depends(get_db)):
    dialect = csv.Sniffer().sniff(file.file.readline().decode("utf-8"), delimiters=";,")
    file.file.seek(0)

    reader = csv.DictReader(
        codecs.iterdecode(file.file, "utf-8"), skipinitialspace=True, dialect=dialect
    )

    with session:
        for l in reader:
            try:
                item = PlanInSchema(**l)
            except ValidationError as ex:
                raise HTTPException(status_code=422, detail=ex.errors())
            plan = session.query(Plan).filter_by(id_plan=item.id_plan).first()
            if not plan:
                n_client = Plan(**item.dict())
                session.add(n_client)
            else:
                plan.update(**item.dict())
                plan.lote = Plan.lote + 1
        session.commit()


@router.post("/planes/conf-avanzado", tags=["planes"])
def crear_plan_avanzado(data: PlanConfAvanzadoInSchema, session=Depends(get_db)):
    item = PlanConfAvanzado(**data.dict())
    session.add(item)
    session.commit()


@router.get("/planes/conf-avanzado", tags=["planes"])
def list_planes_avanzado(page: int = 1, q: str = None, session=Depends(get_db)):
    """
    Devuelve una lista paginada de todos los planes avanzado
    """
    results = session.query(PlanConfAvanzado).paginate(page=page).as_dict()
    return results


@router.post("/planes", tags=["planes"])
def crear_plan(content: PlanCreateSchema, session=Depends(get_db)):
    item = Plan(**content.plan.dict())
    item.plan_conf_avanzado = PlanConfAvanzado(**content.plan_conf_avanzado.dict())
    session.add(item)
    session.commit()
