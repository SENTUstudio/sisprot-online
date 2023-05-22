from fastapi import APIRouter, Depends, HTTPException, status
from sisprot.db import get_db
from sisprot.auth import jwt_required
from sisprot.models import Configuracion
from sisprot.schemas import PaginatedResponseSchema, UpdateConfigKeySchema
from sisprot.roles import admin_allowed

router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])


@router.get("/configuraciones", dependencies=[Depends(admin_allowed)])
def list_configuraciones(page: int = 1, q: str = None, session=Depends(get_db)):
    """
    Devuelve una lista de todas las configuraciones registradas en BD
    """
    with session:
        results = session.query(Configuracion).paginate(page=page).as_dict()
    return results


@router.post("/configuraciones", dependencies=[Depends(admin_allowed)])
def update_configuracion(data: UpdateConfigKeySchema, session=Depends(get_db)):
    conf_obj = session.query(Configuracion).filter_by(key=data.key).first()

    if not conf_obj:
        raise HTTPException(status_code=404, detail="Object does not exist")

    conf_obj.value = data.value
    session.commit()
