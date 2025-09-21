"""Handler para el comando CommandCreatePartner

Este archivo define el handler para crear un partner asociado a contenido, siguiendo la estructura de PartnerLifecycle.
"""

from content_management.modulos.content_management.aplicacion.comandos.comandos_contenido import CommandCreatePartner
from content_management.modulos.content_management.infraestructura.modelos import ContenidoDBModel
from content_management.seedwork.aplicacion.comandos import ejecutar_commando
from content_management.infraestructura.pulsar import pulsar_publisher
from content_management.config.db import db
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

@ejecutar_commando.register
def _(comando: CommandCreatePartner):
    """Handler para crear un partner asociado a contenido"""
    try:
        # Crear y publicar evento CommandCreatePartner
        from content_management.modulos.content_management.dominio.entidades import CommandCreatePartner as CommandCreatePartnerEvent
        evento = CommandCreatePartnerEvent(
            id=comando.id,
            id_marca=comando.id_marca,
            id_partner=comando.id_partner,
            tipo_partnership=comando.tipo_partnership,
            terminos_contrato=comando.terminos_contrato,
            comision_porcentaje=comando.comision_porcentaje,
            metas_mensuales=comando.metas_mensuales,
            beneficios_adicionales=comando.beneficios_adicionales,
            notas=comando.notas,
            fecha_creacion=comando.fecha_creacion or datetime.utcnow().isoformat(),
            fecha_actualizacion=comando.fecha_actualizacion or datetime.utcnow().isoformat()
        )

        # Publicar evento en Pulsar con saga_id y status
        pulsar_publisher.publish_event(
            comando.saga_id,
            evento,
            'CommandCreatePartner',
            'success'
        )

        logger.info(f"CommandCreatePartner publicado exitosamente para partner: {comando.id_partner}")

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creando CommandCreatePartner: {e}")
        # Publicar evento fallido si es necesario
        pulsar_publisher.publish_event(
            comando.saga_id,
            evento,
            'CommandCreatePartner',
            'failed'
        )
        raise
