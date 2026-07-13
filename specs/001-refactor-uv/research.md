# Research: refactor-uv

Este documento resume la investigación técnica y decisiones de diseño tomadas para la refactorización y centralización del entorno del proyecto TickerSec bajo la herramienta `uv`.

## 1. Decisiones de Configuración de Entorno

### Decisión 1: Estructura del pyproject.toml
*   **Selección**: Usar el estándar de metadatos PEP 621 definido en `pyproject.toml` para registrar las dependencias y la configuración de ejecución.
*   **Razón**: Es el formato estándar de empaquetado de Python moderno. `uv` lo consume directamente de manera nativa para compilar dependencias y sincronizar entornos virtuales (`uv sync`).
*   **Alternativas Consideradas**: 
    *   *Mantener requirements.txt tradicional*: Descartado. No provee un mecanismo nativo de bloqueo determinista como `uv.lock` y es más difícil de integrar con herramientas modernas de linting/formatting.
    *   *Poetry*: Descartado. El usuario especificó expresamente usar la librería `uv`. `uv` es sustancialmente más rápido que Poetry y tiene menor sobrecarga.

### Decisión 2: Aislamiento del Entorno Virtual (.venv)
*   **Selección**: Utilizar un directorio `.venv/` en la raíz del proyecto para alojar las dependencias locales.
*   **Razón**: Es el estándar de `uv` y se integra de forma transparente con editores modernos como VS Code o PyCharm, facilitando la autodetectación de paquetes y el intérprete de Python del proyecto.

### Decisión 3: Gestión de Scripts y Alias de Ejecución
*   **Selección**: Utilizar `uv run python manage.py <command>` para la ejecución de comandos.
*   **Razón**: Permite la ejecución de tareas de Django garantizando el aislamiento del entorno virtual sin necesidad de activar manualmente la terminal mediante `.venv/bin/activate`.

---

## 2. Mapeo de Dependencias

Se analizó el archivo `requirements.txt` actual para determinar las versiones de paquetes a migrar al `pyproject.toml`.

Las dependencias identificadas y sus versiones correspondientes son:
*   `django==5.0.11`
*   `python-decouple==3.8`
*   `psycopg2-binary==2.9.9`
*   `pillow==10.4.0`
*   `django-bootstrap5==24.2`
*   `django-quill-editor==0.1.40`
*   `pandas` (versión más reciente compatible con Python 3.10+)
*   `plotly==5.24.1`

Todas estas dependencias se agregarán al array `dependencies` de la sección `[project]` del `pyproject.toml`.
