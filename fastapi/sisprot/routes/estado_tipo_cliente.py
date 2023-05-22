from fastapi import APIRouter, Depends, HTTPException, status
from sisprot.db import get_db
from sisprot.auth import jwt_required
from sisprot.models import EstadoCliente, TipoCliente
from sisprot.schemas import PaginatedResponseSchema, EstadoClienteInSchema, TipoClienteInSchema

router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])


@router.get("/estado-clientes", tags=["estado-clientes"])
def list_estado_clientes(page: int = 1, q: str = None, session=Depends(get_db)):
    """
    Devuelve una lista de todos estados de un cliente
    """
    results = session.query(EstadoCliente).paginate(page=page).as_dict()
    return results

@router.post("/estado-clientes", tags=["estado-clientes"])
def create(data: EstadoClienteInSchema, session=Depends(get_db)):
    item = EstadoCliente(**data.dict())
    session.add(item)
    session.commit()

@router.put("/estado-clientes/{id}", tags=["estado-clientes"])
def update(id: int, data:EstadoClienteInSchema, session=Depends(get_db)):
    """
    Actualiza los parametros de un estado
    """
    with session:
        obj = session.query(EstadoCliente).get(id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"Estado de cliente con id {id} no encontrado")
        
        session.query(EstadoCliente).filter_by(id=id).update(data.dict())
        session.commit()
    
    return "ok"

@router.get("/tipo-clientes", tags=["tipo-clientes"])
def list_tipo_clientes(page: int = 1, q: str = None, session=Depends(get_db)):
    """
    Devuelve una lista paginada de todos los tipos de clientes
    """
    results = session.query(TipoCliente).paginate(page=page).as_dict()
    return results

@router.post("/tipo-clientes", tags=["tipo-clientes"])
def create_tipo_cliente(data:TipoClienteInSchema, session=Depends(get_db)):
    item = TipoCliente(**data.dict())
    session.add(item)
    session.commit()

@router.put("/tipo-clientes/{id}", tags=["tipo-clientes"])
def update(id: int, data:TipoClienteInSchema, session=Depends(get_db)):
    """
    Actualiza los parametros de un tipo de cliente
    """
    with session:
        obj = session.query(TipoCliente).get(id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"Tipo de cliente con id {id} no encontrado")
        
        session.query(TipoCliente).filter_by(id=id).update(data.dict())
        session.commit()
    
    return "ok"