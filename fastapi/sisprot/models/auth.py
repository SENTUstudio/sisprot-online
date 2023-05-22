from sqlalchemy import (
    DateTime,
    MetaData,
    Table,
    Column,
    Integer,
    Text,
    select,
    String,
    Date,
    update,
    Boolean,
    ForeignKey,
)
from sisprot.db import BaseModel
from sisprot.utils import check_password, flatten
from sqlalchemy.dialects.postgresql import ARRAY


class Rol(BaseModel):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), unique=True)
    permisos = Column(ARRAY(String(200)))


class Permiso(BaseModel):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True)
    descripcion = Column(String(300))
    modulo = Column(String(100))


class UserAuth(BaseModel):
    __tablename__ = "agentes"
    id_agente = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    nombres = Column(String(100))
    apellidos = Column(String(100))
    dni = Column(String(100))
    email = Column(String(100))
    telefono = Column(String(100))
    rol = Column(Text)
    last_login = Column(DateTime)
    rol_id = Column(Integer)
    id_cartera = Column(Integer, ForeignKey("cartera_clientes.id"), nullable=True)

    def check_password(self, password):
        return check_password(password, self.password_hash)

    def list_permissions(self, session):
        roles = session.query(Rol.permisos).filter(Rol.id == self.rol_id).all()
        user_permissions = flatten([rol[0] for rol in roles if rol[0] is not None])
        return user_permissions
