"""Comandos para la gestión de contenido

En este archivo se definen los comandos para la gestión de contenido

"""

from dataclasses import dataclass
from content_management.seedwork.aplicacion.comandos import Comando
from content_management.modulos.content_management.dominio.entidades import TipoContenido, EstadoContenido, CategoriaContenido
from datetime import datetime
import uuid

@dataclass
class CrearContenido(Comando):
    id: str
    id_campana: str = ""
    id_creador: str = ""
    id_marca: str = ""
    titulo: str = ""
    descripcion: str = ""
    tipo_contenido: str = "post_instagram"
    categoria: str = "producto"
    url_media: str = ""
    hashtags: str = ""
    menciones: str = ""
    fecha_programada: str = ""
    plataformas: str = ""
    costo_produccion: float = 0.0
    fecha_creacion: str = ""
    fecha_actualizacion: str = ""

@dataclass
class EnviarRevisionContenido(Comando):
    id_contenido: str
    fecha_actualizacion: str = ""

@dataclass
class AprobarContenido(Comando):
    id_contenido: str
    aprobador: str = ""
    fecha_actualizacion: str = ""

@dataclass
class RechazarContenido(Comando):
    id_contenido: str
    motivo: str = ""
    aprobador: str = ""
    fecha_actualizacion: str = ""

@dataclass
class PublicarContenido(Comando):
    id_contenido: str
    fecha_publicacion: str = ""
    fecha_actualizacion: str = ""

@dataclass
class ArchivarContenido(Comando):
    id_contenido: str
    motivo: str = ""
    fecha_actualizacion: str = ""

@dataclass
class ActualizarMetricasContenido(Comando):
    id_contenido: str
    engagement: int = 0
    alcance: int = 0
    impresiones: int = 0
    clics: int = 0
    fecha_actualizacion: str = ""
