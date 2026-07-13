# Quickstart: refactor-uv

Esta guía orienta al desarrollador sobre cómo inicializar y utilizar el entorno de TickerSec una vez refactorizado bajo `uv`.

## 1. Requisitos Previos

Asegúrate de tener instalados en el sistema global:
- **Python**: Versión >= 3.10
- **uv**: Instalado en el PATH global (puedes instalarlo con `curl -LsSf https://astral.sh/uv/install.sh | sh` o el instalador de tu plataforma).

## 2. Configuración Inicial del Entorno

Para inicializar el entorno y descargar todas las dependencias del proyecto de forma aislada, simplemente ejecuta el comando de sincronización de `uv` en la raíz del repositorio:

```bash
uv sync
```

Este comando:
1. Creará la carpeta de entorno virtual `.venv/` en la raíz (si no existe).
2. Leerá las dependencias declaradas en `pyproject.toml`.
3. Sincronizará e instalará de forma determinista todas las librerías necesarias, bloqueando las versiones en `uv.lock`.

## 3. Comandos de Ejecución Frecuentes

Para garantizar que los comandos se ejecuten dentro del contexto del entorno virtual local, antepón siempre `uv run`:

### Ejecutar el servidor de desarrollo Django:
```bash
uv run python manage.py runserver
```

### Ejecutar las migraciones de la base de datos:
```bash
uv run python manage.py migrate
```

### Poblar la base de datos con datos de prueba:
```bash
uv run python populatedb.py
```

### Correr los tests del proyecto:
```bash
uv run python manage.py test
```

### Agregar un nuevo paquete al proyecto:
```bash
uv add <nombre_paquete>
```
