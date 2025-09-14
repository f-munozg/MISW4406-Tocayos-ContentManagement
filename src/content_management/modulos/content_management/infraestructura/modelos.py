"""Modelos de base de datos para contenido

En este archivo se definen los modelos de base de datos para contenido

"""

from content_management.config.db import db
from sqlalchemy import Column, String, DateTime, Float, Integer, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from enum import Enum as PyEnum

class ContenidoDBModel(db.Model):
    __tablename__ = "contenido"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creador = Column(String(255), nullable=False)
    audiencia = Column(String(255), nullable=False)
    campania = Column(String(255), nullable=False)
    canales = Column(String(255), nullable=False)
    marca = Column(String(255), nullable=False)
    categoria = Column(String(255), nullable=False)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Contenido {self.titulo} ({self.estado.value})>"
