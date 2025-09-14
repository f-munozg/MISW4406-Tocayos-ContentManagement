# Content Management Microservice

Este microservicio se encarga de la gestión de contenido de marketing, incluyendo su creación, revisión, aprobación, publicación y archivado.

## Características

- **Gestión de Contenido**: Crear, enviar a revisión, aprobar, rechazar, publicar y archivar contenido
- **Tipos de Contenido**: Post Instagram, Story Instagram, Post Facebook, Video YouTube, Post TikTok, Blog Post, Email Marketing, Infografía
- **Categorías**: Producto, Lifestyle, Educacional, Promocional, Testimonial, Entertainment
- **Estados**: Borrador, En Revisión, Aprobado, Publicado, Archivado, Rechazado
- **Métricas**: Seguimiento de engagement, alcance, impresiones y clics
- **Eventos**: Arquitectura orientada a eventos con Pulsar
- **Base de Datos**: PostgreSQL con SQLAlchemy

## Arquitectura

El microservicio sigue los principios de Domain-Driven Design (DDD) con:

- **Dominio**: Entidades, eventos de dominio y reglas de negocio
- **Aplicación**: Comandos, queries, handlers y DTOs
- **Infraestructura**: Modelos de base de datos, Pulsar, configuración
- **API**: Endpoints REST para operaciones CRUD

## Tecnologías

- **Backend**: Python 3.11, Flask
- **Base de Datos**: PostgreSQL 15
- **Eventos**: Apache Pulsar 3.1.0
- **ORM**: SQLAlchemy
- **Contenedores**: Docker, Docker Compose

## Instalación y Ejecución

### Con Docker Compose (Recomendado)

```bash
# Clonar el repositorio
git clone <repository-url>
cd content-management

# Ejecutar con Docker Compose
docker-compose up -d

# El microservicio estará disponible en http://localhost:5001
```

### Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export DATABASE_URL="postgresql://user:password@localhost:5432/content_management"
export PULSAR_SERVICE_URL="pulsar://localhost:6650"
export PULSAR_ADMIN_URL="http://localhost:8080"

# Ejecutar la aplicación
python src/content_management/main.py
```

## API Endpoints

### Contenido

- `POST /content-management/content` - Crear contenido
- `PUT /content-management/content/{id}/enviar-revision` - Enviar a revisión
- `PUT /content-management/content/{id}/aprobar` - Aprobar contenido
- `PUT /content-management/content/{id}/rechazar` - Rechazar contenido
- `PUT /content-management/content/{id}/publicar` - Publicar contenido
- `PUT /content-management/content/{id}/archivar` - Archivar contenido
- `PUT /content-management/content/{id}/actualizar-metricas` - Actualizar métricas
- `GET /content-management/content/{id}` - Obtener contenido
- `GET /content-management/contents/campana/{id_campana}` - Obtener contenidos por campaña
- `GET /content-management/contents/creador/{id_creador}` - Obtener contenidos por creador
- `GET /content-management/contents/marca/{id_marca}` - Obtener contenidos por marca
- `GET /content-management/contents/tipo/{tipo}` - Obtener contenidos por tipo
- `GET /content-management/contents/estado/{estado}` - Obtener contenidos por estado

## Eventos

El microservicio publica los siguientes eventos en Pulsar:

- `ContenidoCreado` - Cuando se crea nuevo contenido
- `ContenidoEnviadoRevision` - Cuando se envía contenido a revisión
- `ContenidoAprobado` - Cuando se aprueba contenido
- `ContenidoRechazado` - Cuando se rechaza contenido
- `ContenidoPublicado` - Cuando se publica contenido
- `ContenidoArchivado` - Cuando se archiva contenido
- `MetricasContenidoActualizadas` - Cuando se actualizan las métricas

## Configuración

### Variables de Entorno

- `DATABASE_URL`: URL de conexión a PostgreSQL
- `PULSAR_SERVICE_URL`: URL del servicio Pulsar
- `PULSAR_ADMIN_URL`: URL del admin de Pulsar
- `FLASK_ENV`: Entorno de Flask (development/production)

### Base de Datos

El microservicio utiliza PostgreSQL con la siguiente estructura:

- **Tabla**: `contenido`
- **Esquema**: `content_management`
- **Índices**: Optimizados para consultas por campaña, creador, marca, estado y tipo

## Monitoreo

- **Pulsar Manager**: http://localhost:9528
- **Logs**: Disponibles en los contenedores Docker
- **Métricas**: A través de los eventos publicados en Pulsar

## Desarrollo

### Estructura del Proyecto

```
src/content_management/
├── api/                    # Endpoints REST
├── config/                 # Configuración
├── infraestructura/        # Pulsar, base de datos
├── modulos/
│   └── content_management/
│       ├── aplicacion/     # Comandos, queries, handlers
│       ├── dominio/        # Entidades, eventos
│       └── infraestructura/ # Modelos de BD
└── seedwork/              # Código reutilizable
```

### Agregar Nuevas Funcionalidades

1. **Dominio**: Definir entidades y eventos en `dominio/`
2. **Aplicación**: Crear comandos/queries en `aplicacion/`
3. **Infraestructura**: Implementar persistencia en `infraestructura/`
4. **API**: Exponer endpoints en `api/`

## Contribución

1. Fork el repositorio
2. Crear una rama para la funcionalidad
3. Hacer commit de los cambios
4. Crear un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT.
