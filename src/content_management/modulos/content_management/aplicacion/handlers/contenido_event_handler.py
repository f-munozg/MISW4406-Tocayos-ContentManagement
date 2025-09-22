"""Content Event Handler Adapter

This file implements the EventHandler port for content-related events.
This follows hexagonal architecture by implementing the application layer
contract for event handling.

"""

import logging
from datetime import datetime
from typing import Dict, Any
from content_management.modulos.content_management.aplicacion.handlers.event_handler import EventHandler
from content_management.modulos.content_management.aplicacion.comandos.comandos_contenido import BuscarContenido
from content_management.modulos.content_management.aplicacion.mapeadores import MapeadorContenidoDTOJson
from content_management.seedwork.aplicacion.comandos import ejecutar_commando
from content_management.seedwork.dominio.excepciones import ExcepcionDominio

logger = logging.getLogger(__name__)


class ContenidoEventHandler(EventHandler):
    """Adapter for handling content-related events"""
    
    def handle_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """
        Handle content-related events by executing the appropriate command
        
        Args:
            event_type: The type of content event
            event_data: The event payload data
            
        Raises:
            ExcepcionDominio: If domain rules are violated
            Exception: If event handling fails
        """
        try:
            logger.info(f"Handling content event: {event_type} with data: {event_data}")
            
            # Map the event data to DTO using the mapeador
            map_contenido = MapeadorContenidoDTOJson()
            contenido_dto = map_contenido.externo_a_dto(event_data)
            
            # Create BuscarContenido command
            comando = BuscarContenido(
                id=contenido_dto.id,
                saga_id=event_data.get('saga_id', ''),
                creador=contenido_dto.creador,
                audiencia=contenido_dto.audiencia,
                campania=contenido_dto.campania,
                canales=contenido_dto.canales,
                marca=contenido_dto.marca,
                categoria=contenido_dto.categoria,
                fecha_creacion=contenido_dto.fecha_creacion or datetime.now().isoformat(),
                fecha_actualizacion=contenido_dto.fecha_actualizacion or datetime.now().isoformat()
            )
            
            # Execute the command
            ejecutar_commando(comando)
            
            logger.info(f"Content event handled successfully for content: {contenido_dto.id}")
            
        except ExcepcionDominio as e:
            logger.error(f"Domain error handling content event: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error handling content event: {e}")
            raise
