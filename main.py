from fastapi import FastAPI
import uvicorn
from config.database import engine, Base

from routers import proyectos


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(proyectos.router)


@app.get("/")
async def root():
    return {"message": "API de proyectos online"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)
