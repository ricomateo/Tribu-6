from config.database import Base
from sqlalchemy import Column, Integer, String, Date
from typing import Optional
from datetime import date

from sqlmodel import Field, SQLModel


class Proyectos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    fecha_inicio: date
    fecha_estimada_fin: date
    fecha_fin: Optional[date] = None


class ProyectosUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_estimada_fin: Optional[date] = None
    fecha_fin: Optional[date] = None


# class Proyecto(Base):
#     __tablename__ = "Proyectos"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     nombre = Column(String)
#     descripcion = Column(String)
#     fecha_inicio = Column(Date)
#     fecha_estimada_fin = Column(Date)
#     fecha_fin = Column(Date, nullable=True)
