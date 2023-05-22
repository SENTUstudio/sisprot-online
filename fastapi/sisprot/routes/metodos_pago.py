from fastapi import APIRouter, Depends, HTTPException, status
from sisprot.db import get_db
from sisprot.auth import jwt_required
from sisprot.models import MetodoPago
from sisprot.schemas import PaginatedResponseSchema, MetodoPagoInSchema, MetodoPagoOutSchema

router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])

@router.get("/metodos-de-pago", response_model=PaginatedResponseSchema[MetodoPagoOutSchema])
def index(page: int = 1, session=Depends(get_db)):
    """
    Devuelve una lista paginada de Metodos de pago
    """
    with session:
        results = session.query(MetodoPago).paginate(page=page).as_dict()
    return results

@router.post("/metodos-de-pago")
def create(data: MetodoPagoInSchema, session=Depends(get_db)):
    """
    Crea un metodo de pago
    """
    with session:
        metodo_pago = MetodoPago(**data.dict())
        session.add(metodo_pago)
        session.commit()
    
    return "ok"

@router.put("/metodos-de-pago/{id}")
def update(id: int, data: MetodoPagoInSchema, session=Depends(get_db)):
    """
    Actualiza los parametros de un metodo de pago
    """
    with session:
        obj = session.query(MetodoPago).get(id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"Metodo de pago con id {id} no encontrado")
        
        session.query(MetodoPago).filter_by(id=id).update(data.dict())
        session.commit()
    
    return "ok"