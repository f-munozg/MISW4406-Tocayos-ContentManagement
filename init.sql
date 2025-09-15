-- Script de inicialización de la base de datos para Content Management

-- Crear esquema si no existe
CREATE SCHEMA IF NOT EXISTS content_management;

-- Crear tabla de contenido
CREATE TABLE IF NOT EXISTS contenido (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    creador VARCHAR(255) NOT NULL,
    audiencia VARCHAR(255) NOT NULL,
    campania VARCHAR(255) NOT NULL,
    canales VARCHAR(255) NOT NULL,
    marca VARCHAR(255) NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_contenido_id_creador ON contenido(creador);
CREATE INDEX IF NOT EXISTS idx_contenido_id_marca ON contenido(marca);
CREATE INDEX IF NOT EXISTS idx_contenido_tipo ON contenido(campania);
CREATE INDEX IF NOT EXISTS idx_contenido_categoria ON contenido(audiencia);