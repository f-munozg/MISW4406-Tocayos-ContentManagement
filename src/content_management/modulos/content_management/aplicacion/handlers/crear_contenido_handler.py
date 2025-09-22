"""Handler para el comando BuscarContenido

En este archivo se define el handler para crear contenido

"""

from content_management.modulos.content_management.aplicacion.comandos.comandos_contenido import BuscarContenido
from content_management.modulos.content_management.infraestructura.modelos import ContenidoDBModel
from content_management.seedwork.aplicacion.comandos import ejecutar_commando
from content_management.infraestructura.pulsar import pulsar_publisher
from content_management.config.db import db
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

@ejecutar_commando.register
def _(comando: BuscarContenido):
    """Handler para crear nuevo contenido"""
    try:
        # Crear modelo de base de datos directamente
        contenido_model = ContenidoDBModel()
        contenido_model.id = uuid.UUID(comando.id) if comando.id else uuid.uuid4()
        contenido_model.creador = comando.creador
        contenido_model.audiencia = comando.audiencia
        contenido_model.campania = comando.campania
        contenido_model.canales = comando.canales
        contenido_model.marca = comando.marca
        contenido_model.categoria = comando.categoria
        contenido_model.fecha_creacion = datetime.fromisoformat(comando.fecha_creacion) if comando.fecha_creacion else datetime.utcnow()
        contenido_model.fecha_actualizacion = datetime.fromisoformat(comando.fecha_actualizacion) if comando.fecha_actualizacion else datetime.utcnow()

        # Guardar en base de datos
        db.session.add(contenido_model)
        db.session.commit()

        # Crear y publicar evento CommandCreatePartner
        from content_management.modulos.content_management.dominio.entidades import CommandCreatePartner
        evento = CommandCreatePartner(
            identificacion=contenido_model.creador,
            campania_asociada=contenido_model.campania,
            canales=contenido_model.canales,
            marca=contenido_model.marca,
            categoria=contenido_model.categoria
        )

        # Publicar evento en Pulsar
        # pulsar_publisher.publish_event(evento, 'content-events')
        pulsar_publisher.publish_event(evento, 'partner-events', 'Success')

        logger.info(f"Contenido creado exitosamente: {contenido_model.id}")

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creando contenido: {e}")
        raise
