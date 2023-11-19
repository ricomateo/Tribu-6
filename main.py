from fastapi import FastAPI, status
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from models.proyectos import Proyectos, ProyectosUpdate
from config.database import Session, engine, Base


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get(
    "/get_proyectos",
    status_code=status.HTTP_200_OK,
    tags=["Proyectos"],
)
def get_proyectos():
    db = Session()
    result = db.query(Proyectos).all()

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(result)
    )


@app.get(
    "/get_proyecto/{id}",
    status_code=status.HTTP_200_OK,
    response_model=Proyectos,
    tags=["Proyectos"],
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


@app.post(
    "/create_proyecto",
    status_code=status.HTTP_201_CREATED,
    response_model=Proyectos,
    tags=["Proyectos"],
)
def create_proyecto(proyecto: Proyectos):
    db = Session()

    new_proyecto = Proyectos(**proyecto.dict())

    db.add(new_proyecto)
    db.commit()
    return proyecto


@app.delete(
    "/delete_proyecto/{id}",
    status_code=status.HTTP_200_OK,
    tags=["Proyectos"],
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


@app.patch(
    "/patch_proyecto",
    status_code=status.HTTP_200_OK,
    tags=["Proyectos"],
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


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
