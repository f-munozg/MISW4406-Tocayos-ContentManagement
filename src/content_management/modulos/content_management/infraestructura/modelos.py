"""Modelos de base de datos para contenido

En este archivo se definen los modelos de base de datos para contenido

"""

from content_management.config.db import db
from sqlalchemy import Column, String, DateTime, Float, Integer, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from enum import Enum as PyEnum

class TipoContenidoEnum(PyEnum):
    POST_INSTAGRAM = "post_instagram"
    STORY_INSTAGRAM = "story_instagram"
    POST_FACEBOOK = "post_facebook"
    VIDEO_YOUTUBE = "video_youtube"
    POST_TIKTOK = "post_tiktok"
    BLOG_POST = "blog_post"
    EMAIL_MARKETING = "email_marketing"
    INFOGRAFIA = "infografia"

class EstadoContenidoEnum(PyEnum):
    BORRADOR = "borrador"
    EN_REVISION = "en_revision"
    APROBADO = "aprobado"
    PUBLICADO = "publicado"
    ARCHIVADO = "archivado"
    RECHAZADO = "rechazado"

class CategoriaContenidoEnum(PyEnum):
    PRODUCTO = "producto"
    LIFESTYLE = "lifestyle"
    EDUCACIONAL = "educacional"
    PROMOCIONAL = "promocional"
    TESTIMONIAL = "testimonial"
    ENTERTAINMENT = "entertainment"

class ContenidoDBModel(db.Model):
    __tablename__ = "contenido"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_campana = Column(UUID(as_uuid=True), nullable=True)
    id_creador = Column(UUID(as_uuid=True), nullable=False)
    id_marca = Column(UUID(as_uuid=True), nullable=False)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    tipo_contenido = Column(Enum(TipoContenidoEnum), nullable=False)
    categoria = Column(Enum(CategoriaContenidoEnum), nullable=False)
    estado = Column(Enum(EstadoContenidoEnum), nullable=False, default=EstadoContenidoEnum.BORRADOR)
    url_media = Column(Text, nullable=True)
    hashtags = Column(Text, nullable=True)
    menciones = Column(Text, nullable=True)
    fecha_programada = Column(DateTime, nullable=True)
    fecha_publicacion = Column(DateTime, nullable=True)
    plataformas = Column(Text, nullable=True)
    metricas_engagement = Column(Integer, nullable=False, default=0)
    metricas_alcance = Column(Integer, nullable=False, default=0)
    metricas_impresiones = Column(Integer, nullable=False, default=0)
    metricas_clics = Column(Integer, nullable=False, default=0)
    costo_produccion = Column(Float, nullable=False, default=0.0)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_ultima_actividad = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Contenido {self.titulo} ({self.estado.value})>"
