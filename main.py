from fastapi import FastAPI
import uvicorn
from config.database import create_db_and_tables

from routers.proyectos import routerProyectos
from routers.tareas import routerTareas

app = FastAPI()

create_db_and_tables()

app.include_router(routerProyectos)
app.include_router(routerTareas)


@app.get("/")
async def root():
    return {"message": "API de proyectos está en linea"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)
