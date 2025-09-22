"""Entidades del dominio de Content Management

En este archivo se definen las entidades del dominio para la gestión de contenido

"""

from dataclasses import dataclass, field
from enum import Enum
from content_management.seedwork.dominio.entidades import AgregacionRaiz
from content_management.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
import uuid


@dataclass
class Contenido(AgregacionRaiz):
    creador: str = field(default="")
    audiencia: str = field(default="")
    campania: str = field(default="")
    canales: str = field(default="")
    marca: str = field(default="")
    categoria: str = field(default="")
    
@dataclass
class CommandCreatePartner(EventoDominio):
    identificacion: str = None
    campania_asociada: str = None
    canales: str = None
    marca: str = None
    categoria: str = None
