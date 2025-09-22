"""Aplicación principal del microservicio Content Management

En este archivo se define la aplicación principal del microservicio
"""

from flask import Flask
from content_management.config.db import init_db
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos
    database_url = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/content_management')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar base de datos
    init_db(app)
    
    # Importar handlers de comandos para registrar los dispatchers
    try:
        from content_management.modulos.content_management.aplicacion.handlers import crear_contenido_handler
        from content_management.modulos.content_management.aplicacion.handlers import crear_partner_handler
        logger.info("Handlers de content management registrados")
    except Exception as e:
        logger.error(f"Error registrando handlers de content management: {e}")
    
    try:
        from content_management.api.content_management import bp as content_management_bp
        app.register_blueprint(content_management_bp)
        logger.info("Blueprint de content management registrado")
    except Exception as e:
        logger.error(f"Error registrando blueprint de content management: {e}")
    
    # Inicializar servicios de Pulsar (opcional)
    try:
        from content_management.infraestructura.event_consumer_service import create_event_consumer_service
        from content_management.infraestructura.pulsar import pulsar_publisher
        from content_management.modulos.content_management.aplicacion.handlers.contenido_event_handler import ContenidoEventHandler
        import atexit
        
        # Crear el event handler
        contenido_event_handler = ContenidoEventHandler()
        
        # Iniciar el servicio de consumo de eventos con el handler
        event_consumer_service = create_event_consumer_service(app, contenido_event_handler)
        event_consumer_service.start_consuming()
        logger.info("Servicio de consumo de eventos iniciado con ContenidoEventHandler")
        
        # Registrar función de limpieza al cerrar la aplicación
        atexit.register(cleanup_pulsar_connections)
        
    except Exception as e:
        logger.warning(f"Pulsar no disponible, continuando sin eventos: {e}")
    
    return app

def cleanup_pulsar_connections():
    """Limpia las conexiones de Pulsar al cerrar la aplicación"""
    try:
        from content_management.infraestructura.pulsar import pulsar_publisher
        pulsar_publisher.close()
        logger.info("Conexiones de Pulsar cerradas correctamente")
    except Exception as e:
        logger.error(f"Error cerrando conexiones de Pulsar: {e}")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
