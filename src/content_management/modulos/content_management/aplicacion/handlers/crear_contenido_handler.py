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
        from content_management.modulos.content_management.aplicacion.comandos.comandos_contenido import CommandCreatePartner as CommandCreatePartnerCmd
        
        
        # Create and execute the command
        comando = CommandCreatePartnerCmd(
            saga_id=comando.saga_id,
            id=str(contenido_model.id),
            id_marca=contenido_model.marca,
            id_partner=str(contenido_model.id),  # Use content ID as partner ID for now
            tipo_partnership='marca_embajador',
            terminos_contrato='',
            comision_porcentaje=0.0,
            metas_mensuales=0,
            beneficios_adicionales='',
            notas='',
            fecha_creacion=contenido_model.fecha_creacion.isoformat() if contenido_model.fecha_creacion else datetime.utcnow().isoformat(),
            fecha_actualizacion=contenido_model.fecha_actualizacion.isoformat() if contenido_model.fecha_actualizacion else datetime.utcnow().isoformat()
        )
        ejecutar_commando(comando)

        logger.info(f"Contenido creado exitosamente: {contenido_model.id}")

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creando contenido: {e}")
        raise
