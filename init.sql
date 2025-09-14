-- Script de inicialización de la base de datos para Content Management

-- Crear esquema si no existe
CREATE SCHEMA IF NOT EXISTS content_management;

-- Crear tabla de contenido
CREATE TABLE IF NOT EXISTS contenido (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_campana UUID,
    id_creador UUID NOT NULL,
    id_marca UUID NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    tipo_contenido VARCHAR(50) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    estado VARCHAR(50) NOT NULL DEFAULT 'borrador',
    url_media TEXT,
    hashtags TEXT,
    menciones TEXT,
    fecha_programada TIMESTAMP,
    fecha_publicacion TIMESTAMP,
    plataformas TEXT,
    metricas_engagement INTEGER NOT NULL DEFAULT 0,
    metricas_alcance INTEGER NOT NULL DEFAULT 0,
    metricas_impresiones INTEGER NOT NULL DEFAULT 0,
    metricas_clics INTEGER NOT NULL DEFAULT 0,
    costo_produccion FLOAT NOT NULL DEFAULT 0.0,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_ultima_actividad TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_contenido_id_campana ON contenido(id_campana);
CREATE INDEX IF NOT EXISTS idx_contenido_id_creador ON contenido(id_creador);
CREATE INDEX IF NOT EXISTS idx_contenido_id_marca ON contenido(id_marca);
CREATE INDEX IF NOT EXISTS idx_contenido_estado ON contenido(estado);
CREATE INDEX IF NOT EXISTS idx_contenido_tipo ON contenido(tipo_contenido);
CREATE INDEX IF NOT EXISTS idx_contenido_categoria ON contenido(categoria);
CREATE INDEX IF NOT EXISTS idx_contenido_fecha_creacion ON contenido(fecha_creacion);

-- Insertar datos de ejemplo
INSERT INTO contenido (id, id_campana, id_creador, id_marca, titulo, descripcion, tipo_contenido, categoria, estado, url_media, hashtags, plataformas, costo_produccion) VALUES
    (gen_random_uuid(), gen_random_uuid(), gen_random_uuid(), gen_random_uuid(), 'Post Verano 2024', 'Contenido promocional para el verano', 'post_instagram', 'promocional', 'borrador', 'https://example.com/media1.jpg', '#verano2024 #promocion', 'instagram', 500.0),
    (gen_random_uuid(), gen_random_uuid(), gen_random_uuid(), gen_random_uuid(), 'Video Tutorial', 'Tutorial de producto', 'video_youtube', 'educacional', 'aprobado', 'https://example.com/video1.mp4', '#tutorial #producto', 'youtube', 1200.0);
