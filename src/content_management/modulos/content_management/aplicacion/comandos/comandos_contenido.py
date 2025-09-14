"""Comandos para la gestión de contenido

En este archivo se definen los comandos para la gestión de contenido

"""

from dataclasses import dataclass
from content_management.seedwork.aplicacion.comandos import Comando
from content_management.modulos.content_management.dominio.entidades import TipoContenido, EstadoContenido, CategoriaContenido
from datetime import datetime
import uuid

@dataclass
class BuscarContenido(Comando):
    id: str
    creador: str = ""
    audiencia: str = ""
    campania: str = ""
    canales: str = ""
    marca: str = ""
    categoria: str = ""
    fecha_creacion: str = ""
    fecha_actualizacion: str = ""