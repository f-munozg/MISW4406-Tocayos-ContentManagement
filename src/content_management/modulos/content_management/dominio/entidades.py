"""Entidades del dominio de Content Management

En este archivo se definen las entidades del dominio para la gestión de contenido

"""

from dataclasses import dataclass, field
from enum import Enum
from content_management.seedwork.dominio.entidades import AgregacionRaiz
from content_management.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
import uuid

class EstadoContenido(Enum):
    BORRADOR = "borrador"
    EN_REVISION = "en_revision"
    APROBADO = "aprobado"
    PUBLICADO = "publicado"
    ARCHIVADO = "archivado"
    RECHAZADO = "rechazado"

class TipoContenido(Enum):
    POST_INSTAGRAM = "post_instagram"
    STORY_INSTAGRAM = "story_instagram"
    POST_FACEBOOK = "post_facebook"
    VIDEO_YOUTUBE = "video_youtube"
    POST_TIKTOK = "post_tiktok"
    BLOG_POST = "blog_post"
    EMAIL_MARKETING = "email_marketing"
    INFOGRAFIA = "infografia"

class CategoriaContenido(Enum):
    PRODUCTO = "producto"
    LIFESTYLE = "lifestyle"
    EDUCACIONAL = "educacional"
    PROMOCIONAL = "promocional"
    TESTIMONIAL = "testimonial"
    ENTERTAINMENT = "entertainment"

@dataclass
class Contenido(AgregacionRaiz):
    id_campana: uuid.UUID = field(default=None)
    id_creador: uuid.UUID = field(default=None)
    id_marca: uuid.UUID = field(default=None)
    titulo: str = field(default="")
    descripcion: str = field(default="")
    tipo_contenido: TipoContenido = field(default=TipoContenido.POST_INSTAGRAM)
    categoria: CategoriaContenido = field(default=CategoriaContenido.PRODUCTO)
    estado: EstadoContenido = field(default=EstadoContenido.BORRADOR)
    url_media: str = field(default="")
    hashtags: str = field(default="")
    menciones: str = field(default="")
    fecha_programada: datetime = field(default=None)
    fecha_publicacion: datetime = field(default=None)
    plataformas: str = field(default="")
    metricas_engagement: int = field(default=0)
    metricas_alcance: int = field(default=0)
    metricas_impresiones: int = field(default=0)
    metricas_clics: int = field(default=0)
    costo_produccion: float = field(default=0.0)
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_ultima_actividad: datetime = field(default_factory=datetime.now)
    
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
    
    def rechazar_contenido(self, motivo: str = "", aprobador: str = ""):
        if self.estado == EstadoContenido.EN_REVISION:
            self.estado = EstadoContenido.RECHAZADO
            self.fecha_ultima_actividad = datetime.now()
            self.agregar_evento(ContenidoRechazado(
                id_contenido=self.id,
                id_campana=self.id_campana,
                id_creador=self.id_creador,
                id_marca=self.id_marca,
                titulo=self.titulo,
                motivo=motivo,
                aprobador=aprobador,
                fecha_rechazo=datetime.now()
            ))
    
    def publicar_contenido(self, fecha_publicacion: datetime = None):
        if self.estado == EstadoContenido.APROBADO:
            self.estado = EstadoContenido.PUBLICADO
            self.fecha_publicacion = fecha_publicacion or datetime.now()
            self.fecha_ultima_actividad = datetime.now()
            self.agregar_evento(ContenidoPublicado(
                id_contenido=self.id,
                id_campana=self.id_campana,
                id_creador=self.id_creador,
                id_marca=self.id_marca,
                titulo=self.titulo,
                fecha_publicacion=self.fecha_publicacion
            ))
    
    def archivar_contenido(self, motivo: str = ""):
        if self.estado in [EstadoContenido.PUBLICADO, EstadoContenido.APROBADO]:
            self.estado = EstadoContenido.ARCHIVADO
            self.fecha_ultima_actividad = datetime.now()
            self.agregar_evento(ContenidoArchivado(
                id_contenido=self.id,
                id_campana=self.id_campana,
                id_creador=self.id_creador,
                id_marca=self.id_marca,
                titulo=self.titulo,
                motivo=motivo,
                fecha_archivo=datetime.now()
            ))
    
    def actualizar_metricas(self, engagement: int = 0, alcance: int = 0, impresiones: int = 0, clics: int = 0):
        if self.estado == EstadoContenido.PUBLICADO:
            self.metricas_engagement += engagement
            self.metricas_alcance += alcance
            self.metricas_impresiones += impresiones
            self.metricas_clics += clics
            self.fecha_ultima_actividad = datetime.now()
            self.agregar_evento(MetricasContenidoActualizadas(
                id_contenido=self.id,
                id_campana=self.id_campana,
                id_creador=self.id_creador,
                id_marca=self.id_marca,
                titulo=self.titulo,
                engagement_total=self.metricas_engagement,
                alcance_total=self.metricas_alcance,
                impresiones_total=self.metricas_impresiones,
                clics_total=self.metricas_clics,
                fecha_actualizacion=datetime.now()
            ))

@dataclass
class ContenidoCreado(EventoDominio):
    id_contenido: uuid.UUID = None
    id_campana: uuid.UUID = None
    id_creador: uuid.UUID = None
    id_marca: uuid.UUID = None
    titulo: str = None
    tipo_contenido: str = None
    categoria: str = None
    fecha_creacion: datetime = None

@dataclass
class ContenidoEnviadoRevision(EventoDominio):
    id_contenido: uuid.UUID = None
    id_campana: uuid.UUID = None
    id_creador: uuid.UUID = None
    id_marca: uuid.UUID = None
    titulo: str = None
    fecha_envio: datetime = None

@dataclass
class ContenidoAprobado(EventoDominio):
    id_contenido: uuid.UUID = None
    id_campana: uuid.UUID = None
    id_creador: uuid.UUID = None
    id_marca: uuid.UUID = None
    titulo: str = None
    aprobador: str = None
    fecha_aprobacion: datetime = None

@dataclass
class ContenidoRechazado(EventoDominio):
    id_contenido: uuid.UUID = None
    id_campana: uuid.UUID = None
    id_creador: uuid.UUID = None
    id_marca: uuid.UUID = None
    titulo: str = None
    motivo: str = None
    aprobador: str = None
    fecha_rechazo: datetime = None

@dataclass
class ContenidoPublicado(EventoDominio):
    id_contenido: uuid.UUID = None
    id_campana: uuid.UUID = None
    id_creador: uuid.UUID = None
    id_marca: uuid.UUID = None
    titulo: str = None
    fecha_publicacion: datetime = None

@dataclass
class ContenidoArchivado(EventoDominio):
    id_contenido: uuid.UUID = None
    id_campana: uuid.UUID = None
    id_creador: uuid.UUID = None
    id_marca: uuid.UUID = None
    titulo: str = None
    motivo: str = None
    fecha_archivo: datetime = None

@dataclass
class MetricasContenidoActualizadas(EventoDominio):
    id_contenido: uuid.UUID = None
    id_campana: uuid.UUID = None
    id_creador: uuid.UUID = None
    id_marca: uuid.UUID = None
    titulo: str = None
    engagement_total: int = None
    alcance_total: int = None
    impresiones_total: int = None
    clics_total: int = None
    fecha_actualizacion: datetime = None
