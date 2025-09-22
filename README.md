# Content Management Microservice

Este microservicio se encarga de la gestión de contenido de marketing siguiendo una arquitectura orientada a eventos.

## Características

### Arquitectura

El microservicio sigue los principios de Domain-Driven Design (DDD) con:

- **Dominio**: Entidades, eventos de dominio y reglas de negocio
- **Aplicación**: Comandos, queries, handlers y DTOs
- **Infraestructura**: Modelos de base de datos, Pulsar, configuración
- **API**: Endpoints REST para operaciones CRUD

### Tecnologías

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

### `GET /content-management/content`

Permite buscar el contenido asociado a una campaña.

#### Body

```json
{
    "audiencia": "string",
    "campania": "string",
    "canales": "string",
    "marca": "string",
    "categoria": "string"
}
```

#### Evento creado
```json
{
    "identificacion": "string",
    "campania_asociada": "string",
    "canales": "string",
    "marca": "string",
    "categoria": "string"
}
```

## Eventos

El microservicio publica los siguientes eventos en Pulsar:

- `CommandCreatePartner` - Cuando se buscar asociar contenido a un partner

## Estructura del Proyecto

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
