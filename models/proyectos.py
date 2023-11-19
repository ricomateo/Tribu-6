from config.database import Base
from sqlalchemy import Column, Integer, String, Date
from typing import Optional
from datetime import date

from sqlmodel import Field, SQLModel


class ProyectosBase(SQLModel):
    nombre: str
    descripcion: str
    fecha_inicio: date
    fecha_estimada_fin: date
    fecha_fin: Optional[date] = None


class Proyectos(ProyectosBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ProyectosCreate(ProyectosBase):
    pass


class ProyectosRead(ProyectosBase):
    id: int


class ProyectosUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_estimada_fin: Optional[date] = None
    fecha_fin: Optional[date] = None
