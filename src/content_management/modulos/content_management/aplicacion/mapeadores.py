"""Mapeadores para la gestión de contenido

En este archivo se definen los mapeadores para la gestión de contenido

"""

from content_management.modulos.content_management.aplicacion.dto import ContenidoDTO
from datetime import datetime
import uuid

class MapeadorContenidoDTOJson:

    def externo_a_dto(self, externo: dict) -> ContenidoDTO:
        # Handle both direct event data and nested event_data
        event_data = externo.get('event_data', externo)
        
        return ContenidoDTO(
            id=event_data.get('id', str(uuid.uuid4())),
            creador=event_data.get('creador', event_data.get('tipo', 'campaign_created')),  # Use 'tipo' as creator if no creator field
            audiencia=event_data.get('audiencia', ''),
            campania=event_data.get('campania', event_data.get('tipo', '')),  # Use 'tipo' as campaign if no campaign field
            canales=event_data.get('canales', ''),
            marca=event_data.get('marca', ''),
            categoria=event_data.get('categoria', ''),
            fecha_creacion=event_data.get('fecha_creacion', event_data.get('fecha_evento', '')),
            fecha_actualizacion=event_data.get('fecha_actualizacion', event_data.get('fecha_evento', ''))
        )
    
    def dto_a_externo(self, dto: ContenidoDTO) -> dict:
        return {
            'id': dto.id,
            'creador': dto.creador,
            'audiencia': dto.audiencia,
            'campania': dto.campania,
            'canales': dto.canales,
            'marca': dto.marca,
            'categoria': dto.categoria,
            'fecha_creacion': dto.fecha_creacion,
            'fecha_actualizacion': dto.fecha_actualizacion
        }
