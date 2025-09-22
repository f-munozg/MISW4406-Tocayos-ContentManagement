"""Servicio de Consumo de Eventos

En este archivo se define el servicio principal para consumir eventos de Pulsar

"""

import json
import logging
import threading
from typing import Dict, Any, Optional
from content_management.infraestructura.pulsar import PulsarEventConsumer, PulsarConfig
from content_management.modulos.content_management.aplicacion.handlers.event_handler import EventHandler

logger = logging.getLogger(__name__)

class EventConsumerService:
    def __init__(self, app=None, event_handler: Optional[EventHandler] = None):
        self.config = PulsarConfig()
        self.consumers = {}
        self.running = False
        self.app = app
        self.event_handler = event_handler
        
    def start_consuming(self):
        """Inicia el consumo de eventos para todos los módulos"""
        self.running = True

        # Escuchar eventos de contenido y campaña
        self._start_consumer('content-events', self._handle_content_event)
        self._start_consumer('campaign-events', self._handle_campaign_event)

        logger.info("Servicio de consumo de eventos iniciado")
    def _handle_campaign_event(self, event_data: Dict[str, Any]):
        """Maneja eventos de campaign-events para la saga"""
        try:
            logger.info(f"Received campaign event: {event_data}")
            event_type = event_data.get('event_type')
            status = event_data.get('status')
            saga_id = event_data.get('saga_id')
            payload = event_data.get('event_data', event_data)

            logger.info(f"Procesando evento de campaña: {event_type} con status: {status}")

            # Saga: Si recibimos EventCampaignCreated con status success, lanzamos BuscarContenido
            if event_type == 'EventCampaignCreated' and status == 'success':
                from content_management.modulos.content_management.aplicacion.comandos.comandos_contenido import BuscarContenido
                from content_management.modulos.content_management.aplicacion.mapeadores import MapeadorContenidoDTOJson
                from content_management.seedwork.aplicacion.comandos import ejecutar_commando
                from datetime import datetime
                
                # Ensure we're in a Flask app context when executing commands
                if self.app:
                    with self.app.app_context():
                        # Map the event data to DTO using the mapeador
                        map_contenido = MapeadorContenidoDTOJson()
                        contenido_dto = map_contenido.externo_a_dto(event_data)
                        
                        # Build BuscarContenido command with saga_id
                        comando = BuscarContenido(
                            id=contenido_dto.id,
                            saga_id=saga_id,
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
                        logger.info(f"BuscarContenido lanzado por saga para id: {contenido_dto.id}")
                else:
                    logger.warning("No Flask app context available for campaign event processing")

        except Exception as e:
            logger.error(f"Error procesando evento de campaña: {e}")
            logger.error(f"Event data: {event_data}")

    def _handle_content_event(self, event_data: Dict[str, Any]):
        """Maneja eventos de content-events para la saga"""
        try:
            logger.info(f"Received content event: {event_data}")
            event_type = event_data.get('event_type')
            status = event_data.get('status')
            saga_id = event_data.get('saga_id')
            payload = event_data.get('event_data', event_data)

            logger.info(f"Procesando evento de contenido: {event_type} con status: {status}")

            # Saga: Si CommandCreatePartner falla, lanzamos CommandContentRollbacked
            if event_type == 'CommandCreatePartner' and status == 'failed':
                from content_management.modulos.content_management.aplicacion.comandos.comandos_contenido import CommandContentRollbacked
                from content_management.seedwork.aplicacion.comandos import ejecutar_commando
                
                # Ensure we're in a Flask app context when executing commands
                if self.app:
                    with self.app.app_context():
                        comando = CommandContentRollbacked(
                            saga_id=saga_id,
                            id=payload.get('id'),
                            motivo=payload.get('motivo', 'Error en creación de partner'),
                            fecha_rollback=''
                        )
                        ejecutar_commando(comando)
                        logger.info(f"CommandContentRollbacked lanzado por saga para id: {payload.get('id')}")
                else:
                    logger.warning("No Flask app context available for content event processing")

        except Exception as e:
            logger.error(f"Error procesando evento de contenido: {e}")
            logger.error(f"Event data: {event_data}")
    
    def stop_consuming(self):
        """Detiene el consumo de eventos"""
        self.running = False
        for consumer in self.consumers.values():
            consumer.close()
        logger.info("Servicio de consumo de eventos detenido")
    
    def _start_consumer(self, event_type: str, handler):
        """Inicia un consumidor para un tipo específico de evento"""
        try:
            consumer = PulsarEventConsumer()
            topic_name = self.config.get_topic_name(event_type)
            subscription_name = f"{event_type}-subscription"
            
            logger.info(f"Subscribing to topic: {topic_name}")
            logger.info(f"Using subscription: {subscription_name}")
            logger.info(f"Pulsar service URL: {self.config.service_url}")
            
            consumer.subscribe_to_topic(topic_name, subscription_name, handler)
            self.consumers[event_type] = consumer
            logger.info(f"Consumidor iniciado para {event_type} en topic {topic_name}")
        except Exception as e:
            logger.error(f"Error iniciando consumidor para {event_type}: {e}")
            logger.error(f"Topic name: {topic_name}")
            logger.error(f"Service URL: {self.config.service_url}")
    

# Instancia global del servicio - será creada con Flask app context
event_consumer_service = None

def create_event_consumer_service(app, event_handler=None):
    """Create the event consumer service with Flask app context"""
    global event_consumer_service
    if event_consumer_service is None:
        event_consumer_service = EventConsumerService(app, event_handler)
    return event_consumer_service
