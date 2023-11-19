from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class Proyecto(BaseModel):
    nombre: str
    descripcion: str
    fecha_inicio: date
    fecha_estimada_fin: date
    fecha_fin: Optional[date] = None

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "nombre": "ERM Alpha",
                    "descripcion": "Puede acceder desde una amplia gama de dispositivos con conexión a Internet, como computadora personal (PC), portátiles, tabletas y teléfonos inteligentes.",
                    "fecha_inicio": date.today(),
                    "fecha_estimada_fin": date.today().replace(date.today().year + 1),
                    "fecha_fin": None,
                }
            ]
        }


class ListProyectos(BaseModel):
    proyectos: List[Proyecto]
