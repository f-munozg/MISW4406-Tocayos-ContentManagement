"""Handler para el comando CrearContenido

En este archivo se define el handler para crear contenido

"""

from content_management.modulos.content_management.aplicacion.comandos.comandos_contenido import CrearContenido
from content_management.modulos.content_management.infraestructura.modelos import (
    ContenidoDBModel, TipoContenidoEnum, EstadoContenidoEnum, CategoriaContenidoEnum
)
from content_management.seedwork.aplicacion.comandos import ejecutar_commando
from content_management.infraestructura.pulsar import pulsar_publisher
from content_management.config.db import db
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

@ejecutar_commando.register
def _(comando: CrearContenido):
    """Handler para crear nuevo contenido"""
    try:
        # Crear modelo de base de datos directamente
        contenido_model = ContenidoDBModel()
        contenido_model.id = uuid.UUID(comando.id)
        contenido_model.id_campana = uuid.UUID(comando.id_campana) if comando.id_campana else None
        contenido_model.id_creador = uuid.UUID(comando.id_creador)
        contenido_model.id_marca = uuid.UUID(comando.id_marca)
        contenido_model.titulo = comando.titulo
        contenido_model.descripcion = comando.descripcion
        contenido_model.tipo_contenido = TipoContenidoEnum(comando.tipo_contenido)
        contenido_model.categoria = CategoriaContenidoEnum(comando.categoria)
        contenido_model.estado = EstadoContenidoEnum.BORRADOR
        contenido_model.url_media = comando.url_media
        contenido_model.hashtags = comando.hashtags
        contenido_model.menciones = comando.menciones
        contenido_model.plataformas = comando.plataformas
        contenido_model.costo_produccion = comando.costo_produccion
        
        if comando.fecha_programada:
            contenido_model.fecha_programada = datetime.fromisoformat(comando.fecha_programada)
        if comando.fecha_creacion:
            contenido_model.fecha_creacion = datetime.fromisoformat(comando.fecha_creacion)
        if comando.fecha_actualizacion:
            contenido_model.fecha_actualizacion = datetime.fromisoformat(comando.fecha_actualizacion)
        
        # Guardar en base de datos
        db.session.add(contenido_model)
        db.session.commit()
        
        # Crear y publicar evento de dominio
        from content_management.modulos.content_management.dominio.entidades import ContenidoCreado
        evento = ContenidoCreado(
            id_contenido=contenido_model.id,
            id_campana=contenido_model.id_campana,
            id_creador=contenido_model.id_creador,
            id_marca=contenido_model.id_marca,
            titulo=contenido_model.titulo,
            tipo_contenido=contenido_model.tipo_contenido.value,
            categoria=contenido_model.categoria.value,
            fecha_creacion=contenido_model.fecha_creacion
        )
        
        # Publicar evento en Pulsar
        pulsar_publisher.publish_event(evento, 'content-events')
        
        logger.info(f"Contenido creado exitosamente: {contenido_model.id}")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creando contenido: {e}")
        raise
