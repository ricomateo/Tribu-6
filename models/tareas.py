from typing import Optional
from datetime import date

from sqlmodel import Field, SQLModel


class TareasBase(SQLModel):
    nombre: str  # definir si es unico o no
    description: str
    fecha_inicio: date  # creacion o de inicio del trabajo? TODO definir
    fecha_fin: Optional[date] = None
    estados: str  # Posibles estados: Iniciada, no iniciada, finalizada
    id_proyecto: Optional[int] = Field(default=None, foreign_key="proyectos.id")
    # Responsable
    # Prioridad
    # Horas estimadas


class Tareas(TareasBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TareasCreate(TareasBase):
    pass


class TareasRead(TareasBase):
    id: int


class TareasUpdate(SQLModel):
    nombre: Optional[str] = None
    description: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estados: Optional[str] = None
    id_proyecto: Optional[int] = None
