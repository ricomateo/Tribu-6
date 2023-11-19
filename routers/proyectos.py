from fastapi import APIRouter, status, HTTPException
from typing import List
from sqlmodel import Session, select
from models.proyectos import Proyectos, ProyectosUpdate, ProyectosRead, ProyectosCreate
from config.database import engine

router = APIRouter(
    prefix="/proyectos",
    tags=["Proyectos"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/get_proyectos", status_code=status.HTTP_200_OK, response_model=List[ProyectosRead]
)
def get_proyectos():
    with Session(engine) as session:
        heroes = session.exec(select(Proyectos)).all()
        return heroes


@router.get(
    "/get_proyecto/{id}",
    status_code=status.HTTP_200_OK,
    response_model=Proyectos,
)
def get_proyecto_por_id(id: int):
    with Session(engine) as session:
        proyecto = session.get(Proyectos, id)
        if not proyecto:
            raise HTTPException(status_code=404, detail="No se encontro proyecto")

        return proyecto


@router.post(
    "/create_proyecto",
    status_code=status.HTTP_201_CREATED,
    response_model=ProyectosRead,
)
def create_proyecto(proyecto: ProyectosCreate):
    with Session(engine) as session:
        db_proyectos = Proyectos.from_orm(proyecto)
        session.add(db_proyectos)
        session.commit()
        session.refresh(db_proyectos)
        return db_proyectos


@router.delete(
    "/delete_proyecto/{id}", status_code=status.HTTP_200_OK, response_model=Proyectos
)
def delete_proyecto(id: int):
    with Session(engine) as session:
        proyecto = session.get(Proyectos, id)
        if not proyecto:
            raise HTTPException(status_code=404, detail="No se encontro proyecto")
        session.delete(proyecto)
        session.commit()
        return proyecto


@router.patch("/patch_proyecto/{id}", response_model=ProyectosRead)
def update_proyecto(id: int, proyecto: ProyectosUpdate):
    with Session(engine) as session:
        db_proyectos = session.get(Proyectos, id)
        if not db_proyectos:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")

        proyecto_data = proyecto.dict(exclude_unset=True)
        for key, value in proyecto_data.items():
            setattr(db_proyectos, key, value)
        session.add(db_proyectos)
        session.commit()
        session.refresh(db_proyectos)
        return db_proyectos
