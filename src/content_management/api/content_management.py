"""API para la gestión de contenido

En este archivo se define la API REST para la gestión de contenido

"""

from flask import Blueprint, request, jsonify, Response
from content_management.modulos.content_management.aplicacion.comandos.comandos_contenido import (
    BuscarContenido
)
from content_management.modulos.content_management.aplicacion.queries.queries_contenido import (
    ObtenerContenido, ObtenerContenidosPorCampana, ObtenerContenidosPorCreador,
    ObtenerContenidosPorMarca, ObtenerContenidosPorTipo, ObtenerContenidosPorEstado
)
from content_management.modulos.content_management.aplicacion.mapeadores import MapeadorContenidoDTOJson
from content_management.seedwork.aplicacion.comandos import ejecutar_commando
from content_management.seedwork.dominio.excepciones import ExcepcionDominio
from datetime import datetime
import json
import uuid
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('content_management', __name__, url_prefix='/content-management')

@bp.route('/buscar-contenido', methods=['POST'])
def buscar_contenido():
    """
    Endpoint to receive an event body, create a content record, and publish CommandCreatePartner event.
    """
    try:
        event_body = request.json
        logger.info(f"Received event for /buscar-contenido: {event_body}")

        # Map incoming event to DTO using the mapeador
        map_contenido = MapeadorContenidoDTOJson()
        contenido_dto = map_contenido.externo_a_dto(event_body)

        # Build BuscarContenido command with only the required fields
        from content_management.modulos.content_management.aplicacion.comandos.comandos_contenido import BuscarContenido
        comando = BuscarContenido(
            saga_id=event_body.get('saga_id', ''),
            id=contenido_dto.id,
            creador=contenido_dto.creador,
            audiencia=contenido_dto.audiencia,
            campania=contenido_dto.campania,
            canales=contenido_dto.canales,
            marca=contenido_dto.marca,
            categoria=contenido_dto.categoria,
            fecha_creacion=contenido_dto.fecha_creacion or datetime.now().isoformat(),
            fecha_actualizacion=contenido_dto.fecha_actualizacion or datetime.now().isoformat()
        )

        ejecutar_commando(comando)

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
    except Exception as e:
        logger.error(f"Unexpected error in /buscar-contenido: {e}")
        return Response(json.dumps(dict(error=str(e))), status=500, mimetype='application/json')