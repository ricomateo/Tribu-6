import string
from typing import Optional
from datetime import date

from sqlmodel import Field, SQLModel


class ProyectosBase(SQLModel):
    name: str
    description: str
    fecha_inicio: date
    fecha_estimada_fin: date
    fecha_fin: Optional[date] = None
    state: str


class Proyectos(ProyectosBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ProyectosCreate(ProyectosBase):
    pass


class ProyectosRead(ProyectosBase):
    id: int


class ProyectosUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_estimada_fin: Optional[date] = None
    fecha_fin: Optional[date] = None
    state: Optional[str] = None
