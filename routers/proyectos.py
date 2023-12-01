from fastapi import APIRouter, status, HTTPException
from typing import List
from sqlmodel import Session, select
from models.empleados import Employees
from models.proyectos import Projects, ProjectsUpdate, ProjectsRead, ProjectsCreate
from config.database import engine

routerProjects = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    responses={404: {"description": "Not found"}},
)


@routerProjects.get(
    "/get_projects", status_code=status.HTTP_200_OK, response_model=List[ProjectsRead]
)
def get_projects():
    with Session(engine) as session:
        projects = session.exec(select(Projects)).all()
        return projects


@routerProjects.get(
    "/get_project/{id}",
    status_code=status.HTTP_200_OK,
    response_model=Projects,
)
def get_project_by_id(id: int):
    with Session(engine) as session:
        project = session.get(Projects, id)
        if not project:
            raise HTTPException(status_code=404, detail="No se encontro proyecto")

        return project


@routerProjects.post(
    "/create_project",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectsRead,
)
def create_project(project: ProjectsCreate):
    with Session(engine) as session:
        # Validacion fk
        if project.project_leader_id != None and not session.get(
            Employees, project.project_leader_id
        ):
            raise HTTPException(
                status_code=404, detail="No hay empleado con ese legajo"
            )

        db_projects = Projects.from_orm(project)
        session.add(db_projects)
        session.commit()
        session.refresh(db_projects)
        return db_projects


@routerProjects.delete(
    "/delete_project/{id}", status_code=status.HTTP_200_OK, response_model=Projects
)
def delete_project(id: int):
    with Session(engine) as session:
        project = session.get(Projects, id)
        if not project:
            raise HTTPException(status_code=404, detail="No se encontro proyecto")
        session.delete(project)
        session.commit()
        return project


@routerProjects.patch("/update_project/{id}", response_model=ProjectsRead)
def update_project(id: int, project: ProjectsUpdate):
    with Session(engine) as session:
        db_projects = session.get(Projects, id)
        if not db_projects:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")

        # Validacion fk
        if project.project_leader_id != None and not session.get(
            Employees, project.project_leader_id
        ):
            raise HTTPException(
                status_code=404, detail="No hay empleado con ese legajo"
            )

        project_data = project.dict(exclude_unset=True)
        for key, value in project_data.items():
            setattr(db_projects, key, value)
        session.add(db_projects)
        session.commit()
        session.refresh(db_projects)
        return db_projects
