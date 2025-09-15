"""Mapeadores para la gestión de contenido

En este archivo se definen los mapeadores para la gestión de contenido

"""

from content_management.modulos.content_management.aplicacion.dto import ContenidoDTO
from datetime import datetime
import uuid

class MapeadorContenidoDTOJson:

    def externo_a_dto(self, externo: dict) -> ContenidoDTO:
        return ContenidoDTO(
            id=externo.get('id', str(uuid.uuid4())),
            creador=externo.get('creador', str(uuid.uuid4())),
            audiencia=externo.get('audiencia', ''),
            campania=externo.get('campania', ''),
            canales=externo.get('canales', ''),
            marca=externo.get('marca', ''),
            categoria=externo.get('categoria', ''),
            fecha_creacion=externo.get('fecha_creacion', ''),
            fecha_actualizacion=externo.get('fecha_actualizacion', '')
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
