"""API para la gestión de contenido

En este archivo se define la API REST para la gestión de contenido

"""

from flask import Blueprint, request, jsonify, Response
from content_management.modulos.content_management.aplicacion.comandos.comandos_contenido import (
    CrearContenido, EnviarRevisionContenido, AprobarContenido, RechazarContenido,
    PublicarContenido, ArchivarContenido, ActualizarMetricasContenido
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

@bp.route('/content', methods=['POST'])
def crear_contenido():
    try:
        contenido_dict = request.json
        logger.info(f"Request data: {contenido_dict}")
        
        map_contenido = MapeadorContenidoDTOJson()
        contenido_dto = map_contenido.externo_a_dto(contenido_dict)
        
        comando = CrearContenido(
            id=contenido_dto.id,
            id_campana=contenido_dto.id_campana,
            id_creador=contenido_dto.id_creador,
            id_marca=contenido_dto.id_marca,
            titulo=contenido_dto.titulo,
            descripcion=contenido_dto.descripcion,
            tipo_contenido=contenido_dto.tipo_contenido,
            categoria=contenido_dto.categoria,
            url_media=contenido_dto.url_media,
            hashtags=contenido_dto.hashtags,
            menciones=contenido_dto.menciones,
            fecha_programada=contenido_dto.fecha_programada,
            plataformas=contenido_dto.plataformas,
            costo_produccion=contenido_dto.costo_produccion,
            fecha_creacion=datetime.now().isoformat(),
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/content/<id>/enviar-revision', methods=['PUT'])
def enviar_revision_contenido(id):
    try:
        comando = EnviarRevisionContenido(
            id_contenido=id,
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/content/<id>/aprobar', methods=['PUT'])
def aprobar_contenido(id):
    try:
        data = request.json
        aprobador = data.get('aprobador', '') if data else ''
        
        comando = AprobarContenido(
            id_contenido=id,
            aprobador=aprobador,
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/content/<id>/rechazar', methods=['PUT'])
def rechazar_contenido(id):
    try:
        data = request.json
        motivo = data.get('motivo', '') if data else ''
        aprobador = data.get('aprobador', '') if data else ''
        
        comando = RechazarContenido(
            id_contenido=id,
            motivo=motivo,
            aprobador=aprobador,
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/content/<id>/publicar', methods=['PUT'])
def publicar_contenido(id):
    try:
        data = request.json
        fecha_publicacion = data.get('fecha_publicacion', '') if data else ''
        
        comando = PublicarContenido(
            id_contenido=id,
            fecha_publicacion=fecha_publicacion,
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/content/<id>/archivar', methods=['PUT'])
def archivar_contenido(id):
    try:
        data = request.json
        motivo = data.get('motivo', '') if data else ''
        
        comando = ArchivarContenido(
            id_contenido=id,
            motivo=motivo,
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/content/<id>/actualizar-metricas', methods=['PUT'])
def actualizar_metricas_contenido(id):
    try:
        data = request.json
        engagement = data.get('engagement', 0) if data else 0
        alcance = data.get('alcance', 0) if data else 0
        impresiones = data.get('impresiones', 0) if data else 0
        clics = data.get('clics', 0) if data else 0
        
        comando = ActualizarMetricasContenido(
            id_contenido=id,
            engagement=engagement,
            alcance=alcance,
            impresiones=impresiones,
            clics=clics,
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/content/<id>', methods=['GET'])
def obtener_contenido(id):
    try:
        query = ObtenerContenido(id_contenido=id)
        # TODO: Implementar query handler
        return jsonify({'message': 'Query not implemented yet'})
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/contents/campana/<id_campana>', methods=['GET'])
def obtener_contenidos_por_campana(id_campana):
    try:
        query = ObtenerContenidosPorCampana(id_campana=id_campana)
        # TODO: Implementar query handler
        return jsonify({'message': 'Query not implemented yet'})
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/contents/creador/<id_creador>', methods=['GET'])
def obtener_contenidos_por_creador(id_creador):
    try:
        query = ObtenerContenidosPorCreador(id_creador=id_creador)
        # TODO: Implementar query handler
        return jsonify({'message': 'Query not implemented yet'})
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/contents/marca/<id_marca>', methods=['GET'])
def obtener_contenidos_por_marca(id_marca):
    try:
        query = ObtenerContenidosPorMarca(id_marca=id_marca)
        # TODO: Implementar query handler
        return jsonify({'message': 'Query not implemented yet'})
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/contents/tipo/<tipo_contenido>', methods=['GET'])
def obtener_contenidos_por_tipo(tipo_contenido):
    try:
        query = ObtenerContenidosPorTipo(tipo_contenido=tipo_contenido)
        # TODO: Implementar query handler
        return jsonify({'message': 'Query not implemented yet'})
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/contents/estado/<estado>', methods=['GET'])
def obtener_contenidos_por_estado(estado):
    try:
        query = ObtenerContenidosPorEstado(estado=estado)
        # TODO: Implementar query handler
        return jsonify({'message': 'Query not implemented yet'})
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
