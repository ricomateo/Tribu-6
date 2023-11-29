from fastapi import FastAPI
import uvicorn
from config.database import create_db_and_tables

from routers.proyectos import routerProjects
from routers.tareas import routerTasks
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

create_db_and_tables()

app.include_router(routerProjects)
app.include_router(routerTasks)


@app.get("/")
async def root():
    return {"message": "API del area de proyectos está en linea"}


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)
