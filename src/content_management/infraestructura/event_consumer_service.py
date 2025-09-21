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

            # Saga: Si recibimos EventCampaignCreated con status success, lanzamos CommandCreatePartner
            if event_type == 'EventCampaignCreated' and status == 'success':
                from content_management.modulos.content_management.aplicacion.comandos.comandos_contenido import CommandCreatePartner
                from content_management.seedwork.aplicacion.comandos import ejecutar_commando
                # Extraer los datos necesarios del payload
                comando = CommandCreatePartner(
                    saga_id=saga_id,
                    id=payload.get('id'),
                    id_marca=payload.get('id_marca'),
                    id_partner=payload.get('id_partner'),
                    tipo_partnership=payload.get('tipo_partnership', ''),
                    terminos_contrato=payload.get('terminos_contrato', ''),
                    comision_porcentaje=payload.get('comision_porcentaje', 0.0),
                    metas_mensuales=payload.get('metas_mensuales', ''),
                    beneficios_adicionales=payload.get('beneficios_adicionales', ''),
                    notas=payload.get('notas', ''),
                    fecha_creacion=payload.get('fecha_creacion', ''),
                    fecha_actualizacion=payload.get('fecha_actualizacion', '')
                )
                ejecutar_commando(comando)
                logger.info(f"CommandCreatePartner lanzado por saga para id_partner: {payload.get('id_partner')}")

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
                comando = CommandContentRollbacked(
                    saga_id=saga_id,
                    id=payload.get('id'),
                    motivo=payload.get('motivo', 'Error en creación de partner'),
                    fecha_rollback=''
                )
                ejecutar_commando(comando)
                logger.info(f"CommandContentRollbacked lanzado por saga para id: {payload.get('id')}")

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
    
    def _handle_content_event(self, event_data: Dict[str, Any]):
        """Maneja eventos de contenido delegando al event handler"""
        try:
            logger.info(f"Received content event: {event_data}")
            
            # Handle different event structures
            event_type = event_data.get('event_type')
            event_payload = event_data.get('event_data', event_data)  # Fallback to full event_data
            
            logger.info(f"Procesando evento de contenido: {event_type}")
            logger.info(f"Event payload: {event_payload}")
            
            if self.event_handler:
                # Ensure we're in a Flask app context when using the event handler
                if self.app:
                    with self.app.app_context():
                        self.event_handler.handle_event(event_type, event_payload)
                else:
                    logger.warning("No Flask app context available for event handler")
            else:
                logger.warning("No event handler configured, skipping event processing")

        except Exception as e:
            logger.error(f"Error procesando evento de contenido: {e}")
            logger.error(f"Event data: {event_data}")

# Instancia global del servicio - será creada con Flask app context
event_consumer_service = None

def create_event_consumer_service(app, event_handler=None):
    """Create the event consumer service with Flask app context"""
    global event_consumer_service
    if event_consumer_service is None:
        event_consumer_service = EventConsumerService(app, event_handler)
    return event_consumer_service
