from typing import Optional
from datetime import date

from sqlmodel import Field, SQLModel


class ProjectsBase(SQLModel):
    name: str
    state: str
    description: str
    expected_duration_days: int
    project_id_leader: Optional[int]


class Projects(ProjectsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creation_date: date = date.today()
    end_date: Optional[date] = Field(default=None, nullable=True)


class ProjectsCreate(ProjectsBase):
    pass


class ProjectsRead(ProjectsBase):
    id: int
    creation_date: date = date.today()
    end_date: Optional[date]


class ProjectsUpdate(SQLModel):
    name: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    expected_duration_days: Optional[int] = None
    project_id_leader: Optional[int] = None
    end_date: Optional[date] = None
