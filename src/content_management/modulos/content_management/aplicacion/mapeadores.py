"""Mapeadores para la gestión de contenido

En este archivo se definen los mapeadores para la gestión de contenido

"""

from content_management.modulos.content_management.dominio.entidades import Contenido, TipoContenido, EstadoContenido, CategoriaContenido
from content_management.modulos.content_management.aplicacion.dto import ContenidoDTO
from datetime import datetime
import uuid

class MapeadorContenido:
    
    def dto_a_entidad(self, dto: ContenidoDTO) -> Contenido:
        contenido = Contenido()
        contenido.id = uuid.UUID(dto.id)
        contenido.id_campana = uuid.UUID(dto.id_campana) if dto.id_campana else None
        contenido.id_creador = uuid.UUID(dto.id_creador)
        contenido.id_marca = uuid.UUID(dto.id_marca)
        contenido.titulo = dto.titulo
        contenido.descripcion = dto.descripcion
        contenido.tipo_contenido = TipoContenido(dto.tipo_contenido)
        contenido.categoria = CategoriaContenido(dto.categoria)
        contenido.estado = EstadoContenido(dto.estado)
        contenido.url_media = dto.url_media
        contenido.hashtags = dto.hashtags
        contenido.menciones = dto.menciones
        contenido.plataformas = dto.plataformas
        contenido.metricas_engagement = dto.metricas_engagement
        contenido.metricas_alcance = dto.metricas_alcance
        contenido.metricas_impresiones = dto.metricas_impresiones
        contenido.metricas_clics = dto.metricas_clics
        contenido.costo_produccion = dto.costo_produccion
        
        if dto.fecha_programada:
            contenido.fecha_programada = datetime.fromisoformat(dto.fecha_programada)
        if dto.fecha_publicacion:
            contenido.fecha_publicacion = datetime.fromisoformat(dto.fecha_publicacion)
        
        return contenido
    
    def entidad_a_dto(self, entidad: Contenido) -> ContenidoDTO:
        return ContenidoDTO(
            id=str(entidad.id),
            id_campana=str(entidad.id_campana) if entidad.id_campana else "",
            id_creador=str(entidad.id_creador),
            id_marca=str(entidad.id_marca),
            titulo=entidad.titulo,
            descripcion=entidad.descripcion,
            tipo_contenido=entidad.tipo_contenido.value,
            categoria=entidad.categoria.value,
            estado=entidad.estado.value,
            url_media=entidad.url_media,
            hashtags=entidad.hashtags,
            menciones=entidad.menciones,
            fecha_programada=entidad.fecha_programada.isoformat() if entidad.fecha_programada else "",
            fecha_publicacion=entidad.fecha_publicacion.isoformat() if entidad.fecha_publicacion else "",
            plataformas=entidad.plataformas,
            metricas_engagement=entidad.metricas_engagement,
            metricas_alcance=entidad.metricas_alcance,
            metricas_impresiones=entidad.metricas_impresiones,
            metricas_clics=entidad.metricas_clics,
            costo_produccion=entidad.costo_produccion,
            fecha_creacion=entidad.fecha_creacion.isoformat(),
            fecha_ultima_actividad=entidad.fecha_ultima_actividad.isoformat(),
            fecha_actualizacion=entidad.fecha_actualizacion.isoformat()
        )

class MapeadorContenidoDTOJson:
    
    def externo_a_dto(self, externo: dict) -> ContenidoDTO:
        return ContenidoDTO(
            id=externo.get('id', str(uuid.uuid4())),
            id_campana=externo.get('id_campana', ''),
            id_creador=externo.get('id_creador', ''),
            id_marca=externo.get('id_marca', ''),
            titulo=externo.get('titulo', ''),
            descripcion=externo.get('descripcion', ''),
            tipo_contenido=externo.get('tipo_contenido', 'post_instagram'),
            categoria=externo.get('categoria', 'producto'),
            estado=externo.get('estado', 'borrador'),
            url_media=externo.get('url_media', ''),
            hashtags=externo.get('hashtags', ''),
            menciones=externo.get('menciones', ''),
            fecha_programada=externo.get('fecha_programada', ''),
            fecha_publicacion=externo.get('fecha_publicacion', ''),
            plataformas=externo.get('plataformas', ''),
            metricas_engagement=externo.get('metricas_engagement', 0),
            metricas_alcance=externo.get('metricas_alcance', 0),
            metricas_impresiones=externo.get('metricas_impresiones', 0),
            metricas_clics=externo.get('metricas_clics', 0),
            costo_produccion=externo.get('costo_produccion', 0.0),
            fecha_creacion=externo.get('fecha_creacion', ''),
            fecha_ultima_actividad=externo.get('fecha_ultima_actividad', ''),
            fecha_actualizacion=externo.get('fecha_actualizacion', '')
        )
    
    def dto_a_externo(self, dto: ContenidoDTO) -> dict:
        return {
            'id': dto.id,
            'id_campana': dto.id_campana,
            'id_creador': dto.id_creador,
            'id_marca': dto.id_marca,
            'titulo': dto.titulo,
            'descripcion': dto.descripcion,
            'tipo_contenido': dto.tipo_contenido,
            'categoria': dto.categoria,
            'estado': dto.estado,
            'url_media': dto.url_media,
            'hashtags': dto.hashtags,
            'menciones': dto.menciones,
            'fecha_programada': dto.fecha_programada,
            'fecha_publicacion': dto.fecha_publicacion,
            'plataformas': dto.plataformas,
            'metricas_engagement': dto.metricas_engagement,
            'metricas_alcance': dto.metricas_alcance,
            'metricas_impresiones': dto.metricas_impresiones,
            'metricas_clics': dto.metricas_clics,
            'costo_produccion': dto.costo_produccion,
            'fecha_creacion': dto.fecha_creacion,
            'fecha_ultima_actividad': dto.fecha_ultima_actividad,
            'fecha_actualizacion': dto.fecha_actualizacion
        }
