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
    
    '''
    def enviar_a_revision(self):
        if self.estado == EstadoContenido.BORRADOR:
            self.estado = EstadoContenido.EN_REVISION
            self.fecha_ultima_actividad = datetime.now()
            self.agregar_evento(ContenidoEnviadoRevision(
                id_contenido=self.id,
                id_campana=self.id_campana,
                id_creador=self.id_creador,
                id_marca=self.id_marca,
                titulo=self.titulo,
                fecha_envio=datetime.now()
            ))
    
    def aprobar_contenido(self, aprobador: str = ""):
        if self.estado == EstadoContenido.EN_REVISION:
            self.estado = EstadoContenido.APROBADO
            self.fecha_ultima_actividad = datetime.now()
            self.agregar_evento(ContenidoAprobado(
                id_contenido=self.id,
                id_campana=self.id_campana,
                id_creador=self.id_creador,
                id_marca=self.id_marca,
                titulo=self.titulo,
                aprobador=aprobador,
                fecha_aprobacion=datetime.now()
            ))
    '''
    
@dataclass
class ContenidoAsociadoPartner(EventoDominio):
    identificacion: str = None
    campania_asociada: str = None
    canales: str = None
    marca: str = None
    categoria: str = None
