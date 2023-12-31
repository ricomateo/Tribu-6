from typing import Optional
from datetime import date

from sqlmodel import Field, SQLModel


class TasksBase(SQLModel):
    name: str
    state: str  # Posibles estados: Iniciada, no iniciada, finalizada
    priority: str
    description: str
    project_id: Optional[int] = Field(default=None, foreign_key="projects.id")
    responsible_id: Optional[int] = Field(default=None, foreign_key="employees.legajo")
    end_date: Optional[date] = None


class Tasks(TasksBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creation_date: date = date.today()


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
    priority: Optional[str] = None
    end_date: Optional[date] = None
    responsible_id: Optional[int] = None
    project_id: Optional[int] = None
