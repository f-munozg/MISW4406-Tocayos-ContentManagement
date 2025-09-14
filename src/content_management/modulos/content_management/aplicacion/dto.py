"""DTOs para la gestión de contenido

En este archivo se definen los DTOs para la gestión de contenido

"""

from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class ContenidoDTO:
    id: str
    id_campana: str = ""
    id_creador: str = ""
    id_marca: str = ""
    titulo: str = ""
    descripcion: str = ""
    tipo_contenido: str = "post_instagram"
    categoria: str = "producto"
    estado: str = "borrador"
    url_media: str = ""
    hashtags: str = ""
    menciones: str = ""
    fecha_programada: str = ""
    fecha_publicacion: str = ""
    plataformas: str = ""
    metricas_engagement: int = 0
    metricas_alcance: int = 0
    metricas_impresiones: int = 0
    metricas_clics: int = 0
    costo_produccion: float = 0.0
    fecha_creacion: str = ""
    fecha_ultima_actividad: str = ""
    fecha_actualizacion: str = ""
