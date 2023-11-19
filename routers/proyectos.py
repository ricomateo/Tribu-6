from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from models.proyectos import Proyectos, ProyectosUpdate, ProyectosRead, ProyectosCreate
from config.database import Session

router = APIRouter(
    prefix="/proyectos",
    tags=["Proyectos"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/get_proyectos", status_code=status.HTTP_200_OK, response_model=List[ProyectosRead]
)
def get_proyectos():
    db = Session()
    result = db.query(Proyectos).all()

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(result)
    )


@router.get(
    "/get_proyecto/{id}",
    status_code=status.HTTP_200_OK,
    response_model=Proyectos,
)
def get_proyecto_por_id(id: int):
    db = Session()
    result = db.query(Proyectos).filter(Proyectos.id == id).first()

    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "No existe un proyecto con ese id"},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(result)
    )


@router.post(
    "/create_proyecto",
    status_code=status.HTTP_201_CREATED,
    response_model=Proyectos,
)
def create_proyecto(proyecto: Proyectos):
    db = Session()

    new_proyecto = Proyectos(**proyecto.dict())

    db.add(new_proyecto)
    db.commit()
    return proyecto


@router.delete(
    "/delete_proyecto/{id}",
    status_code=status.HTTP_200_OK,
)
def delete_proyecto(id: int):
    db = Session()
    result = db.query(Proyectos).filter(Proyectos.id == id).first()

    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "No existe un proyecto con ese id"},
        )

    db.delete(result)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(result)
    )


@router.patch(
    "/patch_proyecto",
    status_code=status.HTTP_200_OK,
)
def update_proyecto(proyecto_id: int, proyecto: ProyectosUpdate):
    db = Session()
    result = db.get(Proyectos, proyecto_id)

    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "No existe un proyecto con ese id"},
        )

    proyecto_data = proyecto.dict(exclude_unset=True)
    for key, value in proyecto_data.items():
        setattr(result, key, value)

    db.add(result)
    db.commit()
    db.refresh(result)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(result)
    )
