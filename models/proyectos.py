from typing import Optional
from datetime import date

from sqlmodel import Field, SQLModel


class ProjectsBase(SQLModel):
    name: str
    state: str
    description: str
    creation_date: date = date.today()
    id_proyect_leader: Optional[int]


class Projects(ProjectsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ProjectsCreate(ProjectsBase):
    pass


class ProjectsRead(ProjectsBase):
    id: int


class ProjectsUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    state: Optional[str] = None
    id_proyect_leader: Optional[int] = None
