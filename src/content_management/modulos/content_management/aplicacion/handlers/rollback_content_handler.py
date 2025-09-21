"""Handler para el comando CommandContentRollbacked

Este archivo define el handler para el rollback de contenido como parte de la saga.
"""

from content_management.modulos.content_management.aplicacion.comandos.comandos_contenido import CommandContentRollbacked
from content_management.seedwork.aplicacion.comandos import ejecutar_commando
from content_management.infraestructura.pulsar import pulsar_publisher
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@ejecutar_commando.register
def _(comando: CommandContentRollbacked):
    """Handler para CommandContentRollbacked (saga)"""
    try:
        # Crear y publicar evento CommandContentRollbacked usando la estructura de dominio
        from content_management.modulos.content_management.dominio.entidades import CommandContentRollbacked as CommandContentRollbackedEvent
        evento = CommandContentRollbackedEvent(
            id=comando.id,
            motivo=comando.motivo,
            fecha_rollback=comando.fecha_rollback or datetime.utcnow().isoformat()
        )

        # Publicar evento en Pulsar con saga_id y status
        pulsar_publisher.publish_event(
            comando.saga_id,
            evento,
            'CommandContentRollbacked',
            'success'
        )

        logger.info(f"CommandContentRollbacked publicado exitosamente para id: {comando.id}")

    except Exception as e:
        logger.error(f"Error en CommandContentRollbacked: {e}")
        # Publicar evento fallido si es necesario
        pulsar_publisher.publish_event(
            comando.saga_id,
            evento,
            'CommandContentRollbacked',
            'failed'
        )
        raise