from typing import Optional
from datetime import date

from sqlmodel import Field, SQLModel


class TareasBase(SQLModel):
    nombre: str
    descripcion: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    estados: str  # Posibles estados: Iniciada, no iniciada, finalizada


class Tareas(TareasBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TareasCreate(TareasBase):
    pass


class TareasRead(TareasBase):
    id: int


class TareasUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estados: Optional[str] = None
