from typing import Optional
from datetime import date

from sqlmodel import Field, SQLModel


class TasksBase(SQLModel):
    name: str
    state: str  # Posibles estados: Iniciada, no iniciada, finalizada
    description: str
    creation_date: date = date.today()
    id_project: Optional[int] = Field(default=None, foreign_key="projects.id")
    # Responsable


class Tasks(TasksBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TasksCreate(TasksBase):
    pass


class TasksRead(TasksBase):
    id: int


class TasksUpdate(SQLModel):
    name: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    id_project: Optional[int] = None
