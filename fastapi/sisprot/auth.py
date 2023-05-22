from fastapi import Depends, HTTPException, status
from fastapi_another_jwt_auth import AuthJWT

from sisprot.models import UserAuth, Cliente, Rol, Permiso
from sisprot.db import get_db
from sisprot.utils import flatten

def jwt_required(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()


def get_current_user(Authorize: AuthJWT = Depends(), session=Depends(get_db)):
    Authorize.jwt_required()
    identity = Authorize.get_jwt_subject()

    scopes = Authorize.get_raw_jwt().get("scopes", "")

    if scopes != "admin":
        raise HTTPException(status_code=401, detail="You are not logged as admin")
    
    with session:
        user = session.query(UserAuth).filter_by(username=identity).one_or_none()
    return user


def get_current_client(Authorize: AuthJWT = Depends(), session=Depends(get_db)):
    Authorize.jwt_required()
    identity = Authorize.get_jwt_subject()

    scopes = Authorize.get_raw_jwt().get("scopes", "")

    if scopes != "cliente":
        raise HTTPException(status_code=401, detail="You are not logged as client")

    user = session.query(Cliente).filter_by(dni_cedula=identity).one_or_none()
    return user

def user_has_permissions(permissions=None):
    def wrapper(Authorize: AuthJWT = Depends(), session=Depends(get_db)):
        Authorize.jwt_required()
        identity = Authorize.get_jwt_subject()
        user = session.query(UserAuth).filter_by(username=identity).one_or_none()

        roles = session.query(Rol.permisos).filter(Rol.id == user.rol_id).all()
        user_permissions = flatten([rol[0] for rol in roles if rol[0] is not None])

        if 'all' in user_permissions:
            return user


        if permissions is not None and not any(x in permissions for x in user_permissions):
            raise HTTPException(status_code=401, detail="Permisos insuficientes")

        return user
    return wrapper