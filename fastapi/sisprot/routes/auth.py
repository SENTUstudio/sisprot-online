from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_another_jwt_auth import AuthJWT

from sisprot.db import get_db
from sisprot.models import UserAuth, Cliente
from sisprot.schemas import UserAuthScheme, UserAuthOutScheme
from sisprot.utils import row2dict

router = APIRouter(prefix="/api")


@router.post(
    "/login",
    summary="Ingresa un usuario al sistema",
    tags=["auth"],
    response_model=UserAuthOutScheme,
)
async def login_auth(
        data: UserAuthScheme, session=Depends(get_db), Authorize: AuthJWT = Depends()
):
    """
    Ingresa un usuario al sistema.

    - **username**: Usuario
    - **password**: Contraseña
    """
    with session:
        user = session.query(UserAuth).filter_by(username=data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad username or password"
        )

    if not user.check_password(data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad username or password"
        )

    user_claims = {
        "scopes": "admin"
    }

    access_token = Authorize.create_access_token(subject=user.username, user_claims=user_claims)
    user.last_login = datetime.now()
    session.commit()

    return dict(
        accessToken=access_token, user=row2dict(user, exclude=["password_hash"])
    )


@router.post("/verify-token", response_model=UserAuthOutScheme, tags=["auth"])
def verify_token(Authorize: AuthJWT = Depends(), session=Depends(get_db)):
    Authorize.jwt_optional()

    username = Authorize.get_jwt_subject()

    user = session.query(UserAuth).filter_by(username=username).first()

    return {"accessToken": "", "user": user}


@router.post(
    "/authorize",
    summary="Ingresa un usuario al sistema",
    tags=["auth"],
    response_model=UserAuthOutScheme,
)
def authorize(
        data: UserAuthScheme, session=Depends(get_db), Authorize: AuthJWT = Depends()
):
    """
    Ingresa un usuario al sistema.

    - **username**: Usuario
    - **password**: Contraseña
    """
    with session:
        user = session.query(UserAuth).filter_by(username=data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=""
        )

    if not user.check_password(data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=""
        )

    access_token = Authorize.create_access_token(subject=user.username)

    return None


@router.post(
    "/clientes_login",
    summary="Ingresa un usuario al sistema",
    tags=["auth"],
    # response_model=UserAuthOutScheme,
)
def login_auth_cliente(
        data: UserAuthScheme, session=Depends(get_db), Authorize: AuthJWT = Depends()
):
    """
    Ingresa un usuario al sistema.

    - **username**: Usuario
    - **password**: Contraseña
    """

    user = session.query(Cliente).filter_by(dni_cedula=data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad username or password"
        )

    if not user.clave_6d == data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad username or password"
        )

    user_claims = {
        "scopes": "cliente"
    }

    access_token = Authorize.create_access_token(subject=user.dni_cedula, user_claims=user_claims)
    user.last_login = datetime.now()
    session.commit()

    return dict(
        accessToken=access_token
    )
