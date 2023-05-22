from fastapi import APIRouter, Depends, HTTPException, status
from sisprot.db import get_db
from sisprot.auth import jwt_required, get_current_user, user_has_permissions
from sisprot.models import Task, UserAuth, Rol
from sisprot.schemas import UserCreateSchema, PaginatedResponseSchema, RolOutSchema
from sisprot.utils import get_hashed_password


router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])


@router.get("/roles", response_model=PaginatedResponseSchema[RolOutSchema])
def list_roles(page: int = 1, session=Depends(get_db)):
    stmt = session.query(Rol)

    return stmt.paginate(page=page).as_query()


@router.post("/users", tags=["users"])
def create_user(
    data: UserCreateSchema,
    session=Depends(get_db),
    current_user=Depends(user_has_permissions(permissions=["lider_cartera:create", "admin_cartera:create"])),
):

    if session.query(UserAuth).filter(UserAuth.username == data.username).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    permissions = current_user.list_permissions(session)

    # if "admin_cartera:create" in permissions:
    #     rol = session.query(Rol).filter(Rol.nombre == "Administrador_Cartera").first()
    #     data.rol = rol.id
    if "lider_cartera:create" in permissions:
        rol = session.query(Rol).filter(Rol.id == data.rol_id).first()
        if rol.nombre not in ["Cartera_Lider_Residencial", "Cartera_Lider_Corporativo"]:
            raise HTTPException(status_code=400, detail="Este rol no se puede asignar")

    user = UserAuth(**data.dict())
    password = get_hashed_password(data.password_hash)
    user.password_hash = password
    session.add(user)
    session.commit()

    print("user creado")



