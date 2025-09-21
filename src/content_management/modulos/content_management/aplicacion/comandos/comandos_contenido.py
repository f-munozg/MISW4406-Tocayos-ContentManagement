"""Comandos para la gestión de contenido

En este archivo se definen los comandos para la gestión de contenido

"""

from dataclasses import dataclass
from content_management.seedwork.aplicacion.comandos import Comando
from datetime import datetime
import uuid

@dataclass
class CommandCreatePartner(Comando):
    saga_id: str
    id: str
    id_marca: str
    id_partner: str
    tipo_partnership: str
    terminos_contrato: str = ""
    comision_porcentaje: float = 0.0
    metas_mensuales: str = ""
    beneficios_adicionales: str = ""
    notas: str = ""
    fecha_creacion: str = ""
    fecha_actualizacion: str = ""

@dataclass
class CommandContentRollbacked(Comando):
    saga_id: str
    id: str
    motivo: str = ""
    fecha_rollback: str = ""

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