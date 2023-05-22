from fastapi import APIRouter, Depends, HTTPException, status
from sisprot.db import get_db
from sisprot.auth import jwt_required, get_current_user, user_has_permissions
from sisprot.models import Task, UserAuth, Rol, CarteraCliente
from sisprot.schemas import UserCreateSchema, AnalistaUserInSchema
from sisprot.utils import get_hashed_password


router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])


@router.post("/cartera/user-cartera-analista", tags=["cartera"])
def create_wallet_analyst(
    data: AnalistaUserInSchema,
    session=Depends(get_db),
    current_user=Depends(user_has_permissions(permissions=["wallet_analyst:create"])),
):
    if session.query(UserAuth).filter(UserAuth.username == data.username).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    user = UserAuth(
        **data.dict(
            include={
                "username",
                "password_hash",
                "nombres",
                "apellidos",
                "dni",
                "email",
                "telefono",
            }
        )
    )

    cartera = CarteraCliente(**data.dict(include={"nombre", "tipo", "estado"}))
    session.add(cartera)
    session.flush()
    user.id_cartera = cartera.id
    password = get_hashed_password(data.password_hash)
    user.password_hash = password
    rol = session.query(Rol).filter(Rol.nombre == "Analista_Cartera").first()

    user.rol_id = rol.id
    session.add(user)
    # session.add(cartera)
    session.commit()
