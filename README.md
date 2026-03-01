# Company Fredd - MCP Server

Servidor MCP (Model Context Protocol) para gestionar empleados de un bufete de abogados. Permite a modelos de lenguaje (como Claude) consultar y agregar empleados a una base de datos PostgreSQL mediante herramientas MCP.

## Arquitectura

```
┌─────────────────────┐
│   Cliente MCP       │
│   (Claude, etc.)    │
└──────────┬──────────┘
           │ SSE (port 3000)
┌──────────▼──────────┐
│   FastMCP Server    │
│   (main.py)         │
└──────────┬──────────┘
           │ psycopg2
┌──────────▼──────────┐
│   PostgreSQL 16     │
│   (init.sql)        │
└─────────────────────┘
```

## Herramientas MCP disponibles

| Herramienta      | Descripcion                                  | Parametros                                                  |
|------------------|----------------------------------------------|-------------------------------------------------------------|
| `list_employees` | Lista empleados con limite opcional           | `limit` (int, default: 5)                                   |
| `add_employee`   | Agrega un nuevo empleado a la base de datos   | `name`, `position`, `department`, `salary`, `hire_date` (opcional) |

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes)
- Docker y Docker Compose

## Inicio rapido

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd fast_mcp_course
```

### 2. Configurar variables de entorno

Crear un archivo `.env` en la raiz del proyecto:

```env
DB_HOST=postgres
DB_PORT=5432
DB_NAME=company_fredd
DB_USER=postgres
DB_PASSWORD=tu_password_seguro
```

> **Nota:** Cuando se ejecuta con Docker Compose, `DB_HOST` debe ser `postgres` (nombre del servicio). Para desarrollo local sin Docker, usar `localhost`.

### 3. Levantar con Docker Compose

```bash
docker compose up --build -d
```

Esto levanta:
- **PostgreSQL 16** (Alpine) con la tabla `employees` pre-poblada con 10 registros
- **MCP Server** en el puerto `3000` con transporte SSE

### 4. Verificar que funciona

```bash
# Ver logs del servidor MCP
docker logs company_mcp_server

# Ver logs de PostgreSQL
docker logs company_postgres
```

## Desarrollo local (sin Docker)

```bash
# Instalar dependencias
uv sync

# Levantar PostgreSQL localmente y ejecutar init.sql

# Ejecutar el servidor
uv run python main.py
```

El servidor se inicia en `http://localhost:3000` con transporte SSE.

## Conectar con Claude Desktop

Agregar al archivo de configuracion de Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "company-fredd": {
      "url": "http://localhost:3000/sse"
    }
  }
}
```

## Estructura del proyecto

```
fast_mcp_course/
├── main.py              # Servidor MCP con herramientas
├── init.sql             # Schema y datos iniciales de empleados
├── Dockerfile           # Imagen del servidor MCP
├── docker-compose.yml   # Orquestacion de servicios
├── pyproject.toml       # Dependencias del proyecto
├── uv.lock              # Lock de dependencias
└── .env                 # Variables de entorno (no versionado)
```

## Datos iniciales

La base de datos se inicializa con 10 empleados del bufete:

| Nombre              | Posicion           | Departamento          | Salario   |
|---------------------|--------------------|-----------------------|-----------|
| Alejandro Morales   | Socio Senior       | Litigios              | $120,000  |
| Isabel Fernandez    | Abogada Asociada   | Derecho Corporativo   | $85,000   |
| Roberto Castillo    | Socio Fundador     | Derecho Penal         | $150,000  |
| Valentina Torres    | Abogada Junior     | Derecho Laboral       | $55,000   |
| Diego Ramirez       | Paralegal Senior   | Litigios              | $45,000   |
| Sofia Herrera       | Abogada Asociada   | Derecho Inmobiliario  | $80,000   |
| Andres Vargas       | Director Legal     | Compliance            | $110,000  |
| Camila Jimenez      | Abogada Junior     | Derecho Corporativo   | $52,000   |
| Luis Mendoza        | Paralegal          | Derecho Laboral       | $38,000   |
| Patricia Nunez      | Secretaria Legal   | Administracion        | $32,000   |

## Stack tecnologico

- **FastMCP** >= 3.0.2 - Framework para servidores MCP
- **psycopg2** >= 2.9.11 - Adaptador PostgreSQL para Python
- **PostgreSQL 16** (Alpine) - Base de datos
- **Docker** - Containerizacion
- **uv** - Gestor de paquetes Python
