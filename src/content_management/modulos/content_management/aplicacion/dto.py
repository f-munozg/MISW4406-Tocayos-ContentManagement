"""DTOs para la gestión de contenido

En este archivo se definen los DTOs para la gestión de contenido

"""

from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class ContenidoDTO:
    id: str
    creador: str
    audiencia: str = ""
    campania: str = ""
    canales: str = ""
    marca: str = ""
    categoria: str = ""
    fecha_creacion: str = ""
    fecha_actualizacion: str = ""
