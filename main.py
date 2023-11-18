from fastapi import FastAPI
from fastapi import status
import uvicorn
from models.proyectos import Proyecto, ListProyectos

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello world"}


@app.get(
    "/get_proyectos",
    status_code=status.HTTP_200_OK,
    response_model=ListProyectos,
    tags=["Proyetos"],
)
def get_proyectos():
    return ListProyectos()


@app.get("/get_proyecto/{id}", status_code=status.HTTP_200_OK, tags=["Proyetos"])
def get_proyecto_por_id(id):
    return {"message": "Hello world"}


@app.post(
    "/create_proyecto",
    status_code=status.HTTP_201_CREATED,
    response_model=Proyecto,
    tags=["Proyetos"],
)
def create_proyecto(proyecto: Proyecto):
    return proyecto


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
