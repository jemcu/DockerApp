# Gestor de tareas con Docker Compose

Aplicación contenerizada formada por una API Flask, una interfaz web servida por Nginx y una base de datos MySQL 8.4. Los servicios se comunican por la red privada de Docker Compose; la aplicación web queda disponible en el puerto `8080` del equipo.

## Requisitos

- Docker Desktop (Windows/macOS) o Docker Engine
- Docker Compose v2 (`docker compose`)
- Git, si se va a clonar el repositorio

## Clonar y configurar

Clona el repositorio y entra en su carpeta:

```bash
git clone <URL_DEL_REPOSITORIO>
cd actividad2_Docker
```

Crea el archivo `.env` copiando la plantilla:

```bash
cp .env.example .env
```

En Windows PowerShell puedes usar:

```powershell
Copy-Item .env.example .env
```

Edita `.env` y define valores propios para `DB_ROOT_PASSWORD`, `DB_NAME`, `DB_USER` y `DB_PASSWORD`. El `.env` incluido en el proyecto es únicamente para desarrollo local; no uses esas contraseñas en producción ni publiques el archivo.

## Ejecutar

Desde la carpeta raíz del proyecto:

```bash
docker compose up -d --build
```

Abre <http://localhost:8080> para usar el gestor de tareas. La API también ofrece `GET /api/estado` (estado y versión) y los endpoints de tareas bajo `/api/tareas`.

## Construir las imágenes de la API por versión

Para practicar la construcción independiente de la API, ejecuta desde la carpeta raíz:

```bash
docker build -t tareas-api:1.0 ./api
docker build -t tareas-api:1.1 ./api
docker image ls tareas-api
```

Compose construye y ejecuta la API con la etiqueta `tareas-api:1.1`.

Comandos útiles:

```bash
docker compose ps
docker compose logs -f
docker volume ls
docker compose down
```

Los datos de MySQL se conservan en el volumen `datos-bd` al detener los servicios. Para eliminar también la base persistida, ejecuta `docker compose down -v`; esta acción borra permanentemente esos datos.

## Estructura

```text
actividad2_Docker/
├── api/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── index.html
│   ├── nginx.conf
│   └── Dockerfile
├── .env.example
├── .gitignore
└── compose.yaml
```

## Integrantes

- [Nombre y apellido]
- [Nombre y apellido]
- [Nombre y apellido]
