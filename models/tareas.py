from typing import Optional
from datetime import date

from sqlmodel import Field, SQLModel


class TasksBase(SQLModel):
    name: str
    state: str  # Posibles estados: Iniciada, no iniciada, finalizada
    description: str
    project_id: Optional[int] = Field(default=None, foreign_key="projects.id")
    # Responsable


class Tasks(TasksBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creation_date: date = date.today()
    end_date: Optional[date] = Field(default=None, nullable=True)


class TasksCreate(TasksBase):
    pass


class TasksRead(TasksBase):
    id: int
    creation_date: date
    end_date: Optional[date]


class TasksUpdate(SQLModel):
    name: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[int] = None
    end_date: Optional[date] = None
