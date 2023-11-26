from fastapi import APIRouter, status, HTTPException
from typing import List
from sqlmodel import Session, select
from models.proyectos import Proyectos
from models.tareas import Tareas, TareasUpdate, TareasRead, TareasCreate
from config.database import engine

routerTareas = APIRouter(
    prefix="/tareas",
    tags=["Tareas"],
    responses={404: {"description": "Not found"}},
)


@routerTareas.get(
    "/get_tareas", status_code=status.HTTP_200_OK, response_model=List[TareasRead]
)
def get_tareas():
    with Session(engine) as session:
        tareas = session.exec(select(Tareas)).all()
        return tareas


@routerTareas.get(
    "/get_tareas/{id}",
    status_code=status.HTTP_200_OK,
    response_model=Tareas,
)
def get_tarea_por_id(id: int):
    with Session(engine) as session:
        tarea = session.get(Tareas, id)
        if not tarea:
            raise HTTPException(status_code=404, detail="No se encontro tarea")

        return tarea


@routerTareas.post(
    "/create_tarea",
    status_code=status.HTTP_201_CREATED,
    response_model=TareasRead,
)
def create_tarea(tarea: TareasCreate):
    with Session(engine) as session:
        # Validacion fk
        if tarea.id_proyecto != None and not session.get(Proyectos, tarea.id_proyecto):
            raise HTTPException(status_code=404, detail="No hay proyecto con ese id")

        db_tareas = Tareas.from_orm(tarea)
        session.add(db_tareas)
        session.commit()
        session.refresh(db_tareas)
        return db_tareas


@routerTareas.delete(
    "/delete_tarea/{id}", status_code=status.HTTP_200_OK, response_model=Tareas
)
def delete_tarea(id: int):
    with Session(engine) as session:
        tarea = session.get(Tareas, id)
        if not tarea:
            raise HTTPException(status_code=404, detail="No se encontro tarea")
        session.delete(tarea)
        session.commit()
        return tarea


@routerTareas.patch("/patch_tarea/{id}", response_model=TareasRead)
def update_tarea(id: int, tarea: TareasUpdate):
    with Session(engine) as session:
        db_tareas = session.get(Tareas, id)
        if not db_tareas:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

        # Validacion fk
        if tarea.id_proyecto != None and not session.get(Proyectos, tarea.id_proyecto):
            raise HTTPException(status_code=404, detail="No hay proyecto con ese id")

        tarea_data = tarea.dict(exclude_unset=True)
        for key, value in tarea_data.items():
            setattr(db_tareas, key, value)
        session.add(db_tareas)
        session.commit()
        session.refresh(db_tareas)
        return db_tareas
