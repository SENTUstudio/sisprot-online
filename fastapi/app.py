from datetime import timedelta
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
from fastapi_another_jwt_auth import AuthJWT
from fastapi_another_jwt_auth.exceptions import AuthJWTException


from sisprot.models import BaseModel
from sisprot.db import db_session
from sisprot.routes import (
    auth,
    partidas_contable,
    potes,
    metodos_pago,
    clientes,
    clientes_wisphub,
    tasa_cambiaria,
    planes,
    tasa_digital,
    reporte_de_pagos,
    configuraciones,
    bancos,
    mensajeria,
    anuncios_mantenimiento,
    estado_tipo_cliente,
    tasks,
    prospectos_residenciales,
    prospectos_pymes,
    reporte_fallas,
    users,
    carteras,
    entidades,
)

app = FastAPI()
_settings = dotenv_values()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(potes.router)
app.include_router(metodos_pago.router)
app.include_router(clientes.router)
app.include_router(clientes_wisphub.router)
app.include_router(tasa_cambiaria.router)
app.include_router(planes.router)
app.include_router(tasa_digital.router)
app.include_router(partidas_contable.router)
app.include_router(reporte_de_pagos.router)
app.include_router(configuraciones.router)
app.include_router(bancos.router)
app.include_router(mensajeria.router)
app.include_router(anuncios_mantenimiento.router)
app.include_router(estado_tipo_cliente.router)
app.include_router(tasks.router)
app.include_router(prospectos_residenciales.router)
app.include_router(prospectos_pymes.router)
app.include_router(reporte_fallas.router)
app.include_router(users.router)
app.include_router(carteras.router)
app.include_router(entidades.router)


@AuthJWT.load_config
def get_config():
    return [
        ("authjwt_secret_key", _settings["JWT_SECRET_KEY"]),
        ("authjwt_access_token_expires", timedelta(days=360)),
    ]


# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


# BaseModel.metadata.create_all(bind=db_session().bind)
