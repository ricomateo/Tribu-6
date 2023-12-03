from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlmodel import Session, select
from models.proyectos import Projects
from models.empleados import Employees
from models.tareas import Tasks, TasksUpdate, TasksRead, TasksCreate
from config.database import get_session

routerTasks = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={404: {"description": "Not found"}},
)


@routerTasks.get(
    "/get_tasks", status_code=status.HTTP_200_OK, response_model=List[TasksRead]
)
def get_tasks(*, session: Session = Depends(get_session)):
    tasks = session.exec(select(Tasks)).all()
    return tasks


@routerTasks.get(
    "/get_task/{id}",
    status_code=status.HTTP_200_OK,
    response_model=Tasks,
)
def get_task_by_id(*, session: Session = Depends(get_session), id: int):
    task = session.get(Tasks, id)
    if not task:
        raise HTTPException(status_code=404, detail="No se encontro tarea")

    return task


@routerTasks.get(
    "/get_tasks_by_project_id/{id}",
    status_code=status.HTTP_200_OK,
    response_model=List[TasksRead],
)
def get_tasks_by_project_id(
    *, session: Session = Depends(get_session), project_id: int
):
    tasks = session.exec(select(Tasks).where(Tasks.project_id == project_id)).all()
    # if not tasks:
    #     raise HTTPException(status_code=404, detail="No se encontraron tareas")

    return tasks


@routerTasks.post(
    "/create_task",
    status_code=status.HTTP_201_CREATED,
    response_model=TasksRead,
)
def create_task(*, session: Session = Depends(get_session), task: TasksCreate):
    # Validacion fk
    if task.project_id != None and not session.get(Projects, task.project_id):
        raise HTTPException(status_code=404, detail="No hay proyecto con ese id")

    if task.responsible_id != None and not session.get(Employees, task.responsible_id):
        raise HTTPException(status_code=404, detail="No hay empleado con ese legajo")

    db_tasks = Tasks.from_orm(task)
    session.add(db_tasks)
    session.commit()
    session.refresh(db_tasks)
    return db_tasks


@routerTasks.delete(
    "/delete_task/{id}", status_code=status.HTTP_200_OK, response_model=Tasks
)
def delete_task(*, session: Session = Depends(get_session), id: int):
    task = session.get(Tasks, id)
    if not task:
        raise HTTPException(status_code=404, detail="No se encontro tarea")
    session.delete(task)
    session.commit()
    return task


@routerTasks.patch("/update_task/{id}", response_model=TasksRead)
def update_task(*, session: Session = Depends(get_session), id: int, task: TasksUpdate):
    db_tasks = session.get(Tasks, id)
    if not db_tasks:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # Validacion fk
    if task.project_id != None and not session.get(Projects, task.project_id):
        raise HTTPException(status_code=404, detail="No hay proyecto con ese id")

    if task.responsible_id != None and not session.get(Employees, task.responsible_id):
        raise HTTPException(status_code=404, detail="No hay empleado con ese legajo")

    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_tasks, key, value)
    session.add(db_tasks)
    session.commit()
    session.refresh(db_tasks)
    return db_tasks
