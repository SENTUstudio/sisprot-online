from datetime import datetime, date, time
from operator import or_
from fastapi import APIRouter, Depends, HTTPException, status
from dotenv import dotenv_values
from sqlalchemy import or_, func
from sqlalchemy.orm import joinedload
from sisprot.db import get_db
from sisprot.auth import jwt_required, get_current_user
from sisprot.models import Task


router = APIRouter(prefix="/api", dependencies=[Depends(jwt_required)])


@router.get("/tasks", tags=["tasks"])
def index(page: int = 1, q: str = None, session=Depends(get_db)):
    stmt = session.query(Task).order_by(Task.id.desc())
    results = stmt.paginate(page=page).as_dict()
    return results

@router.get("/tasks/{task_id}", tags=["tasks"])
def retrieve(task_id: int, session=Depends(get_db)):
    stmt = session.query(Task).filter_by(id=task_id)
    return stmt.first()
