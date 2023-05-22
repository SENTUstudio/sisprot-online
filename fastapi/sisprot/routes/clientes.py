import csv
import codecs
from operator import or_
from sqlalchemy import or_
from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy import String
from sisprot.db import get_db
from sisprot.auth import jwt_required
from sisprot.models import Cliente
from sisprot.schemas import PaginatedResponseSchema, ClienteOutSchema, ClienteInSchema, ClientEditSchema


router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])


@router.get("/clientes", tags=["clientes"])
def index(page: int = 1, q: str = None, session=Depends(get_db)):
    """
    Devuelve una lista paginada de Clientes importados
    Parametros:

    - **q**: Palabras a buscar
    """
    with session:

        stmt = session.query(Cliente)

        if q:
            stmt = stmt.filter(
                or_(
                    Cliente.nombre_cliente.ilike("%" + q + "%"),
                    Cliente.dni_cedula.ilike("%" + q + "%")
                )
            )
        results = stmt.paginate(page=page).as_dict()
    return results

@router.post("/clientes/", tags=["clientes"])
def create_cliente(data: ClienteInSchema, session=Depends(get_db)):
    """
    Crea un cliente
    """
    item = Cliente(**data.dict())
    session.add(item)
    session.commit()


@router.get("/clientes/estados-filtros/", tags=["clientes"])
def estados_filtros(session=Depends(get_db)):
    results = {}
    fields = ["barrio_localidad", "router", "plan_internet", "estado_facturacion"]
    for field in fields:
        results[field] = [
            item[field]
            for item in session.query(getattr(Cliente, field)).distinct().all()
        ]
    return results


@router.get("/clientes/{ci_usuario}", response_model=ClienteOutSchema, tags=["clientes"])
def retrieve(ci_usuario: str, session=Depends(get_db)):
    """
    Devuelve un cliente por su nro de cedula
    """

    item = session.query(Cliente).filter_by(dni_cedula=ci_usuario).first()

    if not item:
        raise HTTPException(status_code=404, detail="CLiente no encontrado")

    return item

@router.put("/clientes/{ci_usuario}", tags=["clientes"])
def edit(ci_usuario: str, data: ClientEditSchema, session=Depends(get_db)):
    """Devuelve un cliente por su nro de cedula
    
    """
    data = data.dict(exclude_none=True)
    item = session.query(Cliente).filter_by(dni_cedula=ci_usuario).first()

    if not item:
        raise HTTPException(status_code=404, detail="CLiente no encontrado")
    for k,v in data.items():
        setattr(item, k, v)
    session.commit()


@router.post("/importar-clientes", tags=["clientes"])
def import_clientes(file: UploadFile, session=Depends(get_db)):
    """
    Importa un listado de clientes en formato CSV
    *file*: Archivo a subir
    """
    try:
        dialect = csv.Sniffer().sniff(file.file.readline().decode("utf-8"), delimiters=";,")
        file.file.seek(0)
        reader = csv.DictReader(
            codecs.iterdecode(file.file, "utf-8"), skipinitialspace=True, dialect=dialect
        )
    except:

        raise HTTPException(status_code=400, detail="Hubo un error al subir el archivo")

    with session:
        for l in reader:
            try:
                item = ClienteInSchema(**l)
            except ValidationError as ex:
                raise HTTPException(status_code=422, detail=ex.errors())
            cliente = (
                session.query(Cliente).filter_by(id_cliente_wisphub=item.id_cliente_wisphub).first()
            )
            if not cliente:
                n_client = Cliente(**item.dict())
                session.add(n_client)
            else:
                cliente.update(**item.dict())
                cliente.lote = Cliente.lote + 1
        session.commit()


