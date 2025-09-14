"""Queries para la gestión de contenido

En este archivo se definen las queries para la gestión de contenido

"""

from dataclasses import dataclass
from abc import ABC, abstractmethod

class Query:
    ...

class QueryHandler(ABC):
    @abstractmethod
    def handle(self, query: Query):
        raise NotImplementedError()

@dataclass
class ObtenerContenido(Query):
    id_contenido: str

@dataclass
class ObtenerContenidosPorCampana(Query):
    id_campana: str

@dataclass
class ObtenerContenidosPorCreador(Query):
    id_creador: str

@dataclass
class ObtenerContenidosPorMarca(Query):
    id_marca: str

@dataclass
class ObtenerContenidosPorTipo(Query):
    tipo_contenido: str

@dataclass
class ObtenerContenidosPorEstado(Query):
    estado: str

@dataclass
class ObtenerContenidosPublicados(Query):
    pass

@dataclass
class ObtenerContenidosPorCategoria(Query):
    categoria: str
