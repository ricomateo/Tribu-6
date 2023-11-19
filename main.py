from fastapi import FastAPI
import uvicorn
from config.database import create_db_and_tables

from routers import proyectos


app = FastAPI()

create_db_and_tables()

app.include_router(proyectos.router)


@app.get("/")
async def root():
    return {"message": "API de proyectos está en linea"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)
