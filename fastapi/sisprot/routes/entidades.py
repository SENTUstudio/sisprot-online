from fastapi import APIRouter, Depends

from sisprot.db import get_db
from sisprot.models import Estados, Municipios, Parroquias, Comunidades

router = APIRouter(prefix="/api")


@router.get("/estados", tags=["entidades"])
def lista_estados(page: int = 1, q: str = None, session=Depends(get_db)):
    """
    Devuelve una lista de los Estados de la Nación
    """
    results = session.query(Estados).all()
    return results


@router.get("/municipios", tags=["entidades"])
def lista_municipios(page: int = 1, q: str = None, session=Depends(get_db)):
    """
    Devuelve una lista de los municipios de la Nación
    """
    results = session.query(Municipios).all()
    return results


@router.get("/municipios/{id}", tags=["entidades"])
def index(*, id: int, session=Depends(get_db)):
    """
    Devuelve una lista de los municipios por Estado
    """
    result = session.query(Municipios).filter_by(id_estado=id).all()
    return result


@router.get("/parroquias", tags=["entidades"])
def lista_parroquias(page: int = 1, q: str = None, session=Depends(get_db)):
    """
    Devuelve una lista de las parroquias de la Nación
    """
    results = session.query(Parroquias).all()
    return results


@router.get("/parroquias/{id}", tags=["entidades"])
def index(*, id: int, session=Depends(get_db)):
    """
    Devuelve una lista de las parroquias por municipio
    """
    result = session.query(Parroquias).filter_by(id_municipio=id).all()
    return result


@router.get("/comunidades", tags=["entidades"])
def lista_comunidades(page: int = 1, q: str = None, session=Depends(get_db)):
    """
    Devuelve una lista de las comunidades de la Nación
    """
    results = session.query(Comunidades).all()
    return results


@router.get("/comunidades/{id}", tags=["entidades"])
def index(*, id: int, session=Depends(get_db)):
    """
    Devuelve una lista de las comunidades por parroquia
    """
    result = session.query(Comunidades).filter_by(id_parroquia=id).all()
    return result
