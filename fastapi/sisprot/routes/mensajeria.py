from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from pydantic import ValidationError
from sisprot.db import get_db
from sisprot.auth import jwt_required
from sisprot.models import Cliente, PlantillaMensaje, Pais, Task
from sisprot.utils import is_time_between, config, row2dict
from sisprot.tasks import messages

from sisprot.schemas import (
    MessageSchema,
    PaginatedResponseSchema,
    PlantillaMensajeOutSchema,
    PlantillaMensajeInSchema,
    DeviceSchema
)

import requests


router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])

url = "https://api.wiivo.net/v1/messages"


class Default(dict):
    def __missing__(self, key):
        return key.join("{}")


@router.post("/mensajeria", tags=["mensajeria"])
def send_messages(
    data: MessageSchema,
    bg: BackgroundTasks,
    session=Depends(get_db),
):

    # print(data.filters.dict())

    task = Task(status="STARTING")
    session.add(task)

    session.commit()

    bg.add_task(messages.send_messages, task_id=task.id, data=data, filters=data.filters.dict())

    return {
        'task_id': task.id, 'status': 'RUNNING'
    }


@router.get("/mensajeria/multimedia", tags=["mensajeria"])
def list_multimedia(page: int = 0, session=Depends(get_db)):
    API_TOKEN = config(session, key="wiivo_api_token")

    url = "https://api.wiivo.net/v1/files"

    querystring = {"size": "25", "page": page, "status": "any"}

    headers = {"Token": API_TOKEN}

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()


@router.post("/mensajeria/subir-archivo", tags=["mensajeria"])
async def upload_file(file: UploadFile, session=Depends(get_db)):
    API_TOKEN = config(session, key="wiivo_api_token")

    url = "https://api.wiivo.net/v1/files"

    headers = {"Token": API_TOKEN}

    file_bytes = file.file.read()

    data = {"file": file_bytes}

    response = requests.post(url, files=data, headers=headers)

    return response.json()


@router.delete("/mensajeria/eliminar-archivo/{file_id}", tags=["mensajeria"])
def delete_file(file_id: str, session=Depends(get_db)):
    API_TOKEN = config(session, key="wiivo_api_token")

    url = f"https://api.wiivo.net/v1/files/{file_id}"

    headers = {"Token": API_TOKEN}

    response = requests.request("DELETE", url, headers=headers)

    return response.json()


@router.get("/mensajeria/plantillas", response_model=PaginatedResponseSchema[PlantillaMensajeOutSchema], tags=["mensajeria"])
def list_plantillas(page: int = 1, session=Depends(get_db)):
    return session.query(PlantillaMensaje).paginate(page=page).as_query()


@router.post("/mensajeria/plantillas", tags=["mensajeria"])
def create_plantilla(data: PlantillaMensajeInSchema, session=Depends(get_db)):
    session.add(PlantillaMensaje(**data.dict()))
    session.commit()


@router.put("/mensajeria/plantillas/{id}", tags=["mensajeria"])
def edit_plantilla(id: int, data: PlantillaMensajeInSchema, session=Depends(get_db)):
    session.query(PlantillaMensaje).filter_by(id=id).update(data.dict())
    session.commit()


@router.delete("/mensajeria/plantillas/{id}", tags=["mensajeria"])
def delete_plantilla(id: int, session=Depends(get_db)):
    session.query(PlantillaMensaje).filter_by(id=id).delete()
    session.commit()

@router.get('/devices', tags=["mensajeria"])
def devices(session=Depends(get_db)):
    API_TOKEN = config(session, key="wiivo_api_token")

    url = f"https://api.wiivo.net/v1/devices"

    headers = {"Token": API_TOKEN}
    response = requests.get( url, headers=headers)

    return response.json()